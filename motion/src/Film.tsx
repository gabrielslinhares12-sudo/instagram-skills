import React from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {Scenery} from './Scenery';
import {Episode,Scene,episodeSchema,frames} from './schema';
import './style.css';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const Shot:React.FC<{scene:Scene}>=({scene})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const t=frame/fps;
 const progress=frame/Math.max(1,frames(scene.duration)-1);
 const enter=spring({frame,fps,config:{damping:22,stiffness:85}});
 const x=scene.side==='left'?35:300;
 const drift=scene.actor==='enter'?(1-enter)*160:0;
 const bob=Math.sin(t*1.8)*9;
 const discover=scene.actor==='discover'?Math.sin(Math.min(t/1.2,1)*Math.PI)*-3:0;
 const cameraScale=scene.camera==='push'?1+progress*.055:1.06;
 const cameraX=scene.camera==='pan'?-25+progress*50:0;
 const caption=scene.captions.find(c=>t>=c.start&&t<c.end);
 return <AbsoluteFill style={{background:'#f4ede1'}}>
  <AbsoluteFill style={{transform:`translateX(${cameraX}px) scale(${cameraScale})`}}>
   {scene.background ? scene.background.kind==='video'?<OffthreadVideo src={staticFile(scene.background.src)} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>:<Img src={staticFile(scene.background.src)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>:<Scenery kind={scene.environment} time={t}/>}
  </AbsoluteFill>
  <div style={{position:'absolute',left:x+drift,top:720+bob,width:720,transform:`rotate(${discover}deg)`,opacity:scene.actor==='enter'?interpolate(frame,[0,12],[0,1],clamp):1}}>
   <div style={{position:'absolute',left:140,top:140,width:430,height:430,background:'radial-gradient(circle, #ffe89188, transparent 70%)'}}/>
   <Img src={staticFile('lumino-original.png')} style={{width:'100%',filter:'drop-shadow(12px 26px 22px #40342344)'}}/>
  </div>
  {t<scene.headingSeconds&&scene.heading&&<div style={{position:'absolute',top:235,left:72,right:110,transform:`translateY(${(1-enter)*-35}px)`}}>
   <div style={{position:'absolute',inset:'-16px -20px',background:'#ffd600',clipPath:'polygon(1% 9%,98% 0,100% 89%,2% 100%,0 70%)',transform:'rotate(-2deg)'}}/>
   <div style={{position:'relative',fontFamily:'Title',fontSize:100,lineHeight:1,whiteSpace:'pre-line',color:'#111'}}>{scene.heading}</div>
  </div>}
  {caption&&<div style={{position:'absolute',left:90,right:140,top:1530,textAlign:'center',fontFamily:'Title',fontSize:66,lineHeight:1.08,color:'#111',textShadow:'0 2px 5px #fff5e4, 2px 0 5px #fff5e4'}}>{caption.text}</div>}
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
