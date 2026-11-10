// Usage: node fit-shadow.test.mjs [--root /path/to/project-with-three]
import { existsSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { fitDirectionalShadow, suggestShadowBias } from './fit-shadow.mjs';

const rootIdx = process.argv.indexOf( '--root' );
const root = resolve( rootIdx >= 0 ? process.argv[ rootIdx + 1 ] : process.cwd() );
const candidate = resolve( root, 'node_modules/three/build/three.module.js' );
const threeHref = existsSync( candidate )
	? pathToFileURL( candidate ).href
	: pathToFileURL( createRequire( resolve( root, 'noop.js' ) ).resolve( 'three' ) ).href;
const THREE = await import( threeHref );

let fails = 0;
const rnd = ( a, b ) => a + Math.random() * ( b - a );
for ( let t = 0; t < 2000; t ++ ) {

	const mode = t % 2 ? 'tight' : 'stable';
	const margin = t % 4 < 2 ? 0.25 : 0; // exercise zero-margin boundary on both modes
	const mapRes = t % 5 === 0 ? 64 : 2048; // coarse shadow maps amplify texel-snap rounding
	const box = new THREE.Box3( new THREE.Vector3( rnd( - 50, 0 ), rnd( - 5, 0 ), rnd( - 50, 0 ) ), new THREE.Vector3( rnd( 1, 50 ), rnd( 1, 20 ), rnd( 1, 50 ) ) );
	const light = new THREE.DirectionalLight( 0xffffff, 3 );
	light.position.set( rnd( - 100, 100 ), rnd( 5, 100 ), rnd( - 100, 100 ) );
	light.target.position.set( rnd( - 5, 5 ), 0, rnd( - 5, 5 ) );
	light.shadow.mapSize.set( mapRes, mapRes );
	const texel = fitDirectionalShadow( light, box, { mode, margin } );
	// light.shadow.matrix must ALREADY be updated on return without an extra caller updateMatrices():
	const m = light.shadow.matrix; // world -> shadow UV/depth in [0,1]
	const { min, max } = box;
	for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

		const p = new THREE.Vector3( x, y, z ).applyMatrix4( m );
		if ( p.x < 0 || p.x > 1 || p.y < 0 || p.y > 1 || p.z < 0 || p.z > 1 ) { fails ++; if ( fails < 5 ) console.log( 'OUT', mode, margin, mapRes, p ); }

	}

	const b = suggestShadowBias( light, texel );
	if ( ! ( b.normalBias > 0 && b.bias < 0 && b.bias >= - 0.0005 ) ) fails ++;

}

// stable mode: frustum width must not change as the light rotates
const box = new THREE.Box3( new THREE.Vector3( - 10, 0, - 10 ), new THREE.Vector3( 10, 5, 10 ) );
const L = new THREE.DirectionalLight(); L.shadow.mapSize.set( 2048, 2048 );
const widths = new Set();
for ( let a = 0; a < 6.28; a += 0.1 ) { L.position.set( Math.cos( a ) * 30, 20, Math.sin( a ) * 30 ); widths.add( fitDirectionalShadow( L, box, { mode: 'stable', margin: 0 } ).toFixed( 9 ) ); }
if ( widths.size !== 1 ) { console.log( 'FAIL stable width varied:', widths.size ); fails ++; }

// negative self-check: deliberately negative margin MUST clip corners (proves test can fail)
fitDirectionalShadow( L, box, { mode: 'tight', margin: - 5 } );
let negOut = 0;
for ( const x of [ - 10, 10 ] ) for ( const y of [ 0, 5 ] ) for ( const z of [ - 10, 10 ] ) {

	const p = new THREE.Vector3( x, y, z ).applyMatrix4( L.shadow.matrix );
	if ( p.x < 0 || p.x > 1 || p.y < 0 || p.y > 1 || p.z < 0 || p.z > 1 ) negOut ++;

}

if ( negOut === 0 ) { console.log( 'FAIL negative self-check did not detect clipped corners' ); fails ++; }

console.log( 'stable widths distinct:', widths.size, '| negative-margin clipped corners:', negOut );
console.log( fails ? `FAIL ${ fails }` : 'PASS: all corners of 2000 random boxes (including margin=0, 64px maps) inside fitted shadow frustum' );
process.exitCode = fails ? 1 : 0;
