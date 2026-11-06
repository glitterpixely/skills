// Physical-camera, photometry, tone-mapping, and IBL helpers for three.js r187 scenes
// (units: metres, millimetres where noted).
// Run `node physical.mjs` to execute the self-test.

/** toneMappingExposure for a scene metered at EV100 (Lagarde & de Rousiers 2014, saturation-based). */
export const exposureFromEV100 = ( ev100 ) => 1 / ( 1.2 * 2 ** ev100 );

/** Point light: candela from lumens (isotropic, P = 4πI). Same as `pointLight.power = lm`. */
export const pointCandelaFromLumens = ( lm ) => lm / ( 4 * Math.PI );

/** Spot light: candela from lumens, three.js convention P = πI (independent of cone angle). */
export const spotCandelaFromLumens = ( lm ) => lm / Math.PI;

/** RectAreaLight: nits from lumens, P = I·w·h·π. */
export const rectNitsFromLumens = ( lm, w, h ) => lm / ( w * h * Math.PI );

/** Dielectric normal-incidence reflectance from IOR (against air). */
export const f0FromIor = ( n ) => ( ( n - 1 ) / ( n + 1 ) ) ** 2;

/** KHR_materials_dispersion / MeshPhysicalMaterial.dispersion from an Abbe number. */
export const dispersionFromAbbe = ( abbe ) => 20 / abbe;

/** three.js clamps MeshPhysicalMaterial.ior to [1, 2.333]. */
export const clampIor = ( n ) => Math.min( Math.max( n, 1 ), 2.333 );

/** Exact IEC 61966-2-1 linear -> sRGB transfer for a scalar channel in [0, 1]. */
export const linearToSrgbScalar = ( x ) => {

	const c = Math.min( 1, Math.max( 0, x ) );
	return c <= 0.0031308 ? 12.92 * c : 1.055 * Math.pow( c, 1 / 2.4 ) - 0.055;

};

/**
 * Exact Three.js r187 ACESFilmicToneMapping transfer for an achromatic linear grey `c`.
 * Note: Three.js pre-divides by 0.6 (`color = color * exposure / 0.6`, +0.737 EV) before RRT+ODT.
 */
export function acesFilmicToneMapScalar( c, exposure = 1.0 ) {

	const x = ( c * exposure ) / 0.6;
	const y = ( x * ( x + 0.0245786 ) - 0.000090537 ) / ( x * ( 0.983729 * x + 0.4329510 ) + 0.238081 );
	return Math.min( 1, Math.max( 0, y ) );

}

/**
 * Exact Three.js r187 AgXToneMapping transfer for an achromatic linear grey `c`.
 * Uses [-12.47393, +4.026069] EV window around 0.18 linear mid-grey and the 6th-order contrast polynomial.
 */
export function agxToneMapScalar( c, exposure = 1.0 ) {

	const AgxMinEv = - 12.47393;
	const AgxMaxEv = 4.026069;
	let x = Math.max( c * exposure, 1e-10 );
	x = ( Math.log2( x ) - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	x = Math.min( 1, Math.max( 0, x ) );
	const x2 = x * x;
	const x4 = x2 * x2;
	const contrast = 15.5 * x4 * x2 - 40.14 * x4 * x + 31.96 * x4 - 6.868 * x2 * x + 0.4298 * x2 + 0.1191 * x - 0.00232;
	return Math.min( 1, Math.max( 0, Math.pow( Math.max( 0, contrast ), 2.2 ) ) );

}

/**
 * Exact Three.js r187 NeutralToneMapping (Khronos PBR Neutral) transfer for an achromatic linear grey `c`.
 * Subtracts a 0.04 toe offset for c * exposure >= 0.08 and compresses highlights above StartCompression = 0.76.
 */
export function neutralToneMapScalar( c, exposure = 1.0 ) {

	const StartCompression = 0.8 - 0.04;
	let x = c * exposure;
	const offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	x -= offset;
	if ( x < StartCompression ) return Math.max( 0, x );
	const d = 1 - StartCompression;
	return 1 - ( d * d ) / ( x + d - StartCompression );

}

/**
 * Solves for `toneMappingExposure` so `toneMapFn(inputLinear, exposure)` equals `targetLinearOut`.
 */
export function solveExposureForToneMap( toneMapFn, inputLinear, targetLinearOut ) {

	let lo = 1e-4, hi = 1e4;
	for ( let i = 0; i < 80; i ++ ) {

		const mid = 0.5 * ( lo + hi );
		if ( toneMapFn( inputLinear, mid ) < targetLinearOut ) lo = mid; else hi = mid;

	}

	return 0.5 * ( lo + hi );

}

/**
 * Extracts the world-space unit vector [x, y, z] toward the brightest solid-angle-weighted
 * texel in an equirectangular HDR/EXR image (`{ width, height, data }`), accounting for
 * `scene.environmentRotation.y` (`envRotationY`, radians) and loader `flipY`
 * (`HDRLoader` sets `flipY = true`; `EXRLoader` sets `flipY = false`).
 */
export function sunDirectionFromEquirect( image, envRotationY = 0, flipY = true ) {

	const { width, height, data } = image;
	let best = - 1, bestIdx = 0;
	for ( let y = 0; y < height; y ++ ) {

		const v = flipY ? 1 - ( y + 0.5 ) / height : ( y + 0.5 ) / height;
		const theta = ( 1 - v ) * Math.PI;
		const sinT = Math.sin( theta );
		for ( let x = 0; x < width; x ++ ) {

			const i = ( y * width + x ) * 4;
			const lum = ( 0.2126 * data[ i ] + 0.7152 * data[ i + 1 ] + 0.0722 * data[ i + 2 ] ) * sinT;
			if ( lum > best ) { best = lum; bestIdx = y * width + x; }

		}

	}

	const ix = bestIdx % width;
	const iy = ( bestIdx - ix ) / width;
	const u = ( ix + 0.5 ) / width;
	const v = flipY ? 1 - ( iy + 0.5 ) / height : ( iy + 0.5 ) / height;
	const theta = ( 1 - v ) * Math.PI;
	// Three.js `materialEnvRotation` & `backgroundRotation` sample at R_y(envRotationY)^T * D_world,
	// so a feature at unrotated azimuth phi0 appears in world space at phi = phi0 - envRotationY.
	const phi = ( u - 0.5 ) * 2 * Math.PI - envRotationY;
	const sx = Math.sin( theta ) * Math.cos( phi );
	const sy = Math.cos( theta );
	const sz = Math.sin( theta ) * Math.sin( phi );
	const len = Math.hypot( sx, sy, sz ) || 1;
	return [ sx / len, sy / len, sz / len ];

}

/**
 * Thin-lens circle of confusion in pixels.
 * f, filmHeight in mm (camera.getFocalLength(), camera.getFilmHeight()); distances in metres.
 */
export function cocPixels( { f, N, focus, subject, filmHeight, heightPx } ) {

	const S1 = focus * 1000, S2 = subject * 1000;
	const c = ( f * f * Math.abs( S2 - S1 ) ) / ( N * S2 * ( S1 - f ) );
	return ( c / filmHeight ) * heightPx;

}

/** Far-field (subject at infinity) CoC in pixels: the largest background blur. */
export function cocInfinityPixels( { f, N, focus, filmHeight, heightPx } ) {

	const S1 = focus * 1000;
	return ( ( f * f ) / ( N * ( S1 - f ) ) / filmHeight ) * heightPx;

}

/**
 * Distance behind focus (metres) where blur reaches `fraction` of the far-field maximum.
 * Use as the `focalLength` (blur-ramp) argument of TSL dof() or pmndrs `focusRange`.
 */
export function blurRampMetres( { f, N, focus, filmHeight, heightPx, fraction = 0.8 } ) {

	const target = fraction * cocInfinityPixels( { f, N, focus, filmHeight, heightPx } );
	let lo = focus, hi = focus * 1e4;
	for ( let i = 0; i < 80; i ++ ) {

		const mid = ( lo + hi ) / 2;
		if ( cocPixels( { f, N, focus, subject: mid, filmHeight, heightPx } ) < target ) lo = mid; else hi = mid;

	}

	return ( lo + hi ) / 2 - focus;

}

/** Hyperfocal distance in metres for acceptable CoC c (mm). */
export const hyperfocalMetres = ( f, N, c = 0.03 ) => ( ( f * f ) / ( N * c ) + f ) / 1000;

// ---------------------------------------------------------------- self-test
if ( import.meta.url === `file://${ process.argv[ 1 ] }` ) {

	const near = ( a, b, tol ) => Math.abs( a - b ) <= tol;
	const aces018 = acesFilmicToneMapScalar( 0.18, 1.0 );
	const agx018 = agxToneMapScalar( 0.18, 1.0 );
	const neutral018 = neutralToneMapScalar( 0.18, 1.0 );
	const agxExpMatchAces018 = solveExposureForToneMap( agxToneMapScalar, 0.18, aces018 );
	const agxExpMatchAces050 = solveExposureForToneMap( agxToneMapScalar, 0.50, acesFilmicToneMapScalar( 0.50, 1.0 ) );
	const neutralExpMatchAces018 = solveExposureForToneMap( neutralToneMapScalar, 0.18, aces018 );

	// Synthetic 64x32 HDR image with bright sun at (ix=18, iy=10) rotated by rotY = 0.85 rad
	const w = 64, h = 32, ix = 18, iy = 10, rotY = 0.85;
	const data = new Float32Array( w * h * 4 );
	data[ ( iy * w + ix ) * 4 + 1 ] = 100;
	const [ wx, wy, wz ] = sunDirectionFromEquirect( { width: w, height: h, data }, rotY, true );
	// Apply R_y(rotY)^T (which is R_y(-rotY)) to world direction [wx, wy, wz] and recover equirectUV:
	const tx = wx * Math.cos( - rotY ) + wz * Math.sin( - rotY );
	const ty = wy;
	const tz = - wx * Math.sin( - rotY ) + wz * Math.cos( - rotY );
	const uRec = Math.atan2( tz, tx ) / ( 2 * Math.PI ) + 0.5;
	const vRec = Math.asin( Math.max( - 1, Math.min( 1, ty ) ) ) / Math.PI + 0.5;

	const checks = [
		[ 'EV15 exposure', exposureFromEV100( 15 ), 2.543e-5, 1e-8 ],
		[ '800 lm point -> cd', pointCandelaFromLumens( 800 ), 63.66, 0.01 ],
		[ 'F0 ior 1.5', f0FromIor( 1.5 ), 0.04, 1e-6 ],
		[ 'F0 water', f0FromIor( 1.333 ), 0.0204, 1e-4 ],
		[ 'dispersion BK7', dispersionFromAbbe( 64 ), 0.3125, 1e-6 ],
		[ 'CoC inf 50mm f1.8 @2m 1080p', cocInfinityPixels( { f: 50, N: 1.8, focus: 2, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } ), 39.07, 0.05 ],
		[ 'CoC @4m', cocPixels( { f: 50, N: 1.8, focus: 2, subject: 4, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } ), 19.5, 0.05 ],
		[ 'hyperfocal', hyperfocalMetres( 50, 1.8 ), 46.35, 0.01 ],
		[ 'ior clamp diamond', clampIor( 2.417 ), 2.333, 0 ],
		[ 'ACESFilmic(0.18) linear', aces018, 0.213105, 1e-5 ],
		[ 'AgX(0.18) linear', agx018, 0.214519, 1e-5 ],
		[ 'Neutral(0.18) linear', neutral018, 0.140000, 1e-6 ],
		[ 'AgX EV offset vs ACES @0.18', Math.log2( agxExpMatchAces018 ), - 0.012, 0.002 ],
		[ 'AgX EV offset vs ACES @0.50', Math.log2( agxExpMatchAces050 ), 0.802, 0.005 ],
		[ 'Neutral EV offset vs ACES @0.18', Math.log2( neutralExpMatchAces018 ), 0.492, 0.005 ],
		[ 'sunDirectionFromEquirect u round-trip', uRec, ( ix + 0.5 ) / w, 1e-6 ],
		[ 'sunDirectionFromEquirect v round-trip', vRec, 1 - ( iy + 0.5 ) / h, 1e-6 ],
	];
	let fail = 0;
	for ( const [ name, got, want, tol ] of checks ) {

		const ok = near( got, want, tol );
		if ( ! ok ) fail ++;
		console.log( ok ? 'ok  ' : 'FAIL', name, got );

	}

	const ramp = blurRampMetres( { f: 50, N: 1.8, focus: 2, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } );
	const atRamp = cocPixels( { f: 50, N: 1.8, focus: 2, subject: 2 + ramp, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } );
	console.log( near( atRamp, 0.8 * 39.07, 0.1 ) ? 'ok  ' : 'FAIL', 'blur ramp metres', ramp.toFixed( 3 ), 'CoC there', atRamp.toFixed( 2 ) );
	if ( ! near( atRamp, 0.8 * 39.07, 0.1 ) ) fail ++;
	console.log( fail ? `FAILURES ${ fail }` : 'ALL PASS' );
	process.exitCode = fail ? 1 : 0;

}
