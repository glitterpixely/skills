// PROBE for the three.js quality loop: version pin, pipeline, loop style, bundler, and the r186 -> r187 migration surface.
// Usage: node probe.mjs --root <project> [--json probe.json]
// Static only (reads package.json and greps source). Exit 1 when a migration hit or an unpinned three range is found.
import { readFileSync, readdirSync, statSync, existsSync, writeFileSync } from 'node:fs';
import { join, resolve, relative, extname } from 'node:path';

const arg = ( k, d ) => { const i = process.argv.indexOf( `--${ k }` ); return i > 0 ? process.argv[ i + 1 ] : d; };
const root = resolve( arg( 'root', '.' ) );
const pkg = JSON.parse( readFileSync( join( root, 'package.json' ), 'utf8' ) );
const deps = { ...pkg.dependencies, ...pkg.devDependencies, ...pkg.peerDependencies };

const installed = ( name ) => { try { return JSON.parse( readFileSync( join( root, 'node_modules', name, 'package.json' ), 'utf8' ) ).version; } catch { return null; } };
const probe = {
	three: { range: deps.three ?? null, installed: installed( 'three' ), pinnedExact: /^\d+\.\d+\.\d+$/.test( deps.three ?? '' ) },
	typesThree: { range: deps[ '@types/three' ] ?? null, installed: installed( '@types/three' ) },
	r3f: !! deps[ '@react-three/fiber' ],
	pmndrsPostprocessing: deps.postprocessing ? { range: deps.postprocessing, installed: installed( 'postprocessing' ) } : null,
	bundler: [ 'vite', 'webpack', 'esbuild', 'rollup', 'parcel', 'next', '@sveltejs/kit', 'astro' ].filter( ( b ) => deps[ b ] ),
	typescript: !! deps.typescript || existsSync( join( root, 'tsconfig.json' ) ),
	signals: {},
	migration: [],
};

// ---- collect source files
const exts = new Set( [ '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx', '.vue', '.svelte', '.html' ] );
const skip = new Set( [ 'node_modules', 'dist', 'build', '.git', '.next', 'out', 'coverage', '.vite' ] );
const files = [];
( function walk( d ) {

	for ( const n of readdirSync( d ) ) {

		if ( skip.has( n ) || n.startsWith( '.' ) && n !== '.' ) continue;
		const p = join( d, n ), s = statSync( p );
		if ( s.isDirectory() ) walk( p ); else if ( exts.has( extname( n ) ) && s.size < 2e6 ) files.push( p );

	}

} )( root );

const hits = ( re ) => {

	const out = [];
	for ( const f of files ) {

		const lines = readFileSync( f, 'utf8' ).split( '\n' );
		lines.forEach( ( l, i ) => { if ( re.test( l ) ) out.push( `${ relative( root, f ) }:${ i + 1 }: ${ l.trim().slice( 0, 140 ) }` ); } );

	}

	return out;

};

// ---- pipeline and loop signals
const sig = probe.signals;
sig.webgpu = hits( /from ['"]three\/webgpu['"]|WebGPURenderer/ ).length > 0;
sig.webglRenderer = hits( /new\s+(THREE\.)?WebGLRenderer\b/ ).length > 0;
sig.effectComposer = hits( /\bEffectComposer\b/ ).length > 0;
sig.renderPipeline = hits( /\bRenderPipeline\b/ ).length > 0;
sig.tslPostProcessingLegacy = hits( /new\s+(THREE\.)?PostProcessing\s*\(/ ).length > 0;
sig.forceWebGL = hits( /forceWebGL\s*:\s*true/ ).length > 0;
sig.timer = hits( /new\s+(THREE\.)?Timer\s*\(/ ).length > 0;
sig.clock = hits( /new\s+(THREE\.)?Clock\s*\(/ ).length > 0;
sig.rAF = hits( /requestAnimationFrame|setAnimationLoop|useFrame\s*\(/ ).length > 0;
probe.pipeline = sig.webgpu ? ( sig.renderPipeline || sig.tslPostProcessingLegacy ? 'three/webgpu + RenderPipeline/TSL' : 'three/webgpu (no post)' ) : sig.webglRenderer ? ( sig.effectComposer ? 'WebGLRenderer + EffectComposer' : 'WebGLRenderer (no composer)' ) : 'unknown';
probe.loopStyle = sig.timer ? 'THREE.Timer' : sig.clock ? 'THREE.Clock (switch to Timer for manual stepping)' : sig.rAF ? 'rAF / setAnimationLoop' : 'unknown';

// ---- r186 -> r187 migration surface (official Migration Guide + release notes), plus general hygiene
const checks = [
	[ 'r187 #34585: CubeUV PMREM removed (PMREM is now a cube render target)', /CubeUVReflectionMapping|ENVMAP_TYPE_CUBE_UV|cubeUV|CUBEUV_/ ],
	[ 'r187 #34585: custom code assuming PMREM is a 2D WebGLRenderTarget / equirect readback of scene.environment', /fromEquirectangular[^\n]*\.texture\.image|readRenderTargetPixels[^\n]*(pmrem|envMap|environment)|ViewportTextureNode/i ],
	[ 'r187 #34517: removed r177 deprecations (ColorManagement.from/toWorkingColorSpace, TSL transformedNormalView/World, transformedClearcoatNormalView)', /\.(fromWorkingColorSpace|toWorkingColorSpace)\s*\(|transformedNormalView|transformedNormalWorld|transformedClearcoatNormalView/ ],
	[ 'r187 #33695: TSL implicit math coercion — review mixed int/float/vec math in Fn() bodies', /\b(int|uint|ivec[234]|uvec[234])\s*\(/ ],
	[ 'r187 #34807: struct storage buffers are always arrays (use .element(0).get(...))', /storage\s*\([^)]*\)\s*\.get\s*\(/ ],
	[ 'r187 #34622: light node registration is CustomLight.registerNode(Node)', /library\.addLight\s*\(/ ],
	[ 'r187 #34543: pixelationPass pixelSize must be a Number', /pixelationPass\s*\([^,]+,[^,]+,\s*(uniform|float)\s*\(/ ],
	[ 'r187 #34460: setViewport/setScissor no longer scale by pixel ratio when a render target is bound', /set(Viewport|Scissor)\s*\([^)]*(getPixelRatio|pixelRatio|devicePixelRatio)/ ],
	[ 'r187 #35039: iridescenceThicknessRange deprecated (use iridescenceThicknessMinimum/Maximum)', /iridescenceThicknessRange/ ],
	[ 'r187 reversed-depth fixes (#35264, #34606, #34892, #34801): delete manual reversed-depth workarounds', /reversedDepth|reverseDepth|GreaterDepth\b|1\.0\s*-\s*depth|1\s*-\s*depth\b|clearDepth\s*\(\s*0\s*\)/i ],
	[ 'hygiene: pass.fsQuad (most r187 passes keep the quad private as _fsQuad; SAOPass/SSRPass still expose fsQuad)', /\.fsQuad\b/ ],
	[ 'hygiene: r183 PostProcessing -> RenderPipeline', /new\s+(THREE\.)?PostProcessing\s*\(/ ],
	[ 'hygiene: r186 PCFSoftShadowMap removed', /PCFSoftShadowMap/ ],
	[ 'hygiene: r180 RGBELoader -> HDRLoader', /RGBELoader/ ],
	[ 'hygiene: r181 *Async render/clear/feature calls deprecated', /\b(renderAsync|clearAsync|hasFeatureAsync|initTextureAsync|detectSupportAsync)\s*\(/ ],
	[ 'hygiene: r183 THREE.Clock deprecated -> use THREE.Timer', /new\s+(THREE\.)?Clock\s*\(/ ],
	[ 'hygiene: legacy three/examples/jsm/ specifier -> use three/addons/', /from\s+['"]three\/examples\/jsm\// ],
	[ 'hygiene: invalid three/nodes import -> use three/tsl and three/webgpu', /from\s+['"]three\/nodes['"]/ ],
	[ 'hygiene: non-existent #include <output_fragment> -> use #include <opaque_fragment>', /#include\s*<output_fragment>/ ],
	[ 'hygiene: positionGeometry in positionNode drops skinning/morphs/instancing -> use positionLocal', /positionNode\s*=\s*[^;\n]*\bpositionGeometry\b/ ],
	[ 'hygiene: r169 TransformControls is not an Object3D -> use scene.add(tc.getHelper())', /\.add\s*\(\s*transformControls\s*\)/i ],
	[ 'hygiene: r168 removed PointerLockControls.getObject() / DragControls.getObjects() -> use .object / .objects', /\.\s*(getObject|getObjects|getRaycaster)\s*\(\s*\)/ ],
	[ 'hygiene: R3F <Canvas shadows> boolean selects removed PCFSoftShadowMap -> use shadows="percentage"', /<Canvas\b[^>]*\bshadows(?:\s*=\s*\{?\s*(?:true|['"]soft['"])\s*\}?|(?=[\s/>]))/ ],
	[ 'hygiene: R3F state.clock.getElapsedTime() zeroes delta -> use state.clock.elapsedTime', /clock\.getElapsedTime\s*\(\s*\)/ ],
];
for ( const [ title, re ] of checks ) { const h = hits( re ); if ( h.length ) probe.migration.push( { title, hits: h.slice( 0, 25 ), total: h.length } ); }

// ---- report
const warn = [];
if ( ! probe.three.pinnedExact ) warn.push( `three range "${ probe.three.range }" is not an exact pin (use "0.187.0")` );
if ( probe.three.installed && probe.three.installed !== '0.187.0' ) warn.push( `installed three is ${ probe.three.installed }, not 0.187.0` );
if ( probe.typesThree.range && ! /0\.18[6-9]|0\.19/.test( probe.typesThree.range ) ) warn.push( `@types/three ${ probe.typesThree.range } is older than 0.186` );
if ( probe.pmndrsPostprocessing ) warn.push( `pmndrs postprocessing ${ probe.pmndrsPostprocessing.installed ?? probe.pmndrsPostprocessing.range } present: 6.39.5 declares three <0.187.0` );

console.log( `three: range ${ probe.three.range } installed ${ probe.three.installed } | @types/three ${ probe.typesThree.range ?? '-' }` );
console.log( `pipeline: ${ probe.pipeline }${ sig.webgpu ? ` | forceWebGL in code: ${ sig.forceWebGL }` : '' } | loop: ${ probe.loopStyle } | R3F: ${ probe.r3f } | bundler: ${ probe.bundler.join( ',' ) || 'none found' } | TS: ${ probe.typescript }` );
for ( const w of warn ) console.log( 'WARN', w );
for ( const m of probe.migration ) { console.log( `HIT  ${ m.title } (${ m.total })` ); for ( const h of m.hits.slice( 0, 5 ) ) console.log( '     ', h ); }
console.log( probe.migration.length ? `${ probe.migration.length } migration/hygiene categories hit` : 'no migration hits' );
console.log( 'record manually: WebGL2 fallback (forceWebGL parity) in scope? target device?' );
const json = arg( 'json' ); if ( json ) writeFileSync( json, JSON.stringify( { ...probe, warnings: warn }, null, 2 ) );
process.exitCode = probe.migration.length || ! probe.three.pinnedExact ? 1 : 0;
