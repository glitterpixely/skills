// Runs gates G0–G3 (automated) and builds the G4 critic packet for the three.js quality loop.
// Usage (from the project root, with playwright-core installed there and the project served over http):
//   node run-gates.mjs --url http://localhost:8765/quality/gate-harness.html --ceiling quality/ceiling.json \
//        --out quality/pass-03 [--prev quality/pass-02] [--critic quality/pass-03/g4.json] \
//        [--backends webgpu,webgl] [--frame 60] [--software]
// Writes <out>/gates.json, <out>/packet/{contact.png,burst.png,heatmap.png,metrics.md,checklist.md},
// and appends one line to <out>/../quality-log.jsonl. Exit code 1 if any automated gate fails.
import { createRequire } from 'node:module';
import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync, readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, dirname, resolve } from 'node:path';

const { chromium } = createRequire( join( process.cwd(), 'noop.js' ) )( 'playwright-core' );
const arg = ( k, d ) => { const i = process.argv.indexOf( `--${ k }` ); return i > 0 ? process.argv[ i + 1 ] : d; };
const flag = ( k ) => process.argv.includes( `--${ k }` );
const url = arg( 'url' ), out = resolve( arg( 'out', 'quality/pass' ) ), frame = Number( arg( 'frame', 60 ) );
const ceiling = JSON.parse( readFileSync( arg( 'ceiling', 'quality/ceiling.json' ), 'utf8' ) );
const backends = arg( 'backends', ceiling.webglParity ? 'webgpu,webgl' : 'webgpu' ).split( ',' );
const software = flag( 'software' ) || ceiling.determinism?.mode === 'software';
if ( ! url ) { console.error( 'missing --url' ); process.exit( 2 ); }
mkdirSync( join( out, 'packet' ), { recursive: true } );

function findChrome() {

	for ( const c of [ process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium' ] ) if ( c && existsSync( c ) ) return c;
	const pw = join( homedir(), 'Library/Caches/ms-playwright' );
	if ( existsSync( pw ) ) for ( const d of readdirSync( pw ).filter( ( n ) => n.startsWith( 'chromium-' ) ) ) { const p = join( pw, d, 'chrome-mac/Chromium.app/Contents/MacOS/Chromium' ); if ( existsSync( p ) ) return p; }
	return undefined;

}

const gpuArgs = software
	? [ '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--enable-unsafe-webgpu', '--use-webgpu-adapter=swiftshader' ]
	: [ '--enable-unsafe-webgpu', '--enable-gpu', '--ignore-gpu-blocklist', ...( process.platform === 'darwin' ? [ '--use-angle=metal' ] : [] ) ];

async function runOnce( browser, backend, soak ) {

	const ctx = await browser.newContext( { viewport: { width: 1280, height: 720 } } );
	const page = await ctx.newPage();
	const log = [];
	page.on( 'console', ( m ) => log.push( { type: m.type(), text: m.text() } ) );
	page.on( 'pageerror', ( e ) => log.push( { type: 'pageerror', text: e.message } ) );
	const u = new URL( url );
	u.searchParams.set( 'frame', frame ); if ( backend === 'webgl' ) u.searchParams.set( 'webgl', '' ); if ( ! soak ) u.searchParams.set( 'soak', '0' );
	if ( ceiling.allowNoToneMapping ) u.searchParams.set( 'unmapped', '' );
	await page.goto( u.href );
	await page.waitForFunction( () => window.__done === true, null, { timeout: 180000 } ).catch( () => log.push( { type: 'error', text: 'timeout: __done never set' } ) );
	const result = await page.evaluate( () => window.__result );
	return { page, ctx, log, result };

}

const dataToBuf = ( d ) => Buffer.from( d.split( ',' )[ 1 ], 'base64' );
const browser = await chromium.launch( { executablePath: findChrome(), headless: true, args: gpuArgs } );
const report = { time: new Date().toISOString(), url, frame, software, ceiling, backends: {} };

for ( const backend of backends ) {

	const A = await runOnce( browser, backend, true );
	const B = await runOnce( browser, backend, false );
	const r = A.result || {};
	const gatesJs = new URL( 'gates.js', url ).href;
	const cmp = r.frame && B.result?.frame ? await A.page.evaluate( async ( [ js, a, b ] ) => ( await import( js ) ).comparePixels( a, b ), [ gatesJs, r.frame, B.result.frame ] ) : null;
	let prevCmp = null;
	const prevDir = arg( 'prev' );
	const prevPng = prevDir && join( resolve( prevDir ), `frame-${ backend }.png` );
	if ( prevPng && existsSync( prevPng ) && r.frame ) {

		const prevUrl = 'data:image/png;base64,' + readFileSync( prevPng ).toString( 'base64' );
		prevCmp = await A.page.evaluate( async ( [ js, a, b ] ) => ( await import( js ) ).comparePixels( a, b ), [ gatesJs, prevUrl, r.frame ] );

	}

	// ---- gate evaluation
	const all = [ ...A.log, ...B.log ];
	// any console warning or error fails G0 (three's removals warn as "has been removed", not only "deprecated"); favicon-style 404s are ignored
	const bad = all.filter( ( m ) => ( m.type === 'pageerror' || m.type === 'error' || m.type === 'warning' ||
		/deprecat|has been removed|has been renamed|THREE\.TSL|WGSL|Shader Error|program not valid/i.test( m.text ) ) && ! /Failed to load resource.*404/.test( m.text ) );
	const G0 = { pass: ! r.error && bad.length === 0, problems: [ ...( r.error ? [ r.error ] : [] ), ...bad.map( ( m ) => `[${ m.type }] ${ m.text }` ) ] };

	const hw = ! software;
	const G1 = { pass: !! cmp && r.nonFinite === 0 && ( hw ? cmp.maxChannelDelta <= 1 || cmp.fractionWithin1 >= 0.999 : cmp.exact ), nonFinite: r.nonFinite, compare: cmp, rule: hw ? 'hardware: maxChannelDelta<=1 on >=99.9% of pixels' : 'software: exact SHA-256' };

	const m = r.metrics || {};
	const budget = ( k, v ) => ceiling[ k ] == null ? { value: v, budget: null, pass: true } : { value: v, budget: ceiling[ k ], pass: v != null && v <= ceiling[ k ] };
	const sw = ( k, v ) => software ? { value: v, budget: ceiling[ k ], pass: null, note: 'software rasterizer: timing not representative; re-run G2 on target hardware' } : null;
	const G2 = { metrics: {
		gpuMs: sw( 'gpuMs', m.gpuMs ) || ( m.gpuTimer ? budget( 'gpuMs', m.gpuMs ) : { value: null, budget: ceiling.gpuMs, pass: false, note: 'no GPU timer on this backend/browser: measure on target device' } ),
		cpuMs: sw( 'cpuMs', m.cpuMs ) || budget( 'cpuMs', m.cpuMs ), drawCalls: budget( 'drawCalls', m.drawCalls ), triangles: budget( 'triangles', m.triangles ),
		textures: budget( 'textures', m.textures ), geometries: budget( 'geometries', m.geometries ),
	}, soak: r.soak ? { netDelta: r.soak.netDelta, pass: r.soak.pass } : { pass: false, note: 'soak missing' } };
	const vals = Object.values( G2.metrics ).map( ( x ) => x.pass );
	G2.pass = vals.includes( false ) || ! G2.soak.pass ? false : vals.includes( null ) ? null : true;

	const G3 = { pass: !! r.audit?.pass, failures: r.audit?.failures || [ 'audit missing' ] };

	let G4 = { pass: null, note: 'run the blind critic on packet/ and pass --critic <json>' };
	const criticFile = arg( 'critic' );
	if ( criticFile && existsSync( criticFile ) ) {

		const c = JSON.parse( readFileSync( criticFile, 'utf8' ) );
		G4 = { pass: c.score >= ( ceiling.criticTarget ?? 0 ) && ! c.shimmer && ! c.zFighting && ! c.cascadeSwimming && ( c.checklistFailed || [] ).length === 0, critic: c };

	}

	const gates = { G0, G1, G2, G3, G4 };
	const firstOpen = [ 'G0', 'G1', 'G2', 'G3', 'G4' ].find( ( k ) => gates[ k ].pass !== true );
	const lowestFailing = firstOpen ? ( gates[ firstOpen ].pass === null ? `${ firstOpen } (pending: ${ firstOpen === 'G4' ? 'critic' : 'hardware run' })` : firstOpen ) : null;
	report.backends[ backend ] = { backend: r.backend, revision: r.revision, gates, lowestFailing, perceptualVsPrev: prevCmp ? { rmse: prevCmp.rmse, maxChannelDelta: prevCmp.maxChannelDelta, belowThreshold: ceiling.perceptualRmse != null ? prevCmp.rmse <= ceiling.perceptualRmse : null } : null, heatmap: r.heatmap ? { maxDelta: r.heatmap.maxDelta, meanDelta: r.heatmap.meanDelta } : null };

	// ---- artefacts
	if ( r.frame ) writeFileSync( join( out, `frame-${ backend }.png` ), dataToBuf( r.frame ) );
	if ( B.result?.frame ) writeFileSync( join( out, `frame-${ backend }-runB.png` ), dataToBuf( B.result.frame ) );
	if ( backend === backends[ 0 ] ) {

		if ( r.contact ) writeFileSync( join( out, 'packet/contact.png' ), dataToBuf( r.contact ) );
		if ( r.burst ) writeFileSync( join( out, 'packet/burst.png' ), dataToBuf( r.burst ) );
		if ( r.heatmap ) writeFileSync( join( out, 'packet/heatmap.png' ), dataToBuf( r.heatmap.url ) );

	}

	await A.ctx.close(); await B.ctx.close();

}

await browser.close();

// ---- packet text (what the blind critic may see: metrics + checklist, never code or reasoning)
const rows = [];
for ( const [ b, v ] of Object.entries( report.backends ) ) {

	for ( const [ k, x ] of Object.entries( v.gates.G2.metrics ) ) rows.push( `| ${ b } | ${ k } | ${ x.value ?? 'n/a' } | ${ x.budget ?? '—' } | ${ x.pass === null ? 'pending' : x.pass ? 'pass' : 'FAIL' } |` );
	rows.push( `| ${ b } | lifecycle net delta | ${ JSON.stringify( v.gates.G2.soak.netDelta ?? null ) } | 0 | ${ v.gates.G2.soak.pass ? 'pass' : 'FAIL' } |` );
	rows.push( `| ${ b } | G3 audit | ${ v.gates.G3.failures.length } issue(s) | 0 | ${ v.gates.G3.pass ? 'pass' : 'FAIL' } |` );
	if ( v.heatmap ) rows.push( `| ${ b } | temporal ΔY max / mean (8-bit) | ${ v.heatmap.maxDelta.toFixed( 1 ) } / ${ v.heatmap.meanDelta.toFixed( 3 ) } | — | info |` );

}

writeFileSync( join( out, 'packet/metrics.md' ), `| backend | metric | value | budget | result |\n|---|---|---|---|---|\n${ rows.join( '\n' ) }\n` );
writeFileSync( join( out, 'packet/checklist.md' ), ( ceiling.checklist || [] ).map( ( c ) => `- [ ] ${ c }` ).join( '\n' ) + `\n\nCritic score target: ${ ceiling.criticTarget ?? 'n/a' }\n` );
writeFileSync( join( out, 'gates.json' ), JSON.stringify( report, null, 2 ) );
appendFileSync( join( dirname( out ), 'quality-log.jsonl' ), JSON.stringify( { time: report.time, out, backends: Object.fromEntries( Object.entries( report.backends ).map( ( [ b, v ] ) => [ b, { lowestFailing: v.lowestFailing, pass: Object.fromEntries( Object.entries( v.gates ).map( ( [ k, g ] ) => [ k, g.pass ] ) ), metrics: Object.fromEntries( Object.entries( v.gates.G2.metrics ).map( ( [ k, x ] ) => [ k, x.value ] ) ), determinism: v.gates.G1.compare && { maxChannelDelta: v.gates.G1.compare.maxChannelDelta, fractionWithin1: v.gates.G1.compare.fractionWithin1 }, perceptualVsPrev: v.perceptualVsPrev } ] ) ) } ) + '\n' );

for ( const [ b, v ] of Object.entries( report.backends ) ) {

	console.log( `${ b } (${ v.backend }, r${ v.revision }): ${ Object.entries( v.gates ).map( ( [ k, g ] ) => `${ k}=${ g.pass === null ? 'pending' : g.pass ? 'pass' : 'FAIL' }` ).join( ' ' ) }  lowest failing: ${ v.lowestFailing ?? 'none' }` );
	for ( const k of [ 'G0', 'G1', 'G2', 'G3' ] ) if ( v.gates[ k ].pass === false ) console.log( `  ${ k }:`, JSON.stringify( k === 'G2' ? { metrics: v.gates.G2.metrics, soak: v.gates.G2.soak } : v.gates[ k ].problems || v.gates[ k ].failures || v.gates[ k ].compare || v.gates[ k ] ).slice( 0, 600 ) );

}

process.exitCode = Object.values( report.backends ).some( ( v ) => [ 'G0', 'G1', 'G2', 'G3' ].some( ( k ) => v.gates[ k ].pass === false ) ) ? 1 : 0;
