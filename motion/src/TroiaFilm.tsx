import React from 'react';
import {AbsoluteFill,Audio,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import {LuminoPuppet} from './actors/LuminoPuppet';
import {Odysseus,type WarriorPose} from './actors/OdysseusActor';

export const TROIA_CUES=[
 {title:'DEZ ANOS DE GUERRA',text:'Dez anos de guerra, e Troia continuava de pé. Nenhum ataque atravessava suas muralhas.'},
 {title:'UM HOMEM, UMA IDEIA',text:'Mas um guerreiro grego tinha uma ideia que mudaria tudo. Seu nome era Odisseu.'},
 {title:'O PLANO IMPOSSÍVEL',text:'Segundo a mitologia, ele imaginou um cavalo gigante de madeira, completamente oco por dentro.'},
 {title:'A ARMADILHA',text:'Os melhores guerreiros entraram escondidos. Do lado de fora, os gregos fingiram abandonar a guerra.'},
 {title:'UM PRESENTE SUSPEITO',text:'Os troianos encontraram o cavalo diante dos portões e acreditaram que era uma oferenda.'},
 {title:'AS PORTAS DE TROIA',text:'Sem perceber a armadilha, arrastaram aquele presente para dentro da cidade e comemoraram.'},
 {title:'A NOITE CAIU',text:'Quando a noite caiu, uma escotilha se abriu no ventre do cavalo.'},
 {title:'SILÊNCIO NAS RUAS',text:'Odisseu e seus companheiros saíram em silêncio e correram até os portões.'},
 {title:'OS PORTÕES ABERTOS',text:'Eles abriram as portas para o exército que havia retornado. Troia foi tomada.'},
 {title:'A MAIOR ARMA',text:'A maior arma de Odisseu não tinha lâmina. Era sua inteligência. Tem uma explicação.'}
] as const;
const ease=(n:number)=>{const x=Math.max(0,Math.min(1,n));return x*x*(3-2*x);};
const ramp=(t:number,a:number,b:number)=>ease((t-a)/(b-a));
const Sky:React.FC<{t:number;night:number}>=({t,night})=><g>
 <rect width="1080" height="1920" fill="url(#troia-sky)"/>
 <circle cx={795-t*5} cy={320+night*85} r={night>.5?105:160}
  fill={night>.5?'#d9e2e4':'#ffdf9c'} opacity=".85"/>
 {Array.from({length:55},(_,i)=><circle key={i} cx={(i*167+39)%1080}
  cy={(i*253+66)%920} r={1.5+i%3} fill="#fff9df"
  opacity={night*(.4+.3*Math.sin(t*1.4+i))}/>)}
 <path d="M0 1190Q230 1030 480 1120T1080 1110V1920H0Z"
  fill={night>.5?'#24343d':'#77736a'}/>
 <path d="M0 1440Q350 1280 620 1410T1080 1380V1920H0Z"
  fill={night>.5?'#2d353a':'#786b5c'}/>
 </g>;
const Wall:React.FC<{open:number;night:number}>=({open,night})=><g>
 <path d="M0 802L1080 754V1444H0Z" fill="#9b7e62" stroke="#4b3c31" strokeWidth="14"/>
 {[0,1,2,3,4,5,6,7,8,9].map(i=><g key={i}>
  <rect x={i*115} y={764-i*5} width="78" height="65" fill="#c5a586" stroke="#544337" strokeWidth="8"/>
  <path d={'M'+(i*115)+' 980H'+(i*115+88)} stroke="#e7c49c" strokeWidth="6" opacity=".4"/>
 </g>)}
 {[0,1].map(i=><g key={i}>
  <rect x={i?841:70} y={i?485:512} width="166" height="925"
   fill="#887059" stroke="#46372f" strokeWidth="17"/>
  <path d={'M'+(i?825:51)+' '+(i?483:512)+'l103 -103 104 103Z'}
   fill="#6e5044" stroke="#3c302c" strokeWidth="14"/>
  <rect x={i?890:120} y="720" width="54" height="138" rx="15" fill="#293643"/>
 </g>)}
 <path d="M404 1112Q540 917 676 1112V1480H404Z" fill="#081826"
  stroke="#d0b18e" strokeWidth="20"/>
 <g transform={'translate(404 1112) rotate('+(-open*58)+')'}>
  <path d="M0 0Q133 -190 133 0V368H0Z" fill="#7b5138" stroke="#362b29" strokeWidth="14"/>
  {[0,1,2].map(i=><path key={i} d={'M'+(36+i*35)+' 9V352'}
   stroke="#d6a36f" opacity=".64" strokeWidth="9"/>)}
 </g>
 <g transform={'translate(676 1112) rotate('+(open*58)+')'}>
  <path d="M0 0Q-133 -190 -133 0V368H0Z" fill="#7b5138" stroke="#362b29" strokeWidth="14"/>
  {[0,1,2].map(i=><path key={i} d={'M'+(-36-i*35)+' 9V352'}
   stroke="#d6a36f" opacity=".64" strokeWidth="9"/>)}
 </g>
 <rect y="1480" width="1080" height="440" fill="#a18563" opacity=".14"/>
 <rect width="1080" height="1920" fill="#0b1e2b" opacity={night*.33}/>
 </g>;
const Boat:React.FC<{x:number;y:number;scale:number;t:number}>=({x,y,scale,t})=>
 <g transform={'translate('+x+' '+(y+Math.sin(t*1.5+x)*5)+') scale('+scale+')'}>
  <path d="M-130 -10L120 -18L85 40Q0 71 -91 39Z"
   fill="#45362f" stroke="#2b2625" strokeWidth="11"/>
  <path d="M-10 -185V-14" stroke="#d4be91" strokeWidth="12"/>
  <path d="M-10 -176Q-105 -92 -8 -25Z" fill="#d1c9ac" stroke="#827f77" strokeWidth="7"/>
  <path d="M-9 -178Q91 -93 -8 -25Z" fill="#e2d9b3" stroke="#8f8b7c" strokeWidth="6"/>
  <path d="M-112 7H94" stroke="#ca996f" strokeWidth="8"/>
 </g>;
const Horse:React.FC<{x:number;y:number;scale:number;time:number;door:number}>=
 ({x,y,scale,time,door})=><g transform={'translate('+x+' '+y+') scale('+scale+')'}>
  <ellipse cy="12" rx="217" ry="35" fill="#11252d" opacity=".56"/>
  {[-140,136].map((v,i)=><g key={i} transform={'translate('+v+' -36)'}>
    <circle r="47" fill="#785238" stroke="#342824" strokeWidth="13"/>
    <circle r="18" fill="#e0b074" stroke="#392924" strokeWidth="8"/>
    {[0,1,2,3,4,5].map(j=><path key={j} d="M0 0V-36"
      stroke="#be9569" strokeWidth="7" transform={'rotate('+j*60+')'}/>)}
  </g>)}
  {[-110,90].map((v,i)=><path key={i} d={'M'+v+' -270L'+(v-12)+' -42L'+(v+47)+' -42L'+(v+54)+' -266Z'}
   fill="#8a6043" stroke="#342823" strokeWidth="12"/>)}
  <path d="M-180 -462Q-215 -517 -172 -552L86 -583Q212 -552 194 -420L171 -267L-169 -263Z"
   fill="#956d4c" stroke="#312723" strokeWidth="20"/>
  {[0,1,2,3].map(i=><path key={i}
   d={'M-179 '+(-457+i*55)+'L179 '+(-456+i*55)} stroke="#d1a97b"
   strokeWidth="10" opacity=".66"/>)}
  {[-131,-36,69,146].map((v,i)=><path key={i}
   d={'M'+v+' -558L'+(v+7)+' -269'} stroke="#593b2c" strokeWidth="8" opacity=".5"/>)}
  <path d="M-130 -499Q-179 -615 -155 -681Q-123 -721 -77 -680L20 -620L30 -520Z"
   fill="#936e4e" stroke="#322924" strokeWidth="18"/>
  <path d="M-119 -672L-135 -748L-64 -689M-21 -631L-59 -699L29 -661" fill="#765039"
   stroke="#312622" strokeWidth="13"/>
  <path d="M-132 -493L-214 -447L-198 -418L-90 -438Z"
   fill="#bb8f63" stroke="#342823" strokeWidth="12"/>
  <circle cx="-117" cy="-578" r="10" fill="#171f25"/>
  <path d="M192 -460L234 -494L230 -396L193 -379Z" fill="#624531" stroke="#332824" strokeWidth="11"/>
  {door>.01&&<rect x="-56" y="-475" width="140" height="169" rx="9" fill="#0a1620"/>}
  <g transform={'translate(-56 -475) rotate('+(-door*105)+') translate(56 475)'}>
    <rect x="-56" y="-475" width="140" height="169" rx="9"
     fill="#986b48" stroke="#2e2826" strokeWidth="12"/>
    <path d="M-39 -449H70M-39 -392H70M-39 -340H70"
     stroke="#d3a676" strokeWidth="8"/>
    <circle cx="61" cy="-385" r="14" fill="#e8c287" stroke="#493427" strokeWidth="5"/>
  </g>
  {[-150,-85,-20,45,110].map((v,i)=><circle key={i} cx={v} cy="-475" r="7" fill="#d7aa75"/>)}
 </g>;
const Parchment:React.FC<{time:number}>=({time})=>{
 const stroke=1350*(1-ramp(time,1,4.9));
 return <g transform="translate(72 991) rotate(-6)">
  <rect width="944" height="575" rx="24" fill="#d9bd8e" stroke="#503d2c" strokeWidth="22"/>
  <rect x="25" y="22" width="895" height="524" fill="none" stroke="#ad8f68" strokeWidth="5"/>
  <text x="69" y="91" fontFamily="Georgia,serif" fontWeight="bold" fontSize="49" fill="#593b30">A ESTRATÉGIA</text>
  <path d="M339 455L339 296L410 296L413 451M338 302Q299 176 351 158L462 216L458 298"
   stroke="#79553b" strokeDasharray="1350" strokeDashoffset={stroke} strokeWidth="19" fill="none"/>
  <path d="M348 460L348 500M410 459L417 500" stroke="#79553b" strokeWidth="19" opacity={ramp(time,2,4)}/>
  <path d="M106 285L270 288M530 286L785 288" stroke="#966d4c" strokeWidth="15" opacity={ramp(time,2,4)}/>
  <text x="80" y="532" fontFamily="Georgia,serif" fontSize="38" fill="#67513f">A força não abre todas as portas.</text>
 </g>;
};
const captions=(text:string)=>text;
export const TroiaFilm:React.FC<{voicePath?:string}>=({voicePath})=>{
 const frame=useCurrentFrame();const {fps}=useVideoConfig();
 const time=frame/fps,scene=Math.min(9,Math.floor(time/6)),t=time-scene*6;
 const night=scene>=6&&scene<=8?1:0;
 const horseX=scene===5?325+ramp(t,.7,5.5)*300:510;
 const horseScale=scene===3?1.10:1.03;
 const horseY=scene===3?1576:1570;
 const gate=scene===5?ramp(t,1,5):scene===8?ramp(t,1.7,5.6):scene===9?1:0;
 const door=scene===6?ramp(t,2.2,4.4):scene>=7?1:0;
 const role:WarriorPose=['listen','listen','plan','craft','listen','listen','climb','run','open','victory'][scene] as WarriorPose;
 const heroX=[460,225,560,640,0,0,455,190,265,420][scene];
 const heroY=[950,790,775,1320,0,0,1255,1170,1150,860][scene];
 const heroScale=[.77,1.45,.99,.65,0,0,.71,.82,.82,1.15][scene];
 const heroShift=scene===7?t*57:scene===6?ramp(t,2,5)*90:Math.sin(t*2)*3;
 const day=night>0?'#132c42':'#264658';
 return <AbsoluteFill style={{background:'#0a1b2b'}}>
 <svg width="100%" height="100%" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
 <defs>
  <linearGradient id="troia-sky" x1="0" y1="0" x2=".1" y2="1">
   <stop stopColor={night?'#081827':'#17354a'}/>
   <stop offset=".56" stopColor={night?'#1e3954':'#668190'}/>
   <stop offset="1" stopColor={night?'#48525a':'#dda36d'}/>
  </linearGradient>
  <radialGradient id="fire-light"><stop stopColor="#ffdea2" stopOpacity=".7"/>
   <stop offset="1" stopColor="#fdac63" stopOpacity="0"/></radialGradient>
  <linearGradient id="floor-troy" x1="0" y1="0" x2="0" y2="1">
    <stop stopColor="#947b5f"/><stop offset="1" stopColor="#353b3b"/>
  </linearGradient>
 </defs>
 <Sky t={time} night={night}/>
 <g transform={'translate(540 960) scale('+(1+ramp(t,0,6)*.03)+') translate(-540 -960)'}>
  {(scene===0||scene===4||scene===5||scene===8)&&<Wall open={gate} night={night}/>}
  {scene===0&&<>
   {[0,1,2,3,4].map(i=><path key={i}
    d={'M'+(i*230-60)+' 1610L'+(i*230+45)+' 1320L'+(i*230+148)+' 1610Z'}
    fill="#756153" stroke="#3b3835" strokeWidth="14"/>)}
   <path d="M0 1590H1080V1920H0Z" fill="url(#floor-troy)" opacity=".7"/>
  </>}
  {scene===1&&<path d="M0 1390Q430 1160 1080 1380V1920H0Z" fill="#525b55"/>}
  {scene===2&&<>
   <rect y="940" width="1080" height="980" fill="#343a38"/>
   <rect x="40" y="1110" width="1000" height="630" rx="29" fill="#483729" stroke="#b3976f" strokeWidth="31"/>
   <Parchment time={t}/>
  </>}
  {scene===3&&<>
   <path d="M0 1300H1080V1920H0Z" fill="#766554"/>
   {Array.from({length:4},(_,i)=><path key={i}
     d={'M'+(60+i*260)+' 1200L'+(170+i*260)+' 950L'+(260+i*260)+' 1190Z'}
     stroke="#3d3430" fill="#7a6651" strokeWidth="14"/>)}
  </>}
  {scene===4&&<>
   {[0,1,2].map(i=><Boat key={i} x={160+i*300+t*49} y={1690+i*36} scale={.7-i*.07} t={t}/>)}
  </>}
  {scene===5&&<path d="M0 1450H1080V1920H0Z" fill="#a28768" opacity=".6"/>}
  {(scene===6||scene===7)&&<>
   <path d="M0 1050H1080V1920H0Z" fill="#394951"/>
   <path d="M0 1540Q360 1460 1080 1510V1920H0Z" fill="#30363e"/>
   {Array.from({length:4},(_,i)=><g key={i}>
    <rect x={80+i*350} y="945" width="44" height="240" rx="10" fill="#584a3d" stroke="#b99d76" strokeWidth="9"/>
    <circle cx={102+i*350} cy="910" r={105+Math.sin(t*4+i)*8} fill="url(#fire-light)"/>
    <path d={'M'+(102+i*350)+' 873q-27 -66 0 -116q32 38 15 116Z'} fill="#ffd27a"/>
   </g>)}
   {scene===7&&<Wall night={1} open={0}/>}
  </>}
  {scene===8&&<>
   {[0,1,2].map(i=><Boat key={i} x={180+i*340+t*20} y={1780+i*15} scale={.47} t={t}/>)}
   {Array.from({length:7},(_,i)=><circle key={i} cx={(i*187+t*13)%1080}
    cy={1390+i*43-t*20} r={4+i%4} fill="#ffcb85" opacity=".67"/>)}
  </>}
  {scene===9&&<>
   <path d="M0 1220Q500 1100 1080 1180V1920H0Z" fill="#5a5957"/>
   <path d="M0 1470L1080 1340V1920H0Z" fill="#3f474a"/>
  </>}
  {(scene>=3&&scene<=7)&&<Horse x={horseX} y={horseY}
   time={time} door={door} scale={horseScale}/>}
  {scene===5&&<path d={'M'+(horseX+130)+' 1390Q'+(horseX+330)+' 1570 1030 1590'}
   stroke="#ddbb85" strokeWidth="19" fill="none" strokeDasharray="25 8"/>}
  {heroScale>0&&<g transform={'translate('+(heroX+heroShift)+' '+heroY+') scale('+heroScale+')'}>
   <Odysseus time={t} pose={role} night={night>0}/>
  </g>}
  {scene===3&&[0,1].map(i=><g key={i}
   transform={'translate('+(70+i*770)+' 1410) scale(.57)'}>
     <Odysseus time={t+i} pose="craft"/>
    </g>)}
  {scene===7&&[0,1,2].map(i=><g key={i}
   transform={'translate('+(170+i*170+t*60)+' '+(1300+i*42)+') scale('+(0.47-i*.05)+')'}>
    <Odysseus time={t+i} pose="run" night/>
   </g>)}
  {(scene===0||scene===9)&&<g
   transform={'translate('+(scene===0?580:55)+' '+(scene===0?1250:1220)+') scale(.51)'}>
    <LuminoPuppet time={time} gesture={scene===0?'look':'discover'} width={740} height={850}/>
   </g>}
 </g>
 {[0,1,2,3,4].map(i=><ellipse key={i} cx={(i*310+time*17)%1450-150}
  cy={1570+i*61} rx={260+i*30} ry={40+i*6} fill="#e4ded0"
  opacity={night?.037:.042}/>)}
 </svg>
 <div style={{position:'absolute',top:115,left:77,right:60,fontFamily:'Georgia,serif',
  fontSize:33,color:'#f6e0b5',letterSpacing:3,fontWeight:700,
  textShadow:'0 3px 12px #061a20'}}>MITOLOGIA GREGA · ODISSEU</div>
 <div style={{position:'absolute',top:200,left:75,right:60,
  fontFamily:'Arial,sans-serif',fontSize:66,fontWeight:900,
  lineHeight:1.07,color:'#fff0cd',textShadow:'0 4px 16px #0b1118',
  opacity:1-ramp(t,2.5,3.35)}}>{TROIA_CUES[scene].title}</div>
 <div style={{position:'absolute',bottom:168,left:70,right:70,
  fontFamily:'Arial,sans-serif',fontSize:50,fontWeight:700,lineHeight:1.17,
  color:'#fff9e9',textShadow:'0 3px 6px #07141b, 0 4px 16px #07141b',
  textAlign:'center',opacity:ramp(t,.07,.44)*(1-ramp(t,5.55,6))}}>
  {TROIA_CUES[scene].text}
 </div>
 <Audio src={staticFile('audio/odisseu-original-score.wav')} volume={.22}/>
 {voicePath&&<Audio src={staticFile(voicePath)} volume={1}/>}
 </AbsoluteFill>;
};
