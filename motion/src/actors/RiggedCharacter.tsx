import React,{useId} from 'react';
import {staticFile} from 'remotion';
import {actingPose,requireRig,type Bone,type Pose} from './rigs';

// Every part samples its pixels from the immutable canonical PNG. SVG masks
// assign each source pixel to one layer; this is skeletal 2D cutout animation,
// not a single sticker being translated or tilted.
export const RiggedCharacter:React.FC<{
 id:string;pose:Pose;time:number;light?:number;
}>=({id,pose,time,light=1})=>{
 const rig=requireRig(id);
 const unique=useId().replace(/[^a-zA-Z0-9_-]/g,'');
 const act=actingPose(pose,time);
 const source=staticFile(rig.source);
 const wholeMask=unique+'body';
 const partMask=(index:number)=>unique+'part'+index;
 const glowId=unique+'glow';
 const rot:Record<Bone,number>={
  head:act.head,leftArm:act.leftArm,rightArm:act.rightArm
 };
 const dim=Math.max(.22,Math.min(1,light));
 return <svg width="100%" height="100%"
   viewBox={['0','0',rig.width,rig.height].join(' ')}
   preserveAspectRatio="xMidYMid meet"
   style={{display:'block',overflow:'visible',pointerEvents:'none'}}>
   <defs>
    <radialGradient id={glowId}>
     <stop offset="0" stopColor="#ffeeb4" stopOpacity=".55"/>
     <stop offset=".48" stopColor="#ffcd5a" stopOpacity=".18"/>
     <stop offset="1" stopColor="#ffe481" stopOpacity="0"/>
    </radialGradient>
    <mask id={wholeMask} maskUnits="userSpaceOnUse">
     <rect width={rig.width} height={rig.height} fill="white"/>
     {rig.parts.map((part,i)=><path key={i} d={part.path} fill="black"/>)}
    </mask>
    {rig.parts.map((part,index)=>
      <mask key={part.bone} id={partMask(index)} maskUnits="userSpaceOnUse">
       <path d={part.path} fill="white"/>
       {rig.parts.slice(index+1).map((later,j)=>
        <path key={j} d={later.path} fill="black"/>)}
      </mask>
    )}
   </defs>
   <g transform={'translate(615 1000) rotate('+act.body+') translate(-615 -1000)'}>
    <ellipse cx={rig.light.x} cy={rig.light.y} rx={rig.light.rx} ry={rig.light.ry}
      fill={'url(#'+glowId+')'} opacity={Math.min(1,dim*act.light)}/>
    <image href={source} width={rig.width} height={rig.height}
      mask={'url(#'+wholeMask+')'}/>
    {rig.parts.map((part,i)=>{
      const [px,py]=part.pivot;
      return <g key={part.bone}
        transform={'translate('+px+' '+py+') rotate('+rot[part.bone]+') translate('+(-px)+' '+(-py)+')'}>
        <image href={source} width={rig.width} height={rig.height}
          mask={'url(#'+partMask(i)+')'}/>
      </g>;
    })}
    {dim<.999&&<rect width={rig.width} height={rig.height}
      fill="#091b27" opacity={Math.min(.65,(1-dim)*.7)}
      mask={'url(#'+wholeMask+')'}/>}
   </g>
  </svg>;
};
