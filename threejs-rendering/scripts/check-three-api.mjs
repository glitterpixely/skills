// Check a project's installed three.js: revision, version gates, and whether named symbols exist.
// Usage:
//   node check-three-api.mjs --root /path/to/project                 # revision + gate warnings + default symbol set
//   node check-three-api.mjs --root . three/tsl:ssgi,builtinAOContext three/addons/lights/SunLight.js:SunLight
// Exit code 1 when any requested symbol is missing.
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

globalThis.self ??= globalThis; globalThis.window ??= globalThis; // WebGPU build touches `self`

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
	[ rev >= 182 && rev < 186, 'r182–185: PCFSoftShadowMap deprecated; use PCFShadowMap + shadow.radius.' ],
	[ rev >= 186, 'r186+: PCFSoftShadowMap removed (falls back to PCFShadowMap).' ],
	[ rev >= 184, 'r184+: LightProbeGrid available (irradiance volume).' ],
	[ rev >= 186, 'r186+: SunLight (CSM), VXGI, retroreflectivity available.' ],
	[ rev >= 187, 'r187+: LightMapper, diffuseRoughness available; TSL transformedNormal* removed (use normalView/normalWorld); struct storage buffers are arrays (.element(i).get(...)).' ],
	[ rev >= 183, 'r183+: THREE.Clock deprecated — use THREE.Timer (timer.connect(document)).' ],
	[ rev >= 169, 'r169+: TransformControls is not an Object3D — add scene.add(tc.getHelper()).' ],
];
for ( const [ on, msg ] of gates ) if ( on ) console.log( '  gate:', msg );

const pp = resolve( root, 'node_modules/postprocessing/package.json' );
if ( existsSync( pp ) ) {

	const p = JSON.parse( readFileSync( pp, 'utf8' ) );
	console.log( `postprocessing ${ p.version } peer three ${ p.peerDependencies?.three } — check r${ rev } is inside that range` );

}

const map = ( spec ) => {

	if ( spec === 'three' ) return resolve( threeDir, 'build/three.module.js' );
	if ( spec === 'three/webgpu' ) return resolve( threeDir, 'build/three.webgpu.js' );
	if ( spec === 'three/tsl' ) return resolve( threeDir, 'build/three.tsl.js' );
	if ( spec.startsWith( 'three/addons/' ) ) return resolve( threeDir, 'examples/jsm', spec.slice( 'three/addons/'.length ) );
	return resolve( root, 'node_modules', spec );

};

const defaults = [
	'three:ColorManagement,AgXToneMapping,NeutralToneMapping,PCFShadowMap,VSMShadowMap,PMREMGenerator,MeshPhysicalMaterial,Timer,BatchedMesh,InstancedMesh',
	'three/webgpu:WebGPURenderer,MeshPhysicalNodeMaterial,MeshToonNodeMaterial,PointsNodeMaterial,RectAreaLightNode',
	'three/tsl:pass,mrt,output,normalView,normalWorld,positionLocal,velocity,builtinAOContext,renderOutput,toonOutlinePass,reference,instancedArray,instancedBufferAttribute,TWO_PI',
	`three/webgpu:${ rev >= 183 ? 'RenderPipeline' : 'PostProcessing' }`,
	`three/addons/loaders/${ rev >= 180 ? 'HDRLoader.js:HDRLoader' : 'RGBELoader.js:RGBELoader' }`,
	'three/addons/utils/SkeletonUtils.js:clone',
	'three/addons/tsl/display/GTAONode.js:ao',
	'three/addons/tsl/display/TRAANode.js:traa',
];

let fail = 0;
for ( const entry of ( specs.length ? specs : defaults ) ) {

	const cut = entry.lastIndexOf( ':' );
	const mod = entry.slice( 0, cut ), names = entry.slice( cut + 1 ).split( ',' ).filter( Boolean );
	const file = map( mod );
	let m;
	try { m = await import( pathToFileURL( file ).href ); } catch ( e ) { console.log( `MISSING MODULE ${ mod } (${ e.message.split( '\n' )[ 0 ] })` ); fail ++; continue; }
	for ( const n of names ) { if ( m[ n ] === undefined ) { console.log( `MISSING ${ mod } :: ${ n }` ); fail ++; } }

}

console.log( fail ? `${ fail } missing` : 'all requested symbols present' );
process.exitCode = fail ? 1 : 0;
