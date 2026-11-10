// Check a project's installed three.js: revision, version gates, and whether named symbols exist.
// Usage:
//   node check-three-api.mjs --root /path/to/project                 # revision + gate warnings + default symbol set
//   node check-three-api.mjs --root . three/tsl:ssgi,builtinAOContext three/addons/lights/SunLight.js:SunLight
// Exit code 1 when any requested symbol is missing.
import { existsSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

globalThis.self ??= globalThis; globalThis.window ??= globalThis; // WebGPU build touches `self`
Object.defineProperty( globalThis, 'localStorage', { value: { getItem: () => null, setItem: () => {}, removeItem: () => {} }, configurable: true } ); // Inspector.js touches localStorage

const args = process.argv.slice( 2 );
const rootIdx = args.indexOf( '--root' );
const root = resolve( rootIdx >= 0 ? args[ rootIdx + 1 ] : '.' );
const specs = args.filter( ( a, i ) => a !== '--root' && i !== rootIdx + 1 );
const threeDir = resolve( root, 'node_modules/three' );
if ( ! existsSync( threeDir ) ) { console.error( `no node_modules/three under ${ root }` ); process.exit( 2 ); }

const pkg = JSON.parse( readFileSync( resolve( threeDir, 'package.json' ), 'utf8' ) );
const rev = Number( pkg.version.split( '.' )[ 1 ] );
console.log( `three ${ pkg.version } (r${ rev })` );

const gates = [
	[ rev < 165, 'r<165: legacy light mode may exist (useLegacyLights). Set physical intensities explicitly; decay = 2.' ],
	[ rev < 180, 'r<180: use RGBELoader (HDRLoader does not exist yet).' ],
	[ rev >= 180, 'r180+: use HDRLoader (RGBELoader is a deprecated shim).' ],
	[ rev < 183, 'r<183: WebGPU post class is THREE.PostProcessing.' ],
	[ rev >= 183, 'r183+: WebGPU post class is THREE.RenderPipeline (PostProcessing deprecated).' ],
	[ rev >= 182 && rev < 186, 'r182-185: PCFSoftShadowMap deprecated; use PCFShadowMap + shadow.radius.' ],
	[ rev >= 186, 'r186+: PCFSoftShadowMap removed at runtime (rewritten to PCFShadowMap with warning).' ],
	[ rev >= 184, 'r184+: LightProbeGrid available (irradiance volume).' ],
	[ rev >= 186, 'r186+: SunLight (CSM), VXGIVolume, retroreflectivity available.' ],
	[ rev >= 187, 'r187+: LightMapper, diffuseRoughness, BundleGroup, NodeMaterialInstance, TAAUNode, FSR1Node, OITPassNode, GaussianSplat available; TSL transformedNormal* removed (use normalView/normalWorld); struct storage buffers are arrays (.element(i).get(...)).' ],
	[ rev >= 183, 'r183+: THREE.Clock deprecated — use THREE.Timer (timer.connect(document)).' ],
	[ rev >= 169, 'r169+: TransformControls is not an Object3D — add scene.add(tc.getHelper()).' ],
];
for ( const [ on, msg ] of gates ) if ( on ) console.log( '  gate:', msg );

const pp = resolve( root, 'node_modules/postprocessing/package.json' );
if ( existsSync( pp ) ) {

	const p = JSON.parse( readFileSync( pp, 'utf8' ) );
	const peer = p.peerDependencies?.three ?? '';
	const upperMatch = peer.match( /<\s*0\.(\d+)\./ );
	const upperMinor = upperMatch ? Number( upperMatch[ 1 ] ) : null;
	const ok = upperMinor === null || rev < upperMinor;
	console.log( `postprocessing ${ p.version } peer three "${ peer }" — ${ ok ? `compatible with r${ rev }` : `WARNING: r${ rev } exceeds peer upper bound <0.${ upperMinor }.0` }` );

}

const rootReq = existsSync( resolve( root, 'package.json' ) ) ? createRequire( resolve( root, 'package.json' ) ) : null;
const mapUrl = ( spec ) => {

	if ( spec === 'three' ) return pathToFileURL( resolve( threeDir, 'build/three.module.js' ) ).href;
	if ( spec === 'three/webgpu' ) return pathToFileURL( resolve( threeDir, 'build/three.webgpu.js' ) ).href;
	if ( spec === 'three/tsl' ) return pathToFileURL( resolve( threeDir, 'build/three.tsl.js' ) ).href;
	if ( spec.startsWith( 'three/addons/' ) ) return pathToFileURL( resolve( threeDir, 'examples/jsm', spec.slice( 'three/addons/'.length ) ) ).href;
	const pkgJson = resolve( root, 'node_modules', spec, 'package.json' );
	if ( existsSync( pkgJson ) ) {

		const p = JSON.parse( readFileSync( pkgJson, 'utf8' ) );
		const entry = p.module ?? ( typeof p.exports === 'string' ? p.exports : p.exports?.[ '.' ]?.import ?? p.exports?.[ '.' ]?.default ) ?? p.main;
		if ( typeof entry === 'string' ) return pathToFileURL( resolve( root, 'node_modules', spec, entry ) ).href;

	}
	try { if ( rootReq ) return pathToFileURL( rootReq.resolve( spec ) ).href; } catch { /* fall through */ }
	return pathToFileURL( resolve( root, 'node_modules', spec ) ).href;

};

const defaults = [
	'three:ColorManagement,AgXToneMapping,NeutralToneMapping,PCFShadowMap,VSMShadowMap,PMREMGenerator,MeshPhysicalMaterial,Timer,BatchedMesh,InstancedMesh',
	'three/webgpu:WebGPURenderer,BundleGroup,MeshPhysicalNodeMaterial,MeshToonNodeMaterial,PointsNodeMaterial,RectAreaLightNode,NodeMaterialInstance,StorageTexture,IndirectStorageBufferAttribute',
	'three/tsl:pass,mrt,output,normalView,normalWorld,positionLocal,velocity,builtinAOContext,renderOutput,toonOutlinePass,reference,materialReference,instancedArray,instancedBufferAttribute,workgroupArray,workgroupBarrier,atomicAdd,textureStore,TWO_PI',
	`three/webgpu:${ rev >= 183 ? 'RenderPipeline' : 'PostProcessing' }`,
	`three/addons/loaders/${ rev >= 180 ? 'HDRLoader.js:HDRLoader' : 'RGBELoader.js:RGBELoader' }`,
	'three/addons/utils/SkeletonUtils.js:clone',
	'three/addons/utils/SceneOptimizer.js:SceneOptimizer',
	'three/addons/objects/GaussianSplat.js:GaussianSplat',
	'three/addons/inspector/Inspector.js:Inspector',
	'three/addons/tsl/display/GTAONode.js:ao',
	'three/addons/tsl/display/TRAANode.js:traa',
	'three/addons/tsl/display/TAAUNode.js:taau',
	'three/addons/tsl/display/FSR1Node.js:fsr1',
	'three/addons/tsl/display/OITPassNode.js:oitPass',
];

let fail = 0;
for ( const entry of ( specs.length ? specs : defaults ) ) {

	const cut = entry.lastIndexOf( ':' );
	const mod = entry.slice( 0, cut ), names = entry.slice( cut + 1 ).split( ',' ).filter( Boolean );
	const url = mapUrl( mod );
	let m;
	try { m = await import( url ); } catch ( e ) { console.log( `MISSING MODULE ${ mod } (${ e.message.split( '\n' )[ 0 ] })` ); fail ++; continue; }
	for ( const n of names ) { if ( ( m[ n ] ?? m.default?.[ n ] ) === undefined ) { console.log( `MISSING ${ mod } :: ${ n }` ); fail ++; } }

}

console.log( fail ? `${ fail } missing` : 'all requested symbols present' );
process.exitCode = fail ? 1 : 0;
