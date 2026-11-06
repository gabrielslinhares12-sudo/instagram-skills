import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {Odysseus} from './actors/OdysseusActor';

// Editorial-only character animation QC. No audio, publication, or claims of a finished film.
const CLIP=4, WIDTH=1080, HEIGHT=1920;
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>{const t=clamp(n);return t*t*(3-2*t);};
const blend=(a:number,b:number,t:number)=>a+(b-a)*t;

const Backdrop:React.FC<{scene:number;t:number}>=({scene,t})=>{
 const beach=scene===0,wash=scene===1,bed=scene===2;
 const colors=[['#142b43','#ca9072'],['#172432','#796456'],['#1d2934','#806c52']][scene];
 return <svg width={WIDTH} height={HEIGHT} viewBox="0 0 1080 1920"
  style={{position:'absolute',inset:0}}>
  <defs>
   <linearGradient id="home-sky" x2="0" y2="1"><stop stopColor={colors[0]}/><stop offset="1" stopColor={colors[1]}/></linearGradient>
   <radialGradient id="home-light"><stop stopColor="#ffe2a1" stopOpacity=".7"/><stop offset="1" stopColor="#ffe2a1" stopOpacity="0"/></radialGradient>
  </defs>
  <rect width="1080" height="1920" fill="url(#home-sky)"/>
  <circle cx="815" cy="430" r="390" fill="url(#home-light)"/>
  {beach&&<>
   <path d="M0 1050Q220 800 435 950T1080 925V1460H0Z" fill="#516d75"/>
   <path d="M0 1275Q400 1150 1080 1264V1920H0Z" fill="#a58a67"/>
   {[0,1,2,3,4,5,6].map(i=><path key={i} d={'M'+(-100+i*195+Math.sin(t*2+i)*15)+' '+(1210+i%3*44)+'q115 -22 210 0'} fill="none" stroke="#d2dace" strokeWidth="6" opacity=".43"/>)}
   <path d="M0 1600Q400 1475 1080 1540" fill="none" stroke="#dfc499" strokeWidth="22" opacity=".4"/>
   <path d="M0 960Q90 840 206 947T428 941" fill="none" stroke="#425861" strokeWidth="20"/>
   <path d="M0 1520H1080V1920H0Z" fill="#9c8065" opacity=".3"/>
  </>}
  {wash&&<>
   <path d="M0 470H1080V1920H0Z" fill="#6b584a"/>
   {[0,1,2,3,4].map(i=><g key={i}><rect x={i*240-75} y="380" width="154" height="1110" fill="#8e7b64" stroke="#423c39" strokeWidth="12"/><path d={'M'+(i*240-75)+' 630h154M'+(i*240-75)+' 1020h154'} stroke="#d7b790" strokeWidth="12" opacity=".45"/></g>)}
   <path d="M0 1410H1080V1920H0Z" fill="#68554d"/>
   <path d="M115 1380H965" stroke="#c3a580" strokeWidth="18"/>
  </>}
  {bed&&<>
   <rect y="470" width="1080" height="1450" fill="#604a41"/>
   {[0,1,2,3,4].map(i=><g key={i}><path d={'M'+(i*255-10)+' 430V1920'} stroke="#957153" strokeWidth="46"/><path d={'M'+(i*255+22)+' 430V1920'} stroke="#3b3230" strokeWidth="8"/></g>)}
   <path d="M80 1420H1000V1920H80Z" fill="#47362f"/>
   <path d="M150 1275H950V1510H150Z" fill="#a57d53" stroke="#3d302a" strokeWidth="22"/>
   <path d="M180 1350H920L875 1480H195Z" fill="#d8bc8f"/>
   <path d="M190 1570L195 1240M892 1570L884 1240" stroke="#795333" strokeWidth="48" strokeLinecap="round"/>
   <path d="M190 1285Q216 1060 400 1020" stroke="#5a4b36" strokeWidth="45" fill="none"/>
   {[0,1,2,3,4].map(i=><ellipse key={i} cx={230+i*75+Math.sin(t*.65+i)*8} cy={1044+i%2*15} rx="77" ry="35" fill="#657358"/>)}
   <path d="M0 1520H1080V1920H0Z" fill="#876b53" opacity=".36"/>
  </>}
  {[0,1,2,3,4,5,6].map(i=><ellipse key={i} cx={i*171+32} cy={1650+i%3*64} rx={12+i%3*4} ry="3" fill="#e6c7a5" opacity=".17"/>)}
 </svg>;
};

const Argos:React.FC<{t:number}>=({t})=>{
 const lift=ease((t-.4)/1.4),tail=Math.sin(t*10)*lift*22;
 return <g transform={'translate('+(260+lift*38)+' '+(1485-lift*15)+')'}>
  <ellipse cx="-4" cy="25" rx="204" ry="22" opacity=".3" fill="#242d31"/>
  <path d="M-147 -127Q-215 -180 -242 -120" fill="none" stroke="#826144" strokeWidth="32" strokeLinecap="round" transform={'rotate('+tail+' -147 -127)'}/>
  {[[-126,0],[-44,15],[79,-5],[120,7]].map(([x,v],i)=><path key={i} d={'M'+x+' -104q'+v+' 66 '+(v-4)+' 108'} stroke="#9d774c" strokeWidth="30" strokeLinecap="round" fill="none"/>)}
  <path d="M-155 -206Q-45 -255 106 -202L153 -111Q-5 -67 -155 -122Z" fill="#bb9868" stroke="#52483e" strokeWidth="8"/>
  <path d="M-106 -201Q-12 -232 84 -184" fill="none" stroke="#e2bb81" strokeWidth="10"/>
  <g transform={'translate(146 -174) rotate('+(-13+lift*25)+')'}>
   <path d="M-40 -33L-54 -102Q-29 -112 -16 -69" fill="#84613f"/>
   <path d="M32 -32L41 -99Q65 -106 75 -84L69 -23" fill="#84613f"/>
   <ellipse rx="73" ry="68" fill="#b18d5e" stroke="#524537" strokeWidth="8"/>
   <ellipse cx="-25" cy="-17" rx="7" ry="10" fill="#25292c"/>
   <ellipse cx="39" cy="-19" rx="7" ry="10" fill="#25292c"/>
   <ellipse cx="23" cy="21" rx="21" ry="12" fill="#403635"/>
   <path d="M-38 9Q0 40 43 9" stroke="#dfc39d" fill="none" strokeWidth="10"/>
  </g>
 </g>;
};

const Penelope:React.FC<{x:number;t:number}>=({x,t})=>{
 const step=ease((t-2)/1.4),reach=ease((t-2.65)/.8);
 return <g transform={'translate('+(x+step*75)+' 1640) scale(1.45)'}>
   <ellipse cx="0" cy="24" rx="95" ry="16" fill="#262930" opacity=".3"/>
   <path d="M-65 -235L-98 0H101L73 -235Z" fill="#31545a" stroke="#1b343b" strokeWidth="11"/>
   <path d="M-49 -229L-75 -3M49 -229L73 -3" fill="none" stroke="#d6b886" strokeWidth="9"/>
   <path d="M-93 -218Q-157 -179 -142 -106" fill="none" stroke="#31545a" strokeWidth="34" strokeLinecap="round"/>
   <path d="M-142 -107Q-134 -72 -102 -52" fill="none" stroke="#d6a384" strokeWidth="23" strokeLinecap="round"/>
   <circle cx="-102" cy="-52" r="18" fill="#d6a384"/>
   <path d={'M70 -223Q128 -188 '+(118+reach*60)+' '+(-105-reach*90)} fill="none" stroke="#31545a" strokeWidth="34" strokeLinecap="round"/>
   <circle cx={118+reach*60} cy={-105-reach*90} r="17" fill="#d6a384"/>
   <path d="M-46 -260H48V-230H-46Z" fill="#c89476"/>
   <path d="M-78 -317Q-104 -228 -81 -169H-46L-38 -290Z M67 -316Q103 -256 82 -168H51L38 -291Z" fill="#292632"/>
   <ellipse cx="0" cy="-316" rx="71" ry="85" fill="#d7a484" stroke="#4d3530" strokeWidth="8"/>
   <path d="M-69 -319Q-62 -420 38 -395Q82 -368 72 -311L47 -359Q-30 -362 -69 -319Z" fill="#27232f"/>
   <path d="M-50 -316l22 -5M19 -319l23 5" stroke="#47332d" strokeWidth="7"/>
   <circle cx="-31" cy="-307" r="5" fill="#29272e"/><circle cx="33" cy="-307" r="5" fill="#29272e"/>
   <path d="M0 -305l-8 25 12 5" fill="none" stroke="#a8735c" strokeWidth="5"/>
   <path d="M-22 -257Q0 -248 22 -259" fill="none" stroke="#67443b" strokeWidth="5"/>
 </g>;
};

const Eurycleia:React.FC<{t:number}>=({t})=>{
 const reach=ease((t-.35)/1.6),surprise=ease((t-2.5)/.5);
 return <g transform={'translate(445 '+(1650-surprise*28)+') scale(1.42)'}>
  <ellipse cy="20" rx="80" ry="15" fill="#27262a" opacity=".3"/>
  <path d="M-67 -203L-99 12H98L75 -203Z" fill="#6c505b" stroke="#39313b" strokeWidth="9"/>
  <path d="M-46 -211L-58 -8M49 -206L70 -8" stroke="#c4a68f" strokeWidth="7" fill="none"/>
  <path d="M-78 -209Q-110 -155 -110 -103" stroke="#6c505b" strokeWidth="33" fill="none" strokeLinecap="round"/>
  <path d={'M-106 -102Q'+(-60+reach*45)+' '+(-67+reach*18)+' '+(55+reach*30)+' '+(-170+reach*70)} stroke="#c39e8b" strokeWidth="21" fill="none" strokeLinecap="round"/>
  <circle cx={55+reach*30} cy={-170+reach*70} r="16" fill="#c39e8b"/>
  <path d="M73 -208Q122 -166 116 -96" stroke="#6c505b" strokeWidth="30" fill="none" strokeLinecap="round"/>
  <circle cx="119" cy="-94" r="17" fill="#c39e8b"/>
  <path d="M-44 -256H47V-210H-44Z" fill="#c39e8b"/>
  <ellipse cy="-305" rx="65" ry="79" fill="#c5a18d" stroke="#533a38" strokeWidth="8"/>
  <path d="M-65 -311Q-52 -403 42 -374L67 -303Q20 -350 -65 -311Z" fill="#d6d1c7"/>
  <path d="M-52 -307l25 -6M18 -313l25 4" stroke="#63504b" strokeWidth="7"/>
  <circle cx="-31" cy="-294" r="5" fill="#26262d"/><circle cx="29" cy="-294" r="5" fill="#26262d"/>
  <path d="M-11 -276l11 12 9 -11" fill="none" stroke="#977163" strokeWidth="5"/>
  <path d={surprise>.2?'M-16 -252Q0 -239 18 -251':'M-19 -254Q0 -261 17 -256'} stroke="#684b43" strokeWidth="5" fill="none"/>
 </g>;
};

const Basin:React.FC<{t:number}>=({t})=><g transform="translate(575 1510)">
 <ellipse cy="70" rx="248" ry="33" fill="#302b31" opacity=".27"/>
 <path d="M-233 0Q-192 189 0 207Q195 180 233 0Z" fill="#ae7f5b" stroke="#513b30" strokeWidth="13"/>
 <ellipse ry="64" rx="233" fill="#e1b58d" stroke="#594032" strokeWidth="13"/>
 <ellipse ry={45+Math.sin(t*9)*4} rx="205" fill="#61999b" stroke="#b8e6d6" strokeWidth="5"/>
 {[0,1,2].map(i=><ellipse key={i} cx={-100+i*94} cy="8" rx={36+14*Math.sin(t*4+i)} ry="7" fill="none" stroke="#c0dddc" strokeWidth="4"/>)}
 </g>;

export const OdysseyHomeQC:React.FC=()=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig(),at=frame/fps;
 const shot=Math.min(2,Math.floor(at/CLIP)),t=at-shot*CLIP;
 const alpha=clamp(Math.min(t/.25,(CLIP-t)/.30));
 return <AbsoluteFill style={{background:'#172735'}}>
  <div style={{position:'absolute',inset:0,opacity:alpha}}>
   <Backdrop scene={shot} t={t}/>
   <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
    {shot===0&&<>
      <Argos t={t}/>
      <g transform={'translate('+(505-ease((t-1.9)/1.4)*35)+' 600) scale(1.52)'}>
        <Odysseus time={t} pose="pet" civilian/>
      </g>
    </>}
    {shot===1&&<>
      <g transform="translate(420 790) scale(1.27)">
        <Odysseus time={t} pose="listen" civilian/>
      </g>
      <path d="M590 1370Q550 1440 555 1490" stroke="#ad8264" strokeWidth="40" strokeLinecap="round" fill="none"/>
      <path d="M606 1483l-22 12m35 -13l-23 20" stroke="#8d5450" strokeWidth="8"/>
      <Basin t={t}/>
      <Eurycleia t={t}/>
    </>}
    {shot===2&&<>
      <g transform={'translate('+(560-ease((t-1.5)/1.5)*195)+' 840) scale(1.35)'}>
        <Odysseus time={t} pose="embrace" civilian/>
      </g>
      <Penelope x={240} t={t}/>
    </>}
   </svg>
  </div>
 </AbsoluteFill>;
};
