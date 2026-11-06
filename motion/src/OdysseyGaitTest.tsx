import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {Odysseus} from './actors/OdysseusActor';
import {kneeIK,sampleGait} from './actors/gait';

const clamp=(x:number)=>Math.min(1,Math.max(0,x));
const smooth=(x:number)=>{const a=clamp(x);return a*a*(3-2*a)};
const Crew:React.FC<{t:number;speed:number;variant:0|1|2;phase:number}>=({t,speed,variant,phase})=>{
 const gait=sampleGait(t+phase,'walk',speed,440),skin=['#d29c75','#b68163','#d2aa88'][variant];
 const body=['#445b55','#735554','#685943'][variant];
 const hair=['#292826','#44302e','#55412d'][variant];
 const faceShape=variant===2?'M94 136Q123 100 156 135L159 177Q125 213 92 181Z':'M94 135Q124 109 154 134L156 179Q123 215 92 178Z';
 const legs=([[-1,gait.left],[1,gait.right]] as const).map(([side,foot],i)=>{
  const hip={x:124+side*23,y:330+gait.bodyY},ankle={x:124+side*22+foot.ankle.x,y:foot.ankle.y};
  const knee=kneeIK(hip,ankle,67,66,-1);
  return <g key={i}><path d={`M${hip.x} ${hip.y}L${knee.x} ${knee.y}L${ankle.x} ${ankle.y}`}
   stroke="#332b28" strokeWidth="22" strokeLinejoin="round" strokeLinecap="round" fill="none"/>
   <path d={`M${hip.x} ${hip.y}L${knee.x} ${knee.y}L${ankle.x} ${ankle.y}`}
    stroke={skin} strokeWidth="15" strokeLinejoin="round" strokeLinecap="round" fill="none"/>
   <ellipse cx={ankle.x+12} cy={ankle.y+7} rx="29" ry="10" fill="#3d2b27"/>
   <circle cx={knee.x} cy={knee.y} r="12" fill="#9f775d"/>
  </g>;
 });
 const nod=Math.sin(t*1.4+phase)*1.5;
 return <svg width="255" height="480" viewBox="0 0 255 480" style={{overflow:'visible'}}>
  <ellipse cx="130" cy="455" rx="69" ry="13" fill="#1f343a" opacity=".33"/>
  {legs}
  <g transform={`translate(125 318) rotate(${gait.lean}) translate(-125 -318)`}>
   <path d="M80 250Q75 287 91 339L155 338Q172 273 166 250Z" fill={body} stroke="#302b2c" strokeWidth="8"/>
   <path d="M92 260L153 260M101 283L146 280M94 308L157 305" stroke="#d8b881" opacity=".52" strokeWidth="5"/>
   {[[-1,-gait.armPhase],[1,gait.armPhase]].map(([side,arm],i)=>
   <g key={i}><path d={`M${125+side*45} 261Q${125+side*72} 304 ${125+side*(74+arm*22)} ${342+arm*17}`}
     stroke="#302b2c" strokeWidth="23" fill="none" strokeLinecap="round"/>
    <path d={`M${125+side*45} 261Q${125+side*72} 304 ${125+side*(74+arm*22)} ${342+arm*17}`}
    stroke={skin} strokeWidth="16" fill="none" strokeLinecap="round"/></g>)}
   <path d="M114 203V234" stroke={skin} strokeWidth="25"/>
   <g transform={`translate(0 ${nod})`}>
    <path d={faceShape} fill={skin} stroke="#312928" strokeWidth="8"/>
    <path d={variant===0?'M87 137Q98 86 150 111L159 139Q136 116 93 147Z':
     variant===1?'M88 134Q109 98 154 122L158 145Q123 134 95 147Z':'M93 133Q124 82 155 132L143 128L134 117L104 137Z'}
       fill={hair}/>
    {variant===1&&<path d="M100 178Q129 194 151 176L140 203L111 200Z" fill={hair}/>}
    <circle cx="109" cy="158" r="4" fill="#1c2226"/><circle cx="143" cy="158" r="4" fill="#1c2226"/>
    <path d="M119 184Q128 188 138 183" stroke="#744e3a" strokeWidth="3" fill="none"/>
   </g>
  </g></svg>;
};

const background=(t:number,close:boolean)=> <g>
 <defs>
  <linearGradient id="od-sky" x1="0" x2="0" y1="0" y2="1">
   <stop stopColor="#173349"/><stop offset=".58" stopColor="#526d77"/><stop offset="1" stopColor="#de9f7b"/>
  </linearGradient>
  <linearGradient id="od-water" x1="0" y1="0" x2="0" y2="1">
   <stop stopColor="#467382"/><stop offset="1" stopColor="#162d42"/>
  </linearGradient>
 </defs>
 <rect width="1080" height="1920" fill="url(#od-sky)"/>
 <circle cx={811-t*3} cy="346" r="139" fill="#ffdb9a"/>
 {[0,1,2,3,4].map(i=><path key={i} d={`M${-130+i*273-t*(i+4)} ${326+i*76}q80 -24 154 0q-50 9 -154 0`}
  stroke="#e3ece7" strokeWidth="4" opacity=".22" fill="none"/>)}
 <path d="M0 1090Q210 1010 427 1085T1080 1093L1080 1920H0Z" fill="#52666b"/>
 <path d="M0 1240Q295 1107 530 1260T1080 1200V1920H0Z" fill="#75827b"/>
 {close?<g>
   <rect y="1244" width="1080" height="676" fill="url(#od-water)"/>
 </g>:<g>
  <path d="M0 1380H1080V1920H0Z" fill="url(#od-water)"/>
  {[0,1,2,3,4,5].map(i=><g key={i}>
    <rect x={i*235-60} y={850+i%3*52} width="98" height="690" fill="#9f8066" stroke="#554a40" strokeWidth="10"/>
    <rect x={i*235-90} y={833+i%3*52} width="154" height="31" fill="#bb9777" stroke="#5c4940" strokeWidth="8"/>
    <path d={`M${i*235-50} 990V1350`} stroke="#d9b28d" strokeWidth="8"/>
  </g>)}
  <path d="M0 1555H1080V1920H0Z" fill="#7d6854"/>
  {[0,1,2,3,4].map(i=><path key={i} d={`M0 ${1590+i*75}H1080`} stroke="#c3a27f" strokeWidth="8" opacity=".3"/>)}
 </g>}
 {[0,1,2,3].map(i=><g key={i}>
  {Array.from({length:15},(_,j)=><path key={j} d={`M${((j*172+i*151+t*(39+i*9))%1320)-190} ${1440+i*86+j%3*19}q45 -10 94 0`}
    stroke="#e2e0cf" strokeWidth="3" opacity={.12+i*.04} fill="none"/>)}
 </g>)}
 </g>;

const Ship:React.FC<{t:number;close:boolean}>=({t,close})=>{
 const x=close?575:807,y=(close?1334:1465)+Math.sin(t*2)*7,sc=close?1.6:.88,flap=Math.sin(t*2.7)*31;
 return <g transform={`translate(${x} ${y}) scale(${sc})`}>
  <path d="M-290 -18H270L184 88Q0 130 -205 90Z" fill="#785339" stroke="#392f2b" strokeWidth="17"/>
  <path d="M-276 1H251" stroke="#deb87e" strokeWidth="14"/>
  {[0,1,2,3,4,5,6,7,8].map(i=><g key={i}>
   <path d={`M${-245+i*55} 9L${-247+i*55} 83`} stroke="#c9a171" strokeWidth="8"/>
   <circle cx={-243+i*55} cy="17" r="7" fill="#493d32"/>
  </g>)}
  <path d="M0 -8V-347" stroke="#d0ad7b" strokeWidth="15"/>
  <path d={`M0 -342Q${-139+flap} -268 -3 -32Z`} fill="#d9cda9" stroke="#958675" strokeWidth="9"/>
  <path d={`M0 -342Q${150-flap*.4} -261 0 -34Z`} fill="#f2dfbb" stroke="#978773" strokeWidth="8"/>
  {[1,2,3].map(i=><path key={i} d={`M${-100+flap*.5} ${-297+i*61}L${101-flap*.4} ${-307+i*61}`}
    stroke="#968f80" strokeWidth="3" opacity=".42"/>)}
  {[0,1,2,3].map(i=><g key={i} transform={`translate(${-220+i*126} 10) rotate(${Math.sin(t*3.8+i)*15})`}>
    <path d="M0 0L-51 146" stroke="#aa7852" strokeWidth="13"/>
    <ellipse cx="-52" cy="152" rx="13" ry="34" fill="#b18c65"/>
  </g>)}
 </g>;
};

export const OdysseyGaitTest:React.FC=()=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig(),t=frame/fps,close=t>=4,local=close?t-4:t;
 const heroX=close?110+local*67:68+t*93;
 const heroY=close?665:773,scale=close?1.53:1.42;
 return <AbsoluteFill style={{background:'#132b3a'}}>
  <svg width="100%" height="100%" viewBox="0 0 1080 1920">
    {background(t,close)}
    <Ship t={t} close={close}/>
    {!close&&<>
      <g transform={`translate(${60+t*72} 1161) scale(.59)`}>
       <Crew t={t} phase={.12} speed={72/.59} variant={0}/>
      </g>
      <g transform={`translate(${298+t*63} 1189) scale(.69)`}>
       <Crew t={t} phase={.39} speed={63/.69} variant={1}/>
      </g>
      <g transform={`translate(${496+t*47} 1214) scale(.51)`}>
       <Crew t={t} phase={.63} speed={47/.51} variant={2}/>
      </g>
    </>}
    {close&&<>
      <g transform={`translate(742 1310) scale(1.0)`}><Crew t={local} phase={.3} speed={0} variant={2}/></g>
    </>}
    <g transform={`translate(${heroX} ${heroY}) scale(${scale})`}>
      <Odysseus time={local} pose="walk" speed={close?67/1.53:93/1.42}/>
    </g>
    <path d="M0 1698Q364 1641 1080 1688V1920H0Z" fill="#79624f" opacity=".33"/>
    {Array.from({length:25},(_,i)=><circle key={i} cx={(i*83+t*73)%1140-30} cy={1440+(i*47)%385}
     r={1.7+i%3} fill="#ffe2b6" opacity={.18+i%4*.05}/>)}
  </svg>
  <div style={{position:'absolute',top:110,left:76,color:'#f1dfb4',fontSize:35,fontFamily:'Georgia,serif',
     letterSpacing:3,textShadow:'0 2px 6px #0d2231'}}>A ODISSEIA · REVISÃO DO ANDAR</div>
  <div style={{position:'absolute',bottom:72,left:77,right:77,textAlign:'center',fontSize:28,
      color:'#f5eacb',fontFamily:'Arial,sans-serif'}}>Prévia técnica · atuação articulada e cenários em movimento</div>
 </AbsoluteFill>;
};
