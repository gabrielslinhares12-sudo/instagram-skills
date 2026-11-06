import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {Odysseus,type WarriorPose} from './actors/OdysseusActor';

// Four original, distinct fully vector-drawn acting setups, not recycled stills.
// QC stage only: 14 seconds at genuine 2160x3840 / 60fps. Not a finished long film.
const ease=(v:number)=>{const x=Math.max(0,Math.min(1,v));return x*x*(3-2*x)};
const W=1080,H=1920,SHOT=3.5;
const palette=[
 {skyA:'#172c44',skyB:'#d18d64',light:'#f4cb90',ground:'#b89267',name:'CHEGADA A ÍTACA'},
 {skyA:'#091e35',skyB:'#2e5766',light:'#ffc77e',ground:'#6f665c',name:'O PORTÃO DO PALÁCIO'},
 {skyA:'#172d2b',skyB:'#7c866f',light:'#fff4ce',ground:'#91836a',name:'O CAMINHO DA OLIVEIRA'},
 {skyA:'#090d24',skyB:'#413857',light:'#d5bed7',ground:'#464050',name:'A FUGA DA CAVERNA'},
] as const;
const waves=Array.from({length:11},(_,i)=>i),mist=Array.from({length:7},(_,i)=>i),stars=Array.from({length:48},(_,i)=>i);
const lightpath=(i:number,t:number)=>`M ${-100+i*135+Math.sin(t*1.5+i)*20} ${1120+i*34} q 96 ${-19+Math.sin(t*2+i)*7} 201 0`;
const Environment:React.FC<{shot:number;t:number}>=({shot,t})=>{
 const p=palette[shot],dawn=shot===0,castle=shot===1,grove=shot===2,cave=shot===3;
 const cloud=t*24;
 return <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position:'absolute',inset:0}}>
 <defs>
  <linearGradient id={`gsky-${shot}`} x1="0" y1="0" x2="0" y2="1">
   <stop stopColor={p.skyA}/><stop offset=".88" stopColor={p.skyB}/><stop offset="1" stopColor={p.ground}/>
  </linearGradient>
  <linearGradient id={`groad-${shot}`} x1="0" y1="0" x2=".2" y2="1">
    <stop stopColor={p.ground}/><stop offset="1" stopColor="#393d41"/>
  </linearGradient>
  <radialGradient id={`light-${shot}`}>
    <stop stopColor={p.light} stopOpacity=".74"/>
    <stop offset="1" stopColor={p.light} stopOpacity="0"/>
  </radialGradient>
 </defs>
 <rect width={W} height={H} fill={`url(#gsky-${shot})`}/>
 <circle cx={grove?816:castle?673:760} cy={grove?363:308} r={cave?0:130} fill={p.light} opacity=".62"/>
 <circle cx={grove?816:castle?673:760} cy={grove?363:308} r={cave?0:420} fill={`url(#light-${shot})`} opacity=".6"/>
 {stars.map(i=><circle key={i} cx={(i*173+19)%W} cy={(i*139+23)%780} r={i%4===0?2.9:1.3}
   fill="#fff5df" opacity={cave?.34+.25*Math.sin(i*1.9+t*.65):castle?.23:0}/>)}
 {dawn&&<>
   <path d="M0 960Q128 810 264 920T531 920Q715 835 885 943L1080 851V1400H0Z" fill="#67767b"/>
   <path d="M0 1170Q310 970 485 1160T1080 1055V1470H0Z" fill="#465d66"/>
   <path d="M0 1290Q330 1230 530 1280T1080 1230V1920H0Z" fill="#244757"/>
   {waves.map(i=><path key={i} d={lightpath(i,t)} fill="none" stroke="#bbd5ce" opacity={.13+i%3*.09} strokeWidth={i%3===0?7:3}/>)}
   <path d="M0 1440Q350 1380 661 1500T1080 1420V1920H0Z" fill="#c39b71"/>
   <path d="M0 1540Q560 1508 1080 1594" stroke="#ecd4b2" opacity=".57" strokeWidth="14" fill="none"/>
   {[0,1,2,3,4].map(i=><g key={i} transform={`translate(${(i*250+t*4)%1280-130} 1510)`}>
      <path d="M0 0V-70" stroke="#5b5e43" strokeWidth="8"/>
      <path d="M0 -55Q-75 -155 -40 -195Q5 -128 8 -68" fill="#73806a"/>
      <path d="M0 -75Q75 -165 90 -127Q33 -73 0 -43" fill="#87946b"/>
   </g>)}
 </>}
 {castle&&<>
  <path d="M0 1040L320 855L550 915L860 680L1080 780V1920H0Z" fill="#273c43"/>
  <path d="M0 960H1080V1920H0Z" fill="#a68c6f"/>
  {[0,1,2,3,4].map(i=><g key={i} transform={`translate(${i*264-45} 562)`}>
   <rect width="155" height="885" fill="#9a8068" stroke="#3a373a" strokeWidth="12"/>
   <path d="M-19 0L74 -140L166 0" fill="#bc9c78" stroke="#3e3432" strokeWidth="13"/>
   <path d="M26 140H129M26 425H129" stroke="#e3c79a" strokeWidth="11" opacity=".6"/>
  </g>)}
  <path d="M430 1017V1430H680V1017Q560 780 430 1017" fill="#21343e" stroke="#e0c9a0" strokeWidth="15"/>
  {[0,1,2,3,4,5].map(i=><path key={i} d={`M${i*205-53} 1510L${i*217-30} 1920`} stroke="#e4c394" strokeWidth="5" opacity=".35"/>)}
  <path d="M0 1510H1080V1920H0Z" fill="#6b6459" opacity=".47"/>
  {[0,1,2].map(i=><g key={i} transform={`translate(${280+i*380} 1050)`}>
   <path d="M0 -110V310" stroke="#382c2b" strokeWidth="18"/>
   <circle cy="-130" r="42" fill="#ffd492" opacity={.8+.15*Math.sin(t*7+i)}/>
   <circle cy="-130" r="160" fill={`url(#light-${shot})`} opacity=".35"/>
  </g>)}
 </>}
 {grove&&<>
  <path d="M0 1000Q230 765 500 903Q770 728 1080 843V1920H0Z" fill="#586b5f"/>
  <path d="M0 1270Q400 1030 800 1210T1080 1130V1920H0Z" fill="#677566"/>
  <path d="M0 1450Q500 1327 1080 1400V1920H0Z" fill="#947f67"/>
  {[0,1,2,3,4].map(i=><g key={i} transform={`translate(${i*270+54} ${1370-(i%2)*70})`}>
   <path d="M0 0L5 -440" stroke="#534839" strokeWidth="38" strokeLinecap="round"/>
   <path d="M0 -260Q-150 -438 -103 -590M0 -262Q159 -425 126 -606" fill="none" stroke="#5d5440" strokeWidth="21"/>
   <ellipse cx="1" cy="-540" rx="177" ry="96" fill="#4d6455" opacity=".95"/>
   <ellipse cx="-66" cy="-597" rx="129" ry="70" fill="#617d60"/>
   <ellipse cx="103" cy="-598" rx="132" ry="78" fill="#78916c"/>
   {[0,1,2,3,4,5].map(j=><ellipse key={j} cx={(j*57)%215-105} cy={-535-(j*17)%71} rx="9" ry="12" fill="#292d24"/>)}
  </g>)}
  <path d="M0 1520Q220 1490 540 1570T1080 1540" stroke="#d1ae83" opacity=".6" strokeWidth="20" fill="none"/>
 </>}
 {cave&&<>
  <path d="M0 0H1080V1200Q960 1020 850 1140Q600 950 410 1160Q180 890 0 1160Z" fill="#191c2b"/>
  <path d="M0 950L130 1300L63 1850L0 1920ZM1080 790L890 1160L1000 1650L1080 1800Z" fill="#23202c"/>
  <path d="M0 1400Q550 1280 1080 1440V1920H0Z" fill="#33313b"/>
  {mist.map(i=><ellipse key={i} cx={(t*32+i*233)%1250-120} cy={1310+i*82} rx="170" ry="24" fill="#b6bed0" opacity=".08"/>)}
  {[0,1,2,3].map(i=><g key={i} transform={`translate(${i*296+104} ${1400+(i%2)*100})`}>
    <path d="M0 0V-260" stroke="#2c2929" strokeWidth="18"/>
    <circle cy="-280" r={34+Math.sin(t*13+i)*6} fill="#ffb66d"/>
    <ellipse cy="-280" ry="125" rx="110" fill={`url(#light-${shot})`} opacity=".45"/>
  </g>)}
 </>}
 {/* Foreground detail: sand/dust, gravel, shadows track in world coordinates. */}
 {Array.from({length:29},(_,i)=><ellipse key={i} cx={(i*197+47)%1125} cy={1573+(i*41)%360}
    rx={i%3===0?12:5} ry={i%5===0?3:2}
    fill={cave?'#78828c':'#e6d5b5'} opacity=".34"/>)}
 </svg>
};

export const OdysseyGaitQC:React.FC=()=>{
 const f=useCurrentFrame(),{fps}=useVideoConfig(),time=f/fps;
 const shot=Math.min(3,Math.floor(time/SHOT)), t=time-shot*SHOT;
 const p=palette[shot];
 const actorPose:WarriorPose=(['walk','creep','limp','run'] as const)[shot];
 const speed=[96,48,64,122][shot];
 const scale=[1.68,1.95,1.82,1.68][shot];
 const initialX=[-112,-105,-88,-130][shot];
 const motion=initialX+t*speed*.96;
 const y= [800,750,770,795][shot];
 const brightness=Math.min(1,t/.42,(SHOT-t)/.38);
 return <AbsoluteFill style={{background:'#112331'}}>
   <div style={{position:'absolute',inset:0,opacity:brightness}}>
    <Environment shot={shot} t={t}/>
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
     <ellipse cx={motion+181*scale} cy={y+555*scale} rx={105*scale} ry={18*scale} fill="#161d27" opacity=".31"/>
     <g transform={`translate(${motion} ${y}) scale(${scale})`}>
       <Odysseus time={t} pose={actorPose} speed={speed} night={shot===1||shot===3}/>
     </g>
     {[0,1,2,3,4,5].map(i=><circle key={i}
       cx={motion+176*scale - i*77} cy={y+548*scale-(i%2)*12}
       r={3+i%4} fill={shot===3?'#cdd5dd':'#d6b590'} opacity={.27*Math.max(0,1-i/6)}/>)}
    </svg>
    <div style={{position:'absolute',top:128,left:65,right:40,fontFamily:'Arial,sans-serif',fontSize:38,fontWeight:800,letterSpacing:3,color:'#fbe6bf',textShadow:'0 4px 20px #101920'}}>ODISSEIA · TESTE DE ANIMAÇÃO 4K/60 FPS</div>
    <div style={{position:'absolute',top:202,left:67,right:30,fontFamily:'Arial,sans-serif',fontSize:70,fontWeight:900,color:'#fff7e6',textShadow:'0 5px 16px #17202a'}}>{p.name}</div>
    <div style={{position:'absolute',bottom:144,left:65,right:65,background:'#101c26bb',padding:'19px 26px',fontFamily:'Arial,sans-serif',fontSize:38,fontWeight:700,color:'#f9e0ba',textAlign:'center'}}>
      {['Passo completo · joelho e pé de apoio','Aproximação furtiva · peso corporal','Marcha cansada · postura assimétrica','Corrida · impulsão e levantamento'][shot]}
    </div>
   </div>
 </AbsoluteFill>;
};
