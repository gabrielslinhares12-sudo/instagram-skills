import React from 'react';
import type {Scene} from './schema';
// Original vector scenery for the technical demo, not documentary imagery.
export const Scenery:React.FC<{kind:Scene['environment'];time:number}>=({kind,time})=>{
 return <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>
  <defs>
   <linearGradient id="paper" x2="0.7" y2="1"><stop stopColor="#fff9e9"/><stop offset="1" stopColor="#cdbfa4"/></linearGradient>
   <linearGradient id="glass" x2="1" y2="1"><stop stopColor="#e2f5ee"/><stop offset="1" stopColor="#77a5a0"/></linearGradient>
   <radialGradient id="light"><stop stopColor="#ffe690" stopOpacity=".9"/><stop offset="1" stopColor="#ffe690" stopOpacity="0"/></radialGradient>
   <pattern id="grid" width="90" height="90" patternUnits="userSpaceOnUse"><path d="M90 0H0V90" fill="none" stroke="#93836c" strokeOpacity=".12" strokeWidth="2"/></pattern>
  </defs>
  <rect width="1080" height="1920" fill="url(#paper)"/><rect width="1080" height="1920" fill="url(#grid)"/>
  {kind==='laboratory'&&<>
   <path d="M0 1300L1080 1140V1920H0Z" fill="#b7a58b"/>
   <rect x="60" y="450" width="580" height="760" rx="220" fill="#5f6f68"/>
   <rect x="87" y="475" width="526" height="710" rx="200" fill="url(#glass)"/>
   <path d="M350 475V1190M85 840H615" stroke="#efe3c9" strokeWidth="22"/>
   <path d="M0 1270L830 1125L1110 1290L140 1490Z" fill="#eee3cc" stroke="#b9a88c" strokeWidth="8"/>
   <path d="M140 1490V1920M950 1350V1920" stroke="#82715b" strokeWidth="32"/>
   <g transform={`translate(240 1050) rotate(${Math.sin(time)*2})`}>
    <path d="M-30 -170H30V-70L110 100Q120 125 90 130H-90Q-120 125 -110 100L-30 -70Z" fill="#e2f2e8" stroke="#526b65" strokeWidth="10"/>
    <path d="M-64 20H64L100 100Q104 115 80 116H-80Q-104 115 -100 100Z" fill="#00b4bc" opacity=".7"/>
    {[0,1,2].map(i=><circle key={i} cx={-25+i*25} cy={60-((time*36+i*30)%100)} r="8" fill="#fff" opacity=".7"/>)}
   </g>
   <g transform="translate(725 570)"><circle r="135" fill="#eee4cf" stroke="#b49b6b" strokeWidth="10"/><path d="M0 -95V0L70 30" fill="none" stroke="#605747" strokeWidth="8"/></g>
  </>}
  {kind==='city'&&<>
   <circle cx="840" cy="560" r="220" fill="url(#light)"/>
   {[0,1,2,3,4].map(i=><g key={i} transform={`translate(${i*245-80} ${700+(i%2)*100})`}>
    <rect width="210" height="710" fill={i%2?'#9fafa7':'#c7b89d'} stroke="#887e68" strokeWidth="6"/>
    {[0,1,2,3,4].map(j=><g key={j}><rect x="28" y={45+j*125} width="55" height="80" fill="#f9ebc7"/><rect x="125" y={45+j*125} width="55" height="80" fill="#667b79"/></g>)}
   </g>)}
   <path d="M0 1430H1080V1920H0Z" fill="#a59e8c"/><path d="M0 1540H1080" stroke="#eee4cd" strokeWidth="24"/>
   <path d="M850 690V1530" stroke="#4b5953" strokeWidth="20"/><path d="M790 690Q850 580 910 690Z" fill="#4b5953"/><circle cx="850" cy="690" r="35" fill="#ffdc73"/>
   <g transform={`translate(${(time*95)%1500-180} 1390)`}><rect width="200" height="90" rx="25" fill="#bb4740"/><rect x="40" y="-55" width="115" height="65" rx="20" fill="#bb4740"/><circle cx="45" cy="90" r="23" fill="#3e4743"/><circle cx="160" cy="90" r="23" fill="#3e4743"/></g>
  </>}
  {kind==='observatory'&&<>
   <path d="M80 1260V780A460 460 0 0 1 920 780V1260Z" fill="#577376" stroke="#d7c7a8" strokeWidth="32"/>
   <path d="M110 1250V790A425 425 0 0 1 890 790V1250Z" fill="#789898"/>
   {[0,1,2,3,4,5,6,7,8,9,10,11].map(i=><circle key={i} cx={170+(i*137)%680} cy={560+(i*97)%580} r={i%3+2} fill="#fff6d9" opacity={.5+.4*Math.sin(time+i)**2}/>)}
   <circle cx="710" cy="690" r="77" fill="#f6e5b4"/>
   <path d="M0 1400L1080 1280V1920H0Z" fill="#b3a38a"/>
   <g transform={`translate(350 1110) rotate(${-25+Math.sin(time)*2})`}><rect x="-200" y="-70" width="400" height="140" rx="35" fill="#d6c39f" stroke="#847055" strokeWidth="10"/><ellipse cx="200" rx="20" ry="65" fill="#395b62"/><rect x="-50" y="65" width="70" height="85" fill="#8b785e"/></g>
   <path d="M350 1240L180 1630M350 1240L520 1610M350 1240L350 1680" stroke="#796a55" strokeWidth="20"/>
  </>}
  <path d="M0 1700Q450 1600 1080 1720V1920H0Z" fill="#f7eedb" opacity=".94"/>
 </svg>;
};
