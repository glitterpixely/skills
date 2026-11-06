// Browser-side gate helpers for the three.js quality loop (see references/11-quality-loop.md).
// Import from a gate harness page. Works with WebGLRenderer and WebGPURenderer (three r187).

/** G1: replace Math.random with a seeded PRNG (mulberry32). Returns a restore function. */
export function installSeededRandom( seed = 0x9e3779b9 ) {

	const original = Math.random;
	let a = seed >>> 0;
	Math.random = () => {

		a = ( a + 0x6d2b79f5 ) >>> 0;
		let t = a;
		t = Math.imul( t ^ ( t >>> 15 ), t | 1 );
		t ^= t + Math.imul( t ^ ( t >>> 7 ), t | 61 );
		return ( ( t ^ ( t >>> 14 ) ) >>> 0 ) / 4294967296;

	};

	return () => { Math.random = original; };

}

/** G1: wait for everything that can make frame 0 differ between runs. */
export async function awaitReady( { renderer, scene, camera, managers = [], extra = [] } ) {

	await Promise.all( managers.map( ( m ) => new Promise( ( resolve ) => {

		if ( m.__done ) return resolve();
		const prev = m.onLoad; m.onLoad = () => { m.__done = true; prev && prev(); resolve(); };
		if ( m.itemsLoaded !== undefined && m.itemsTotal !== undefined && m.itemsLoaded >= m.itemsTotal ) resolve();

	} ) ) );
	await Promise.all( extra );
	if ( document.fonts ) await document.fonts.ready;
	if ( renderer.compileAsync ) await renderer.compileAsync( scene, camera );

}

/** G1: fixed-step clock. Call step() instead of rAF-driven updates; `onTick(dt, elapsed)` animates the app. */
export function createFixedStepper( { THREE, dtMs = 1000 / 60, onTick = () => {} } ) {

	const timer = new THREE.Timer();
	// r187 Timer.update( timestamp ) subtracts `_startTime = performance.now()` captured in the constructor, so the first
	// synthetic step yields a run-dependent delta (tested: two identical runs captured different animation frames).
	// Zero the private start time so update( t ) means "t ms since start".
	timer._startTime = 0;
	let t = 0;
	return {
		timer,
		get elapsedMs() { return t; },
		tick() { t += dtMs; timer.update( t ); onTick( timer.getDelta(), timer.getElapsed() ); },
	};

}

/** G2: snapshot renderer.info in a renderer-agnostic shape. */
export function infoSnapshot( renderer ) {

	const i = renderer.info;
	const programs = i.memory?.programs ?? ( Array.isArray( i.programs ) ? i.programs.length : null );
	return {
		drawCalls: i.render.drawCalls ?? i.render.calls,
		triangles: i.render.triangles,
		geometries: i.memory.geometries,
		textures: i.memory.textures,
		programs,
	};

}

/** G2: GPU time of one frame in ms, or null when the backend exposes no timer. */
export async function gpuFrameTimeMs( renderer, renderFrame ) {

	if ( renderer.isWebGPURenderer ) {

		if ( ! renderer.backend.trackTimestamp ) return null; // construct with { trackTimestamp: true }
		renderFrame();
		await renderer.resolveTimestampsAsync( 'render' );
		return renderer.info.render.timestamp || null;

	}

	const gl = renderer.getContext();
	const ext = gl.getExtension( 'EXT_disjoint_timer_query_webgl2' );
	if ( ! ext ) { renderFrame(); return null; }
	const q = gl.createQuery();
	gl.beginQuery( ext.TIME_ELAPSED_EXT, q );
	renderFrame();
	gl.endQuery( ext.TIME_ELAPSED_EXT );
	for ( let i = 0; i < 120; i ++ ) {

		await new Promise( ( r ) => requestAnimationFrame( r ) );
		if ( gl.getQueryParameter( q, gl.QUERY_RESULT_AVAILABLE ) && ! gl.getParameter( ext.GPU_DISJOINT_EXT ) ) {

			const ns = gl.getQueryParameter( q, gl.QUERY_RESULT ); gl.deleteQuery( q ); return ns / 1e6;

		}

	}

	return null;

}

/** G2: CPU submission time (ms) of one frame. */
export function cpuFrameTimeMs( renderFrame ) {

	const t0 = performance.now(); renderFrame(); return performance.now() - t0;

}

/** G1: render the raw scene into a HalfFloat target and count non-finite values (NaN/Inf). */
export async function countNonFinite( { THREE, renderer, scene, camera, size = 256 } ) {

	const rt = new THREE.RenderTarget( size, size, { type: THREE.HalfFloatType } );
	const prev = renderer.getRenderTarget();
	renderer.setRenderTarget( rt ); renderer.render( scene, camera ); renderer.setRenderTarget( prev );
	const buf = renderer.readRenderTargetPixelsAsync
		? await renderer.readRenderTargetPixelsAsync( rt, 0, 0, size, size )
		: ( () => { const b = new Uint16Array( size * size * 4 ); renderer.readRenderTargetPixels( rt, 0, 0, size, size, b ); return b; } )();
	rt.dispose();
	let bad = 0;
	for ( let k = 0; k < buf.length; k ++ ) if ( ( buf[ k ] & 0x7c00 ) === 0x7c00 ) bad ++; // half-float exponent all ones = Inf/NaN
	return bad;

}

/** G3: automated colour/tone/shadow audit. Returns { pass, failures[] }. */
export function auditRendering( { THREE, renderer, scene, allowNoToneMapping = false } ) {

	const failures = [];
	if ( renderer.outputColorSpace !== THREE.SRGBColorSpace ) failures.push( `outputColorSpace is ${ renderer.outputColorSpace }` );
	if ( ! allowNoToneMapping && renderer.toneMapping === THREE.NoToneMapping ) failures.push( 'toneMapping is NoToneMapping' );
	const colorSlots = [ 'map', 'emissiveMap', 'sheenColorMap', 'specularColorMap' ];
	const dataSlots = [ 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap', 'clearcoatNormalMap', 'clearcoatRoughnessMap', 'clearcoatMap', 'transmissionMap', 'thicknessMap', 'displacementMap', 'anisotropyMap', 'iridescenceMap', 'iridescenceThicknessMap', 'specularIntensityMap', 'diffuseRoughnessMap', 'gradientMap' ];
	scene.traverse( ( o ) => {

		if ( o.material ) for ( const m of [].concat( o.material ) ) {

			for ( const s of colorSlots ) if ( m[ s ] && m[ s ].colorSpace !== THREE.SRGBColorSpace ) failures.push( `${ m.name || m.type }.${ s } colorSpace=${ m[ s ].colorSpace || 'none' }` );
			for ( const s of dataSlots ) if ( m[ s ] && m[ s ].colorSpace !== THREE.NoColorSpace && m[ s ].colorSpace !== '' ) failures.push( `${ m.name || m.type }.${ s } colorSpace=${ m[ s ].colorSpace }` );

		}

		if ( o.isLight && o.castShadow && o.shadow ) {

			if ( ! renderer.shadowMap.enabled ) failures.push( `${ o.type } casts shadows but renderer.shadowMap.enabled=false` );
			else if ( ! o.shadow.map ) failures.push( `${ o.type } shadow map not allocated after rendering` );

		}

	} );
	return { pass: failures.length === 0, failures };

}

/**
 * G1/G4: grab the canvas as a PNG data URL after the GPU has finished the submitted frame.
 * Waiting on the queue is a precaution so the capture never depends on present timing.
 */
export async function captureCanvas( renderer ) {

	const device = renderer.backend?.device;
	if ( device?.queue?.onSubmittedWorkDone ) await device.queue.onSubmittedWorkDone();
	else renderer.getContext?.()?.finish?.();
	return renderer.domElement.toDataURL( 'image/png' );

}

async function loadImage( src ) { const img = new Image(); img.src = src; await img.decode(); return img; }

/** G4: side-by-side sheet of data-URL images with labels. */
export async function composeSheet( urls, labels = [], scale = 0.5 ) {

	const imgs = await Promise.all( urls.map( loadImage ) );
	const w = Math.round( imgs[ 0 ].width * scale ), h = Math.round( imgs[ 0 ].height * scale );
	const c = document.createElement( 'canvas' ); c.width = w * imgs.length; c.height = h + 24;
	const g = c.getContext( '2d' ); g.fillStyle = '#111'; g.fillRect( 0, 0, c.width, c.height );
	imgs.forEach( ( im, i ) => { g.drawImage( im, i * w, 24, w, h ); g.fillStyle = '#ddd'; g.font = '14px sans-serif'; g.fillText( labels[ i ] || `#${ i }`, i * w + 6, 17 ); } );
	return c.toDataURL( 'image/png' );

}

async function pixels( url ) {

	const im = await loadImage( url );
	const c = document.createElement( 'canvas' ); c.width = im.width; c.height = im.height;
	const g = c.getContext( '2d', { willReadFrequently: true } ); g.drawImage( im, 0, 0 );
	return g.getImageData( 0, 0, im.width, im.height );

}

/** G4: temporal luminance-delta heatmap across a frame burst (max |ΔY| per pixel, ×gain). */
export async function temporalHeatmap( urls, gain = 8 ) {

	const frames = await Promise.all( urls.map( pixels ) );
	const { width, height } = frames[ 0 ];
	const out = new ImageData( width, height );
	let maxDelta = 0, sum = 0;
	const Y = ( d, i ) => 0.2126 * d[ i ] + 0.7152 * d[ i + 1 ] + 0.0722 * d[ i + 2 ];
	for ( let i = 0; i < out.data.length; i += 4 ) {

		let m = 0;
		for ( let f = 1; f < frames.length; f ++ ) m = Math.max( m, Math.abs( Y( frames[ f ].data, i ) - Y( frames[ f - 1 ].data, i ) ) );
		maxDelta = Math.max( maxDelta, m ); sum += m;
		const v = Math.min( 255, m * gain );
		out.data[ i ] = v; out.data[ i + 1 ] = v * 0.4; out.data[ i + 2 ] = 255 - v; out.data[ i + 3 ] = 255;

	}

	const c = document.createElement( 'canvas' ); c.width = width; c.height = height;
	c.getContext( '2d' ).putImageData( out, 0, 0 );
	return { url: c.toDataURL( 'image/png' ), maxDelta, meanDelta: sum / ( width * height ) };

}

/** G1/G4: compare two PNG data URLs: SHA-256 of RGBA, max channel delta, share of pixels within ±1, RMSE. */
export async function comparePixels( urlA, urlB ) {

	const [ a, b ] = await Promise.all( [ pixels( urlA ), pixels( urlB ) ] );
	if ( a.width !== b.width || a.height !== b.height ) return { sizeMismatch: true };
	const hash = async ( d ) => [ ...new Uint8Array( await crypto.subtle.digest( 'SHA-256', d.data ) ) ].map( ( x ) => x.toString( 16 ).padStart( 2, '0' ) ).join( '' );
	let maxChannelDelta = 0, within1 = 0, se = 0;
	const n = a.width * a.height;
	for ( let i = 0; i < a.data.length; i += 4 ) {

		let pxMax = 0;
		for ( let c = 0; c < 3; c ++ ) { const d = Math.abs( a.data[ i + c ] - b.data[ i + c ] ); pxMax = Math.max( pxMax, d ); se += d * d; }
		maxChannelDelta = Math.max( maxChannelDelta, pxMax ); if ( pxMax <= 1 ) within1 ++;

	}

	const [ ha, hb ] = await Promise.all( [ hash( a ), hash( b ) ] );
	return { shaA: ha, shaB: hb, exact: ha === hb, maxChannelDelta, fractionWithin1: within1 / n, rmse: Math.sqrt( se / ( n * 3 ) ) };

}

/** G2: lifecycle soak. mount(renderer) -> { scene, camera, render(), dispose() }. Returns per-phase info and net deltas. */
export async function lifecycleSoak( { renderer, mount, frames = 120 } ) {

	const settle = () => new Promise( ( r ) => requestAnimationFrame( r ) );
	const mem = () => infoSnapshot( renderer );
	const runOnce = async () => {

		const app = await mount( renderer );
		for ( let i = 0; i < frames; i ++ ) { app.render(); if ( i % 10 === 0 ) await settle(); }
		const live = mem();
		app.dispose();
		await settle(); await settle();
		return { live, afterDispose: mem() };

	};

	const first = await runOnce();
	const second = await runOnce();
	const delta = {};
	for ( const k of [ 'geometries', 'textures', 'programs' ] ) delta[ k ] = ( second.afterDispose[ k ] ?? 0 ) - ( first.afterDispose[ k ] ?? 0 );
	return { first, second, netDelta: delta, pass: Object.values( delta ).every( ( v ) => v === 0 ) };

}
