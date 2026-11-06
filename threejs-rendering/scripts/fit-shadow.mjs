import * as THREE from 'three';

const _corners = Array.from( { length: 8 }, () => new THREE.Vector3() );
const _box = new THREE.Box3();
const _sphere = new THREE.Sphere();
const _c = new THREE.Vector3();

/**
 * Fit a DirectionalLight's orthographic shadow camera to a world-space Box3.
 * mode 'tight'  : light-space AABB of the 8 box corners (best texel density; use for static scenes).
 * mode 'stable' : bounding-sphere square (size invariant under light rotation) + texel snapping
 *                 (no shimmer when the light or the content moves; ~1.4–1.7x lower density).
 * Returns the world-space size of one shadow texel, which drives bias tuning.
 */
export function fitDirectionalShadow( light, worldBox, { mode = 'tight', margin = 0.25 } = {} ) {

	const shadow = light.shadow;
	const cam = shadow.camera;

	light.updateMatrixWorld();
	light.target.updateMatrixWorld();
	shadow.updateMatrices( light ); // positions + orients shadow.camera exactly as the renderer will
	const view = cam.matrixWorldInverse; // world -> light view space (camera looks down -Z)

	let minX, maxX, minY, maxY, minZ, maxZ;

	if ( mode === 'tight' ) {

		const { min, max } = worldBox;
		let i = 0;
		for ( const x of [ min.x, max.x ] ) for ( const y of [ min.y, max.y ] ) for ( const z of [ min.z, max.z ] ) {

			_corners[ i ++ ].set( x, y, z ).applyMatrix4( view );

		}

		_box.setFromPoints( _corners );
		( { x: minX, y: minY, z: minZ } = _box.min );
		( { x: maxX, y: maxY, z: maxZ } = _box.max );

	} else {

		worldBox.getBoundingSphere( _sphere );
		_c.copy( _sphere.center ).applyMatrix4( view );
		const r = _sphere.radius;
		// snap the square's centre to whole texels so rasterisation is stable frame to frame
		const texel = ( 2 * ( r + margin ) ) / shadow.mapSize.x;
		const cx = Math.round( _c.x / texel ) * texel;
		const cy = Math.round( _c.y / texel ) * texel;
		minX = cx - r; maxX = cx + r; minY = cy - r; maxY = cy + r;
		minZ = _c.z - r; maxZ = _c.z + r;

	}

	cam.left = minX - margin;
	cam.right = maxX + margin;
	cam.bottom = minY - margin;
	cam.top = maxY + margin;
	cam.near = - maxZ - margin; // may be negative for an orthographic camera; that is valid
	cam.far = - minZ + margin;
	cam.updateProjectionMatrix();

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
