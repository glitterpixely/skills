// Physical-camera and photometry helpers for three.js scenes (units: metres, millimetres where noted).
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
	];
	let fail = 0;
	for ( const [ name, got, want, tol ] of checks ) { const ok = near( got, want, tol ); if ( ! ok ) fail ++; console.log( ok ? 'ok  ' : 'FAIL', name, got ); }
	const ramp = blurRampMetres( { f: 50, N: 1.8, focus: 2, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } );
	const atRamp = cocPixels( { f: 50, N: 1.8, focus: 2, subject: 2 + ramp, filmHeight: 35 / ( 16 / 9 ), heightPx: 1080 } );
	console.log( near( atRamp, 0.8 * 39.07, 0.1 ) ? 'ok  ' : 'FAIL', 'blur ramp metres', ramp.toFixed( 3 ), 'CoC there', atRamp.toFixed( 2 ) );
	if ( ! near( atRamp, 0.8 * 39.07, 0.1 ) ) fail ++;
	console.log( fail ? `FAILURES ${ fail }` : 'ALL PASS' );
	process.exitCode = fail ? 1 : 0;

}
