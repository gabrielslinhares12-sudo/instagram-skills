import React from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {Scenery} from './Scenery';
import {RiggedCharacter} from './actors/RiggedCharacter';
import {poseForBeat} from './actors/rigs';
import {StoryScenery} from './StoryScenery';
import {Episode,Scene,episodeSchema,frames} from './schema';
import './style.css';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const Shot:React.FC<{scene:Scene}>=({scene})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const t=frame/fps;
 const progress=frame/Math.max(1,frames(scene.duration)-1);
 const enter=spring({frame,fps,config:{damping:22,stiffness:85}});
 const story=Boolean(scene.beat);
 const staged=scene.beat==='tea'?{x:535,y:880,size:530}:scene.beat==='hatch'?{x:600,y:825,size:460}:scene.beat==='noise'?{x:0,y:820,size:650}:scene.beat==='sign'?{x:395,y:805,size:590}:null;
 const x=staged?.x??(story?(scene.side==='left'?0:235):(scene.side==='left'?35:300));
 const drift=scene.actor==='enter'?(1-enter)*160:0;
 const bob=Math.sin(t*1.8)*7;
 const cameraScale=scene.camera==='push'?1+progress*.055:1.06;
 const cameraX=scene.camera==='pan'?-25+progress*50:0;
 const caption=scene.captions.find(c=>t>=c.start&&t<c.end);
 const lightOn=scene.beat==='blackout'?Math.max(.25,1-t*2.8):1;
 const defaultSize=staged?.size??(story?805:720);
 const defaultY=staged?.y??(story?685:720);
 const cast=scene.characters??[{instance:'lumino-main',id:'lumino',pose:poseForBeat(scene.beat),
   x,y:defaultY,size:defaultSize,enter:scene.actor==='enter'?'glide' as const:'none' as const}];
 return <AbsoluteFill style={{background:'#f4ede1'}}>
  <AbsoluteFill style={{transform:`translateX(${cameraX}px) scale(${cameraScale})`}}>
   {scene.background ? scene.background.kind==='video'?<OffthreadVideo src={staticFile(scene.background.src)} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>:<Img src={staticFile(scene.background.src)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>:story?<StoryScenery kind={scene.environment} beat={scene.beat} time={t} layer="background"/>:<Scenery kind={scene.environment} time={t}/>}
  </AbsoluteFill>
  {cast.map(actor=>{
   const actorEnter=actor.enter==='glide';
   const approach=actorEnter?(1-enter)*155:0;
   const actorLight=scene.beat==='blackout'?lightOn:1;
   return <React.Fragment key={actor.instance}>
    {story&&<div style={{
       position:'absolute',left:actor.x+actor.size*.17+approach,
       top:actor.y+actor.size*.94,
       width:actor.size*.58,height:70,borderRadius:'50%',
       background:'#07171c9e',filter:'blur(26px)',
       transform:'scaleX(1.2)'
      }}/>}
    <div style={{
      position:'absolute',left:actor.x+approach,top:actor.y+bob,
      width:actor.size,
      opacity:actorEnter?interpolate(frame,[0,12],[0,1],clamp):1,
      filter:story?'drop-shadow(15px 26px 22px rgba(3,12,22,.65))':undefined
     }}>
     <RiggedCharacter id={actor.id} pose={actor.pose} time={t} light={actorLight}/>
    </div>
   </React.Fragment>;
  })}
  {story&&<StoryScenery kind={scene.environment} beat={scene.beat} time={t} layer="foreground"/>}
  {scene.beat==='blackout'&&<AbsoluteFill style={{background:'#06101a',opacity:Math.min(.8,t*.45)}}/>}
  {t<scene.headingSeconds&&scene.heading&&<div style={{position:'absolute',top:235,left:72,right:110,transform:`translateY(${(1-enter)*-35}px)`}}>
   <div style={{position:'absolute',inset:'-16px -20px',background:'#ffd600',clipPath:'polygon(1% 9%,98% 0,100% 89%,2% 100%,0 70%)',transform:'rotate(-2deg)'}}/>
   <div style={{position:'relative',fontFamily:'Title',fontSize:100,lineHeight:1,whiteSpace:'pre-line',color:'#111'}}>{scene.heading}</div>
  </div>}
  {caption&&<div style={{position:'absolute',left:90,right:140,top:story?1580:1530,textAlign:'center',fontFamily:'Title',fontSize:story?60:66,lineHeight:1.08,color:story?'#fff6de':'#111',textShadow:story?'0 2px 9px #071721, 0 3px 15px #071721':'0 2px 5px #fff5e4, 2px 0 5px #fff5e4'}}>{caption.text}</div>}
  {scene.sounds.map((s,i)=><Sequence key={i} from={frames(s.start)} durationInFrames={frames(s.duration)}><Audio src={staticFile(s.src)} volume={s.volume}/></Sequence>)}
 </AbsoluteFill>;
};
export const Film:React.FC<Episode>=(props)=>{
 const episode=episodeSchema.parse(props); const {width}=useVideoConfig(); let start=0;
 return <AbsoluteFill style={{background:'#f4ede1'}}>
  <style>{`@font-face {font-family:Title;src:url('${staticFile('title.woff2')}') format('woff2');font-weight:800;font-display:block;}`}</style>
  <div style={{position:'absolute',width:1080,height:1920,transform:`scale(${width/1080})`,transformOrigin:'top left',overflow:'hidden'}}>
   {episode.scenes.map(scene=>{const from=start;start+=frames(scene.duration);return <Sequence key={scene.id} from={from} durationInFrames={frames(scene.duration)}><Shot scene={scene}/></Sequence>;})}
  </div>
  {episode.narration&&<Audio src={staticFile(episode.narration)}/>}
 </AbsoluteFill>;
};
