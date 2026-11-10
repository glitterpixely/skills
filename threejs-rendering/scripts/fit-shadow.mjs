/**
 * Zero-import DirectionalLight orthographic shadow fitter for Three.js (works in Node, bundlers, and browser importmaps).
 * Fit a DirectionalLight's orthographic shadow camera to a world-space Box3.
 * mode 'tight'  : light-space AABB of the 8 box corners (best texel density; use for static scenes).
 * mode 'stable' : bounding-sphere square (size invariant under light rotation) + texel snapping
 *                 with +0.5-texel snap compensation so no corner ever clips even at margin = 0
 *                 (no shimmer when the light or the content moves; ~1.4-1.7x lower density).
 * Calls `shadow.updateMatrices( light )` after updating projection so `light.shadow.matrix` is fresh on return.
 * Returns the world-space width of one shadow texel, which drives bias tuning.
 */
export function fitDirectionalShadow( light, worldBox, { mode = 'tight', margin = 0.25 } = {} ) {

	const shadow = light.shadow;
	const cam = shadow.camera;
	const { min, max } = worldBox;
	const p = min.clone();

	light.updateMatrixWorld();
	light.target.updateMatrixWorld();
	shadow.updateMatrices( light ); // positions + orients shadow.camera exactly as the renderer will
	const view = cam.matrixWorldInverse; // world -> light view space (camera looks down -Z)

	const dx = max.x - min.x, dy = max.y - min.y, dz = max.z - min.z;
	const r = 0.5 * Math.hypot( dx, dy, dz );
	const eps = Math.max( 1e-5, r * 1e-5 ); // guards IEEE-754 boundary rounding when margin === 0

	if ( mode === 'tight' ) {

		let minX = Infinity, maxX = - Infinity;
		let minY = Infinity, maxY = - Infinity;
		let minZ = Infinity, maxZ = - Infinity;
		for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

			p.set( x, y, z ).applyMatrix4( view );
			if ( p.x < minX ) minX = p.x; if ( p.x > maxX ) maxX = p.x;
			if ( p.y < minY ) minY = p.y; if ( p.y > maxY ) maxY = p.y;
			if ( p.z < minZ ) minZ = p.z; if ( p.z > maxZ ) maxZ = p.z;

		}

		const pad = margin + eps;
		cam.left = minX - pad;
		cam.right = maxX + pad;
		cam.bottom = minY - pad;
		cam.top = maxY + pad;
		cam.near = - maxZ - pad; // may be negative for an orthographic camera; that is valid
		cam.far = - minZ + pad;

	} else {

		p.set( 0.5 * ( min.x + max.x ), 0.5 * ( min.y + max.y ), 0.5 * ( min.z + max.z ) ).applyMatrix4( view );
		const padR = r + margin + eps;
		const nx = Math.max( 2, shadow.mapSize.x );
		const ny = Math.max( 2, shadow.mapSize.y );
		// Solve halfW = padR + 0.5 * texel and texel = (2 * halfW) / n -> texel = (2 * padR) / (n - 1).
		// Width is 100% rotation-invariant, snap step equals exact texel size, and |cx - p.x| <= 0.5 * texel never clips!
		const texelX = ( 2 * padR ) / ( nx - 1 );
		const texelY = ( 2 * padR ) / ( ny - 1 );
		const halfW = 0.5 * nx * texelX;
		const halfH = 0.5 * ny * texelY;
		const cx = Math.round( p.x / texelX ) * texelX;
		const cy = Math.round( p.y / texelY ) * texelY;
		cam.left = cx - halfW;
		cam.right = cx + halfW;
		cam.bottom = cy - halfH;
		cam.top = cy + halfH;
		cam.near = - ( p.z + padR );
		cam.far = - ( p.z - padR );

	}

	cam.updateProjectionMatrix();
	shadow.updateMatrices( light );

	return ( cam.right - cam.left ) / shadow.mapSize.x;

}

/** Starting bias values derived from the fitted frustum (tune from here, not from magic numbers). */
export function suggestShadowBias( light, texelWorld ) {

	const depthRange = light.shadow.camera.far - light.shadow.camera.near;
	return {
		normalBias: texelWorld * 1.0, // world units along the surface normal: ~1 texel
		bias: - Math.min( 0.0005, ( 0.25 * texelWorld ) / depthRange ), // normalized depth; ≈ ¼ texel in world units
	};

}
