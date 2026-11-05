// A reusable 2D cutout rig: all movable parts sample pixels from the SAME
// source image. New cast members only need a vetted source and a manifest.
// Never regenerate a canonical character or silently mutate its artwork.
export type Pose='idle'|'arrive'|'look'|'point'|'inspect'|'listen'|'react'|'discover';
export type Bone='head'|'leftArm'|'rightArm';
export type RigPart={bone:Bone;path:string;pivot:[number,number]};
export type RigManifest={
 id:string;source:string;width:number;height:number;
 parts:RigPart[];light:{x:number;y:number;rx:number;ry:number};
};
const lumino:RigManifest={
 id:'lumino',source:'lumino-original.png',width:1230,height:1278,
 light:{x:510,y:505,rx:350,ry:395},
 parts:[
  // The lantern head ends at the natural coat/neck join.
  {bone:'head',pivot:[530,705],
   path:'M150 -20 L850 -20 L880 580 L800 650 L720 710 L650 745 L455 755 L390 710 L405 625 L415 565 L250 570 L160 525 Z'},
  // The pointing sleeve+glove rotates around the coat shoulder.
  {bone:'rightArm',pivot:[745,760],
   path:'M690 640 L760 680 L825 660 L865 620 L936 590 L1020 545 L1215 465 L1230 550 L1130 650 L1180 720 L1130 765 L1060 795 L1000 880 L890 930 L745 900 L690 860 L650 730 Z'},
  // Gloved magnifier hand and lens use two contiguous mask islands.
  // The movement range is intentionally small to protect the eyeglass seam.
  {bone:'leftArm',pivot:[300,830],
   path:'M140 900 L185 815 L385 800 L440 875 L465 1025 L300 1095 L150 1045 Z M265 580 A145 129 0 1 1 264.9 580 Z'}
 ]};
export const RIGS:Readonly<Record<string,RigManifest>>=Object.freeze({lumino});
export const hasRig=(id:string):boolean=>Object.hasOwn(RIGS,id);
export function requireRig(id:string):RigManifest{
 const rig=RIGS[id];
 if(!rig)throw new Error('Personagem sem rig aprovado: '+id);
 return rig;
}
export const poses:readonly Pose[]=['idle','arrive','look','point','inspect','listen','react','discover'];
const target:Record<Pose,{head:number;leftArm:number;rightArm:number;body:number}>={
 idle:{head:0,leftArm:0,rightArm:0,body:0},
 arrive:{head:-.7,leftArm:0,rightArm:1.2,body:1.3},
 look:{head:-1.8,leftArm:.2,rightArm:1.0,body:0},
 point:{head:-.8,leftArm:0,rightArm:-5.5,body:-.7},
 inspect:{head:-2.5,leftArm:1.2,rightArm:.5,body:1},
 listen:{head:1.9,leftArm:0,rightArm:1.3,body:0},
 react:{head:2.1,leftArm:.5,rightArm:3,body:-1.5},
 discover:{head:-2.2,leftArm:.5,rightArm:-4.5,body:1}
};
const smooth=(x:number)=>{const n=Math.min(1,Math.max(0,x));return n*n*(3-2*n);};
export function actingPose(pose:Pose,time:number){
 // Frame-time-only deterministic motion: safe for distributed Remotion renders.
 const mix=smooth(time/.4);
 const desired=target[pose];
 const breathe=Math.sin(time*1.7);
 const reactive=pose==='react'?Math.sin(time*14)*Math.exp(-time*.8):0;
 return {
  head:(desired.head*mix)+(Math.sin(time*1.3)*.6)+reactive*.4,
  rightArm:(desired.rightArm*mix)+(Math.sin(time*2.1)*.45),
  leftArm:(desired.leftArm*mix)+(Math.sin(time*1.9)*.3),
  body:(desired.body*mix)+(breathe*.5),
  light:pose==='react'?Math.max(.3,1+reactive*.2):1,
 };
}
export function poseForBeat(beat:string|undefined):Pose{
 switch(beat){
  case 'flash':case 'blackout':return 'react';
  case 'arrival':return 'arrive';
  case 'sign':case 'noise':return 'inspect';
  case 'tea':return 'listen';
  case 'hatch':return 'point';
  case 'voice':return 'discover';
  default:return 'idle';
 }
}
