import React from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,interpolate,spring,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {Scenery} from './Scenery';
import {StoryScenery} from './StoryScenery';
import {Episode,Scene,episodeSchema,frames} from './schema';
import './style.css';
const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'} as const;
const Shot:React.FC<{scene:Scene}>=({scene})=>{
 const frame=useCurrentFrame(); const {fps}=useVideoConfig(); const t=frame/fps;
 const progress=frame/Math.max(1,frames(scene.duration)-1);
 const enter=spring({frame,fps,config:{damping:22,stiffness:85}});
 const story=Boolean(scene.beat);
 const x=story?(scene.side==='left'?0:235):(scene.side==='left'?35:300);
 const drift=scene.actor==='enter'?(1-enter)*160:0;
 const bob=Math.sin(t*1.8)*9;
 const discover=scene.actor==='discover'?Math.sin(Math.min(t/1.2,1)*Math.PI)*-3:0;
 const cameraScale=scene.camera==='push'?1+progress*.055:1.06;
 const cameraX=scene.camera==='pan'?-25+progress*50:0;
 const caption=scene.captions.find(c=>t>=c.start&&t<c.end);
 const lightOn=scene.beat==='blackout'?Math.max(0,1-t*2.8):1;
 return <AbsoluteFill style={{background:'#f4ede1'}}>
  <AbsoluteFill style={{transform:`translateX(${cameraX}px) scale(${cameraScale})`}}>
   {scene.background ? scene.background.kind==='video'?<OffthreadVideo src={staticFile(scene.background.src)} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>:<Img src={staticFile(scene.background.src)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>:story?<StoryScenery kind={scene.environment} beat={scene.beat} time={t} layer="background"/>:<Scenery kind={scene.environment} time={t}/>}
  </AbsoluteFill>
  {story&&<div style={{position:'absolute',left:x+200+drift,top:1360,width:410,height:70,borderRadius:'50%',background:'#0a1e26a8',filter:'blur(26px)',transform:'scaleX(1.4)'}}/>}
  <div style={{position:'absolute',left:x+drift,top:(story?685:720)+bob,width:story?805:720,transform:`rotate(${discover}deg)`,opacity:scene.actor==='enter'?interpolate(frame,[0,12],[0,1],clamp):1}}>
   <div style={{position:'absolute',left:120,top:115,width:560,height:590,background:'radial-gradient(circle, rgba(255,219,118,.68) 0%, rgba(255,200,76,.26) 40%, transparent 73%)',opacity:story?lightOn:.65,mixBlendMode:'screen'}}/>
   <Img src={staticFile('lumino-original.png')} style={{width:'100%',filter:story?'drop-shadow(18px 26px 19px rgba(3,12,22,.72))':'drop-shadow(12px 26px 22px #40342344)'}}/>
  </div>
  {story&&<StoryScenery kind={scene.environment} beat={scene.beat} time={t} layer="foreground"/>}
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
