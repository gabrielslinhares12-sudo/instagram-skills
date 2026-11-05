import React from 'react';
import {AbsoluteFill,interpolate,useCurrentFrame,useVideoConfig} from 'remotion';
import {LuminoPuppet} from './actors/LuminoPuppet';
const smooth=(x:number)=>{const t=Math.min(1,Math.max(0,x));return t*t*(3-2*t)};
const remap=(t:number,a:number,b:number)=>smooth((t-a)/(b-a));
/**
 * A single coherent dramatic action.
 * 0-2.5: arrive/scan; 2.5-5.7: physically raise magnifier to clue;
 * 5.7-8: reach lever with right glove; 8-10: hatch opens; react.
 * The set moves when the actor acts. No sticker PNG is rendered.
 */
export const LuminoActorTest:React.FC=()=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig(),t=frame/fps;
 const arrive=remap(t,.05,1.65),inspect=remap(t,2.45,3.8);
 const pull=remap(t,6.5,7.55),open=remap(t,7.52,8.35);
 const shutter=remap(t,8.0,8.85);
 const drift=interpolate(t,[0,2.8,6.0,9.5],[-180,0,0,-40],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 const light=1+open*.35; const steam=130+Math.sin(t*3)*12;
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
  {/* Lever and hatch are causally linked to the character's right-hand gesture. */}
  <g transform={'translate(830 1185) rotate('+(-27+pull*67)+')'}>
    <rect x="-20" y="-98" width="39" height="126" rx="13" fill="#aa8452" stroke="#31271e" strokeWidth="12"/>
    <circle cy="-106" r="39" fill="#f4cc62" stroke="#4d321d" strokeWidth="13"/>
  </g>
  <rect x="725" y="1170" width="205" height="62" rx="14" fill="#4c3c2c" stroke="#c4a76a" strokeWidth="15"/>
  <path d="M700 1445L1080 1395L1080 1830L690 1865Z" fill="#070f14" stroke="#947958" strokeWidth="21"/>
  <path d={'M692 1450L1080 1405L1080 '+(1408-open*210)+'L690 '+(1460-open*210)+'Z'} fill="url(#door)" stroke="#dfb56a" strokeWidth="15"/>
  {open>0&&<path d={'M695 1475L1070 1443L1070 1870L700 1875Z'} fill="#ffcc69" opacity={open*.22}/>}
  <ellipse cx="480" cy="1020" rx="510" ry="690" fill="url(#beam)" opacity={1+open*.3}/>
  {/* Shared local coordinate system: character's hand reaches the actual lever. */}
  <g transform={'translate('+(115+drift)+' 652) scale(1.05)'}>
    <LuminoPuppet time={t} gesture="demo" darkness={shutter*.3}/>
  </g>
  {/* Room foreground crosses character to give occlusion and depth. */}
  <path d="M0 1570Q400 1500 730 1590L1080 1560V1920H0Z" fill="#14242a" opacity=".45"/>
  <path d="M0 1700Q400 1660 1080 1710" stroke="#c6a777" strokeWidth="8" opacity=".23" fill="none"/>
  <path d="M0 190L1080 100" stroke="#121d23" strokeWidth="25" opacity=".8"/>
 </svg>
 <div style={{position:'absolute',top:155,left:75,right:70,
   fontSize:72,fontWeight:800,fontFamily:'sans-serif',letterSpacing:-2,
   color:'#fff3cf',textShadow:'0 4px 14px #071015',
   opacity:1-remap(t,2.0,2.7)}}>O FAROL ESCONDE UM SEGREDO.</div>
 <div style={{position:'absolute',bottom:210,left:100,right:100,textAlign:'center',
  fontFamily:'sans-serif',fontSize:44,letterSpacing:1,color:'#f8e9bd',
  textShadow:'0 4px 9px #000',opacity:Math.min(1,remap(t,.5,1.5))}}>
  {t<3?'ELE ENTRA NA CENA':t<6.3?'INVESTIGA UMA PISTA':t<8.3?'ACIONA O MECANISMO':'O MUNDO REAGE'}
 </div>
 </AbsoluteFill>;
};
