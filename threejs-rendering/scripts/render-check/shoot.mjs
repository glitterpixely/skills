// Headless-Chrome screenshotter for three.js render checks.
// Usage: node shoot.mjs "<url>" out.png [--timeout 90000] [--strict]
// Run from the project root. Needs: `npm i -D playwright-core` there (no browser download), and Google Chrome or a Playwright Chromium.
// The page must set window.__done = true when finished; console output and page errors are printed.
// Exits 1 on uncaught pageerror or timeout (and on console.error when --strict is passed).
import { existsSync, readdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { join } from 'node:path';

// resolve playwright-core from the PROJECT (cwd), not from this skill folder
const { chromium } = createRequire( join( process.cwd(), 'noop.js' ) )( 'playwright-core' );

const rawArgs = process.argv.slice( 2 );
const strict = rawArgs.includes( '--strict' );
const tIdx = rawArgs.indexOf( '--timeout' );
const timeout = tIdx >= 0 ? Number( rawArgs[ tIdx + 1 ] ) : 90000;
const positionals = rawArgs.filter( ( a, i ) => a !== '--strict' && a !== '--timeout' && ( tIdx < 0 || i !== tIdx + 1 ) );
const [ url, out ] = positionals;
if ( ! url || ! out ) { console.error( 'usage: node shoot.mjs <url> <out.png> [--timeout 90000] [--strict]' ); process.exit( 2 ); }

function findChrome() {

	const candidates = [
		process.env.CHROME_PATH,
		'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		'/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
		'C:/Program Files/Google/Chrome/Application/chrome.exe',
	].filter( Boolean );
	for ( const c of candidates ) if ( existsSync( c ) ) return c;
	const pw = join( homedir(), 'Library/Caches/ms-playwright' );
	if ( existsSync( pw ) ) for ( const d of readdirSync( pw ).filter( ( n ) => n.startsWith( 'chromium-' ) ) ) {

		const p = join( pw, d, 'chrome-mac/Chromium.app/Contents/MacOS/Chromium' );
		if ( existsSync( p ) ) return p;

	}

	return undefined; // let playwright-core try its default

}

const browser = await chromium.launch( {
	executablePath: findChrome(),
	headless: true,
	args: [ '--enable-unsafe-webgpu', '--enable-gpu', '--ignore-gpu-blocklist', ...( process.platform === 'darwin' ? [ '--use-angle=metal' ] : [] ) ],
} );
const page = await browser.newPage( { viewport: { width: 1280, height: 720 } } );
const msgs = [];
let failed = false;
page.on( 'console', ( m ) => {

	msgs.push( `[${ m.type() }] ${ m.text() }` );
	if ( strict && m.type() === 'error' ) failed = true;

} );
page.on( 'pageerror', ( e ) => { msgs.push( `[pageerror] ${ e.message }` ); failed = true; } );
await page.goto( url );
await page.waitForFunction( () => window.__done === true, null, { timeout } ).catch( () => { msgs.push( '[timeout] window.__done never set' ); failed = true; } );
await page.screenshot( { path: out } );
if ( msgs.length ) console.log( msgs.join( '\n' ) );
await browser.close();
process.exitCode = failed ? 1 : 0;
