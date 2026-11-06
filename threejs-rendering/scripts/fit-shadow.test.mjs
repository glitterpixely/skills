import * as THREE from 'three';
import { fitDirectionalShadow, suggestShadowBias } from './fit-shadow.mjs';

let fails = 0;
const rnd = ( a, b ) => a + Math.random() * ( b - a );
for ( let t = 0; t < 2000; t ++ ) {

	const mode = t % 2 ? 'tight' : 'stable';
	const box = new THREE.Box3( new THREE.Vector3( rnd( - 50, 0 ), rnd( - 5, 0 ), rnd( - 50, 0 ) ), new THREE.Vector3( rnd( 1, 50 ), rnd( 1, 20 ), rnd( 1, 50 ) ) );
	const light = new THREE.DirectionalLight( 0xffffff, 3 );
	light.position.set( rnd( - 100, 100 ), rnd( 5, 100 ), rnd( - 100, 100 ) );
	light.target.position.set( rnd( - 5, 5 ), 0, rnd( - 5, 5 ) );
	light.shadow.mapSize.set( 2048, 2048 );
	const texel = fitDirectionalShadow( light, box, { mode } );
	// the renderer recomputes matrices each frame: emulate that and project every corner into shadow NDC
	light.shadow.updateMatrices( light );
	const m = light.shadow.matrix; // world -> shadow UV/depth in [0,1]
	const { min, max } = box;
	for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

		const p = new THREE.Vector3( x, y, z ).applyMatrix4( m );
		if ( p.x < 0 || p.x > 1 || p.y < 0 || p.y > 1 || p.z < 0 || p.z > 1 ) { fails ++; if ( fails < 5 ) console.log( 'OUT', mode, p ); }

	}

	const b = suggestShadowBias( light, texel );
	if ( ! ( b.normalBias > 0 && b.bias < 0 && b.bias >= - 0.0005 ) ) fails ++;

}

// stable mode: frustum width must not change as the light rotates
const box = new THREE.Box3( new THREE.Vector3( - 10, 0, - 10 ), new THREE.Vector3( 10, 5, 10 ) );
const L = new THREE.DirectionalLight(); L.shadow.mapSize.set( 2048, 2048 );
const widths = new Set();
for ( let a = 0; a < 6.28; a += 0.1 ) { L.position.set( Math.cos( a ) * 30, 20, Math.sin( a ) * 30 ); widths.add( fitDirectionalShadow( L, box, { mode: 'stable' } ).toFixed( 9 ) ); }
console.log( 'stable widths distinct:', widths.size );
console.log( fails ? `FAIL ${fails}` : 'PASS: all corners of 2000 random boxes inside fitted shadow frustum' );
