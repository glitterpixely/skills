// Headless-Chrome screenshotter for three.js render checks.
// Usage: node shoot.mjs "<url>" out.png [--timeout 90000]
// Run from the project root. Needs: `npm i -D playwright-core` there (no browser download), and Google Chrome or a Playwright Chromium.
// The page must set window.__done = true when finished; console output and page errors are printed.
import { existsSync, readdirSync } from 'node:fs';
import { createRequire } from 'node:module';
import { homedir } from 'node:os';
import { join } from 'node:path';

// resolve playwright-core from the PROJECT (cwd), not from this skill folder
const { chromium } = createRequire( join( process.cwd(), 'noop.js' ) )( 'playwright-core' );

const [ url, out ] = process.argv.slice( 2 );
const tIdx = process.argv.indexOf( '--timeout' );
const timeout = tIdx > 0 ? Number( process.argv[ tIdx + 1 ] ) : 90000;
if ( ! url || ! out ) { console.error( 'usage: node shoot.mjs <url> <out.png>' ); process.exit( 2 ); }

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
page.on( 'console', ( m ) => msgs.push( `[${ m.type() }] ${ m.text() }` ) );
page.on( 'pageerror', ( e ) => msgs.push( `[pageerror] ${ e.message }` ) );
await page.goto( url );
await page.waitForFunction( () => window.__done === true, null, { timeout } ).catch( () => msgs.push( '[timeout] window.__done never set' ) );
await page.screenshot( { path: out } );
console.log( msgs.join( '\n' ) );
await browser.close();
