import React from 'react';
import {AbsoluteFill,interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {LuminoPuppet,sampleActor} from './actors/LuminoPuppet';
import {actorDrift,leverAngle,leverGripWrist,leverKnob,leverPivot,leverProgress,remap} from './actors/stageAction';
const smooth=(x:number)=>{const t=Math.min(1,Math.max(0,x));return t*t*(3-2*t)};

/**
 * A single coherent dramatic action.
 * 0-2.5: arrive/scan; 2.5-5.7: physically raise magnifier to clue;
 * 5.7-8: reach lever with right glove; 8-10: hatch opens; react.
 * The set moves when the actor acts. No sticker PNG is rendered.
 */
export const LuminoActorTest:React.FC=()=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig(),t=frame/fps;
 const arrive=remap(t,.05,1.65),inspect=remap(t,2.45,3.8);
 const pull=leverProgress(t),open=remap(t,7.92,8.83);
 const shutter=remap(t,8.0,8.85);
 const drift=actorDrift(t); const knob=leverKnob(t);
 const light=1+open*.35; const steam=130+Math.sin(t*3)*12;
 const magnify=Math.min(remap(t,2.7,3.7),1-remap(t,5.65,6.15));
 return <AbsoluteFill style={{backgroundColor:'#07151c'}}>
 <svg width="100%" height="100%" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
  <defs>
   <linearGradient id="night" x1="0" y1="0" x2=".5" y2="1">
    <stop stopColor="#0c202e"/><stop offset=".58" stopColor="#203943"/>
    <stop offset="1" stopColor="#0e2128"/>
   </linearGradient>
   <linearGradient id="wood" x1="0" y1="0" x2="1" y2=".9">
    <stop stopColor="#8b6547"/><stop offset=".5" stopColor="#44352c"/>
    <stop offset="1" stopColor="#1d2528"/>
   </linearGradient>
   <radialGradient id="beam">
    <stop stopColor="#fff0a9" stopOpacity={.46*light}/>
    <stop offset=".72" stopColor="#eabe57" stopOpacity=".10"/>
    <stop offset="1" stopColor="#eabe57" stopOpacity="0"/>
   </radialGradient>
   <linearGradient id="door" x1="0" y1="0" x2="0" y2="1">
    <stop stopColor="#e1be6a"/><stop offset="1" stopColor="#433a2c"/>
   </linearGradient>
  </defs>
  {/* faroleiro's workroom, built in the same SVG world as the puppet */}
  <rect width="1080" height="1920" fill="url(#night)"/>
  <path d="M0 0H1080V1290L0 1470Z" fill="#273e45"/>
  <path d="M45 260L970 190V1130L45 1230Z" fill="#15303b" stroke="#897b64" strokeWidth="27"/>
  <path d="M520 212V1177M60 708L956 650" stroke="#837767" strokeWidth="23"/>
  <circle cx="775" cy="405" r="110" fill="#d7d4c2" opacity=".77"/>
  <path d="M0 1420L1080 1280V1920H0Z" fill="url(#wood)"/>
  {[0,1,2,3,4,5].map(i=><path key={i} d={'M0 '+(1460+i*100)+'L1080 '+(1320+i*100)} fill="none" stroke="#d3ae73" strokeWidth="7" opacity=".25"/>)}
  <ellipse cx="508" cy="1450" rx="300" ry="55" fill="#071015" opacity=".83"/>
  <path d="M34 1070L420 1030L440 1214L20 1260Z" fill="#604936" stroke="#1c2325" strokeWidth="22"/>
  <path d="M26 1090L421 1050" stroke="#b49768" strokeWidth="16"/>
  <path d="M67 1220L25 1620M397 1210L428 1510" stroke="#403529" strokeWidth="39"/>
  {/* A real clue (cup) moves its steam when magnifier approaches. */}
  <ellipse cx="265" cy="1090" rx="78" ry="26" fill="#c3ac80"/>
  <path d="M202 988H332V1088H202Z" fill="#b9d4cd" stroke="#405559" strokeWidth="8"/>
  <path d="M333 1014Q402 1001 368 1062Q341 1095 328 1056" fill="none" stroke="#b9d4cd" strokeWidth="15"/>
  {[0,1,2].map(i=><path key={i}
    d={'M'+(222+i*38)+' '+(965-i*12)+'Q'+(204+i*40)+' '+(914-steam*.13)+' '+(233+i*38)+' '+(873-steam*.18)}
    fill="none" stroke="#edf5e9" opacity={(.18+inspect*.40)*(1-i*.17)} strokeWidth="11"/>)}
  <circle cx="264" cy="1000" r={65+inspect*35} fill="none" stroke="#f8d77c" strokeWidth="5" opacity={inspect*.45}/>
  {/* Solid control pedestal; the handle tip follows the gloved finger precisely. */}
  <ellipse cx="905" cy="1320" rx="104" ry="27" fill="#050f15" opacity=".7"/>
  <rect x="827" y="1249" width="162" height="75" rx="18"
    fill="#473c30" stroke="#bca06d" strokeWidth="14"/>
  <circle cx={leverPivot.x} cy={leverPivot.y} r="37"
    fill="#47372a" stroke="#f0c777" strokeWidth="11"/>
  <g transform={'translate('+leverPivot.x+' '+leverPivot.y+') rotate('+leverAngle(t)+')'}>
    <path d="M0 -5V-108" stroke="#2c241e" strokeWidth="37" strokeLinecap="round"/>
    <path d="M0 -5V-108" stroke="#cfaf72" strokeWidth="22" strokeLinecap="round"/>
    <path d="M-6 -102L-6 -22" stroke="#fff1b6" strokeWidth="5" opacity=".45"/>
    <circle cy="-108" r="36" fill="#f2cb70" stroke="#342717" strokeWidth="12"/>
    <circle cx="-11" cy="-120" r="11" fill="#fff7d1" opacity=".72"/>
  </g>
  {/* A hatch with measurable depth, glowing descent and visible stair treads. */}
  <path d="M690 1432L1080 1387L1080 1848L685 1884Z"
    fill="#030c11" stroke="#947958" strokeWidth="22"/>
  {open>0&&<>
    <path d="M705 1459L1060 1417L1060 1820L705 1856Z"
      fill="#f3bd63" opacity={open*.26}/>
    {[0,1,2,3,4].map(i=><path key={i}
      d={'M'+(748+i*10)+' '+(1510+i*63)+'L'+(1018-i*12)+' '+(1481+i*59)}
      stroke="#d9ab6b" strokeWidth={12-i} opacity={open*(.8-i*.11)}/>)}
    <path d="M770 1490L780 1832M986 1465L962 1818"
      stroke="#a98761" strokeWidth="11" opacity={open*.84}/>
    <path d="M730 1465L975 1437L1015 1590Z"
      fill="#ffe1a2" opacity={open*.12}/>
  </>}
  <g transform={'translate(1080 1396) rotate('+(-open*40)+') translate(-1080 -1396)'}>
    <path d="M690 1450L1080 1396L1080 1472L691 1560Z"
      fill="url(#door)" stroke="#ddb56c" strokeWidth="17"/>
    {[0,1,2].map(i=><path key={i}
      d={'M'+(725+i*106)+' '+(1465-i*15)+'L'+(728+i*106)+' '+(1512-i*16)}
      stroke="#362b21" opacity=".42" strokeWidth="10"/>)}
  </g>
  <ellipse cx="480" cy="1020" rx="510" ry="690"
    fill="url(#beam)" opacity={1+open*.3}/>
  <ellipse cx="270" cy="1002" rx={42+magnify*24} ry={29+magnify*19}
    fill="#fff7c5" opacity={magnify*.23}/>
  <path d="M220 1002L320 998" stroke="#ffe7a8"
    strokeWidth="6" opacity={magnify*.5}/>
  {/* Shared local coordinate system: character's hand reaches the actual lever. */}
  <g transform={'translate('+(115+drift)+' 652) scale(1.05)'}>
    <LuminoPuppet time={t} gesture="demo" darkness={shutter*.3}/>
  </g>
  {/* The near side of the lever passes in front of the glove during contact. */}
  <circle cx={knob.x} cy={knob.y} r="22" fill="#ffe5a0"
    stroke="#6f522b" strokeWidth="7" opacity={remap(t,6.4,6.85)*(1-remap(t,8.15,8.7))}/>
  <circle cx={knob.x} cy={knob.y} r="42" fill="none" stroke="#ffedb0"
    strokeWidth="5" opacity={pull*(1-pull)*1.4}/>
  {/* Room foreground crosses character to give occlusion and depth. */}
  <path d="M0 1570Q400 1500 730 1590L1080 1560V1920H0Z" fill="#14242a" opacity=".45"/>
  <path d="M0 1700Q400 1660 1080 1710" stroke="#c6a777" strokeWidth="8" opacity=".23" fill="none"/>
  <path d="M0 190L1080 100" stroke="#121d23" strokeWidth="25" opacity=".8"/>
 </svg>
 <div style={{position:'absolute',top:155,left:75,right:70,
   fontSize:66,fontWeight:800,fontFamily:'sans-serif',letterSpacing:-2,
   color:'#fff3cf',textShadow:'0 4px 14px #071015',
   opacity:1-remap(t,2.0,2.7)}}>O FAROL ESCONDE UM SEGREDO.</div>
 <div style={{position:'absolute',bottom:210,left:100,right:100,textAlign:'center',
  fontFamily:'sans-serif',fontSize:44,letterSpacing:1,color:'#f8e9bd',
  textShadow:'0 4px 9px #000',opacity:Math.min(1,remap(t,.5,1.5))}}>
  {t<3?'O MISTÉRIO COMEÇA':t<6.45?'UMA PISTA NO VAPOR':t<8.35?'A ALAVANCA SE MOVE':'O ALÇAPÃO SE ABRE'}
 </div>
 </AbsoluteFill>;
};
