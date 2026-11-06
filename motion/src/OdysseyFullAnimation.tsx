import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {Odysseus,type WarriorPose} from './actors/OdysseusActor';
import {getOdysseyBeat,ODYSSEY_TOTAL_SECONDS,ODYSSEY_BEATS} from './odysseyTimeline';

/** Full editable 2D character-animation staging of the Odyssey.
 * Production clock follows the source narration, not an invented voice recording.
 * Every named beat is its own action; no backward-forward puppet translation loops.
 * Separate rendering from audio mux and subtitle alignment to preserve Rasalgethi.
 */
const W=1080,H=1920,PI=Math.PI;
const clamp=(v:number,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=(v:number)=>{const x=clamp(v);return x*x*(3-2*x)};
const lerp=(a:number,b:number,x:number)=>a+(b-a)*x;
const cycle=(v:number)=>v-Math.floor(v);
const shade='#1b2230';
const LAND:Record<string,[string,string,string,string]>={
 troia:['#162239','#9a574c','#514a48','#b17b5c'],
 lotus:['#365768','#dcb87c','#709a76','#c3a07c'],
 cave:['#111624','#3b3540','#333039','#77717a'],
 seaStorm:['#081324','#386476','#233e59','#697c8d'],
 wind:['#122d48','#9db1b0','#305468','#c1b7a0'],
 harbor:['#22263d','#a37865','#3e5368','#b0a080'],
 circe:['#162b31','#9c9668','#55765d','#ab956e'],
 hades:['#0b132a','#343750','#353046','#6b6570'],
 sirens:['#101b3b','#a48498','#315777','#a39d9b'],
 strait:['#08263b','#5e7b8e','#274b63','#97aab1'],
 cattle:['#1e3447','#e9b985','#6d8c64','#d7b78c'],
 calypso:['#1c465a','#ecd4a7','#6c8a73','#d9b790'],
 phaeacia:['#21445d','#d4a77a','#8f786b','#d0ac83'],
 journey:['#1c344d','#e4b47a','#67775d','#c6a37a'],
 ithaca:['#132940','#c89074','#647367','#c4ab87'],
 argos:['#1c3545','#c6987f','#5e7d7a','#c6a47b'],
 wash:['#1d202e','#65564c','#554b48','#99836b'],
 bow:['#151b2b','#8b5e4e','#605044','#a48062'],
 penelope:['#152438','#846c61','#524b4a','#bba07e'],
 bed:['#192331','#95755a','#625447','#bd9b72'],
 finale:['#172e43','#e3b48b','#577b70','#c7ab7c']
};
const SEA=new Set(['troia','lotus','seaStorm','wind','harbor','sirens','strait','calypso','phaeacia']);
const INTERIOR=new Set(['wash','bow','penelope','bed']);
const bgClouds=[0,1,2,3,4],dots=Array.from({length:37},(_,i)=>i);
const Stage:React.FC<{world:string;id:string;time:number;progress:number}>=({world,id,time,progress})=>{
 const p=LAND[world]??LAND.ithaca!,sea=SEA.has(world),inside=INTERIOR.has(world),cave=world==='cave',hades=world==='hades',seed=id.split('-').reduce((s,v)=>s+Number(v.replace(/\D/g,'')),0);
 const sunX=720+(seed%5)*21, sunY=385+(seed%4)*31;
 return <g>
  <defs>
   <linearGradient id="saga-sky" x1="0" y1="0" x2="0" y2="1"><stop stopColor={p[0]}/><stop offset=".64" stopColor={p[1]}/><stop offset="1" stopColor={p[2]}/></linearGradient>
   <linearGradient id="saga-earth" x1="0" y1="0" x2=".3" y2="1"><stop stopColor={p[3]}/><stop offset="1" stopColor="#292f36"/></linearGradient>
   <radialGradient id="saga-glow"><stop stopColor="#fff1bd" stopOpacity=".68"/><stop offset="1" stopColor="#fff1bd" stopOpacity="0"/></radialGradient>
  </defs>
  <rect width={W} height={H} fill="url(#saga-sky)"/>
  {!inside&&!cave&&!hades&&<><circle cx={sunX} cy={sunY} r="88" fill="#ffe0a3" opacity=".68"/><circle cx={sunX} cy={sunY} r="410" fill="url(#saga-glow)" opacity=".6"/></>}
  {bgClouds.map(i=><path key={i} d={'M'+(-230+i*265+time*(3+i%2))+' '+(380+i*103)+'q100 -45 240 -4'} stroke="#f5ddce" strokeWidth={22+i%3*9} strokeLinecap="round" fill="none" opacity={inside||cave?.0:.07}/>)}
  {sea&&<><path d="M0 1040Q200 790 430 1010T800 960L1080 850V1530H0Z" fill="#344f62" opacity=".72"/>
   <path d="M0 1250Q310 1110 560 1240T1080 1200V1920H0Z" fill="#24465d"/>
   <path d="M0 1428Q300 1360 650 1470T1080 1450V1920H0Z" fill="#38647a"/>
   {Array.from({length:17},(_,i)=><path key={i} d={'M'+(-135+i*110+Math.sin(time*1.6+i)*14)+' '+(1450+i%4*93)+'q90 -18 160 0'} stroke="#cde1dc" strokeWidth={i%3===0?6:3} opacity=".12" fill="none"/>)}
  </>}
  {!sea&&!inside&&!cave&&<><path d="M0 1020Q200 830 485 1030T1080 920V1920H0Z" fill={p[2]}/><path d="M0 1370Q300 1260 650 1380T1080 1320V1920H0Z" fill="url(#saga-earth)"/></>}
  {(world==='ithaca'||world==='journey'||world==='finale'||world==='argos'||world==='calypso'||world==='circe')&&[0,1,2,3].map(i=><g key={i} transform={'translate('+(i*322-90+seed%65)+' '+(1330+i%2*70)+')'}>
    <path d="M0 0L12 -485" stroke="#494638" strokeWidth="45" strokeLinecap="round"/>
    <path d="M8 -300Q-160 -488 -140 -595M7 -322Q145 -445 143 -586" fill="none" stroke="#494638" strokeWidth="21"/>
    <ellipse cx="-55" cy="-535" rx="167" ry="80" fill="#476651"/><ellipse cx="105" cy="-583" rx="144" ry="82" fill="#648267"/>
    {[0,1,2,3].map(j=><circle key={j} cx={-83+j*70} cy={-550-j%2*35} r="12" fill="#202c27"/>)}
   </g>)}
  {(world==='troia'||world==='phaeacia'||world==='harbor')&&[0,1,2,3].map(i=><g key={i} transform={'translate('+(i*285-20)+' 980)'}>
    <rect x="0" y="-360" width="200" height="780" fill="#a39082" stroke="#343440" strokeWidth="15"/>
    <path d="M-20 -360L100 -495L220 -360Z" fill="#776968" stroke="#303543" strokeWidth="15"/>
    <rect x="65" y="-290" width="70" height="180" fill="#243647"/>
  </g>)}
  {inside&&<><rect y="415" width={W} height="1505" fill="#5b514b" opacity=".9"/>
   {[0,1,2,3,4].map(i=><g key={i}><rect x={i*261-65} y="375" width="145" height="1125" fill="#94806b" stroke="#3b3739" strokeWidth="14"/><path d={'M'+(i*261-65)+' 660h145M'+(i*261-65)+' 990h145'} stroke="#c9a783" strokeWidth="12" opacity=".6"/></g>)}
   <path d="M0 1485H1080V1920H0Z" fill="#554940"/><path d="M0 1505H1080" stroke="#d4bb91" strokeWidth="12"/>
   {[0,1,2,3,4].map(i=><path key={i} d={'M'+(i*290-90)+' 1520L'+(i*250-170)+' 1920'} stroke="#af957b" strokeWidth="5" opacity=".36"/>)}
  </>}
  {cave&&<><path d="M0 0H1080V1920H0V1410Q150 700 540 660Q870 690 1080 1400Z" fill="#24222d"/>
    <path d="M155 1700V1230Q170 710 545 650Q900 680 933 1220V1700Z" fill="#131824" stroke="#77707c" strokeWidth="43"/>
    <path d="M0 1490Q420 1370 1080 1500V1920H0Z" fill="#373039"/>
    {[0,1,2,3,4].map(i=><path key={i} d={'M'+(i*250-80)+' 0l'+(80+i*12)+' '+(240+i%2*140)+'l115 -100Z'} fill="#302e37"/>)}
   </>}
  {hades&&<>{Array.from({length:26},(_,i)=><circle key={i} cx={(i*123+35)%W} cy={(i*171+40)%1350} r={i%4+1} fill="#d4b7d9" opacity=".4"/>)}<path d="M0 1140Q320 930 550 1130T1080 1000V1920H0Z" fill="#29283b"/><path d="M0 1490Q540 1280 1080 1510V1920H0Z" fill="#464051"/></>}
  {dots.map(i=><ellipse key={i} cx={(i*199+seed*23)%W} cy={1560+(i*83)%340} rx={i%3===0?11:4} ry={3} fill="#e8d3b5" opacity=".24"/>)}
 </g>
};
const Ship:React.FC<{x:number;y:number;scale?:number;time:number;broken?:boolean;facing?:number;wave?:number}>=({x,y,scale=1,time,broken=false,facing=1,wave=0})=>{
 const bob=Math.sin(time*2.7+x)*8*(1+wave);
 return <g transform={'translate('+x+' '+(y+bob)+') scale('+(scale*facing)+' '+scale+')'}>
  <ellipse cx="0" cy="115" rx="345" ry="28" fill="#192a37" opacity=".25"/>
  <path d={broken?'M-328 45L-178 145L-38 117L70 164L270 46L165 100L-170 105Z':'M-348 28Q-292 157 0 154Q270 163 345 29L252 63L-250 62Z'} fill="#8e5637" stroke="#402e2a" strokeWidth="13"/>
  <path d="M-315 46Q0 102 310 47" fill="none" stroke="#e0ac76" strokeWidth="12"/>
  <path d="M-235 75L-200 105M-85 80L-50 114M65 81L100 111M215 74L250 103" stroke="#583d2e" strokeWidth="11"/>
  <path d="M-6 25V-490" stroke="#5b3e2f" strokeWidth={broken?18:22}/>
  {!broken&&<path d={'M5 -464Q'+(155+Math.sin(time)*40)+' -267 12 -48Z'} fill="#e5ca98" stroke="#554b43" strokeWidth="11"/>}
  {Array.from({length:5},(_,i)=><g key={i} transform={'translate('+(-220+i*110)+' 68) rotate('+(-21+Math.sin(time*5+i*.38)*25)+')'}>
   <path d="M0 0L-78 160" stroke="#c38d56" strokeWidth="15" strokeLinecap="round"/><ellipse cx="-77" cy="149" rx="20" ry="47" transform="rotate(28 -77 149)" fill="#ae7545"/>
  </g>)}
  {[0,1,2,3].map(i=><g key={i} transform={'translate('+(-172+i*118)+' 6)'}><ellipse cy="-19" rx="15" ry="18" fill={i%2?'#d19c76':'#aa755b'}/><path d="M-20 6L-18 55H17L24 3Z" fill={['#6c5554','#7e684d','#67736a','#4d6470'][i]}/></g>)}
 </g>;
};
const Cyclops:React.FC<{x:number;y:number;scale?:number;t:number;push?:boolean;asleep?:boolean}>=({x,y,scale=2.6,t,push=false,asleep=false})=>{
 const sway=Math.sin(t*1.35)*3,arm=push?Math.min(1,t/2):0;
 return <g transform={'translate('+x+' '+y+') scale('+scale+')'}>
  <g transform={'translate(165 370) rotate('+(-arm*5.5)+') translate(-165 -370)'}>
  <ellipse cx="160" cy="542" rx="130" ry="15" fill="#090d18" opacity=".35"/>
  <path d="M78 381L61 537M229 378L256 537" stroke="#4f413d" strokeWidth="84" strokeLinecap="round"/>
  <path d="M78 380L62 520M229 373L251 520" stroke="#a58b75" strokeWidth="68" strokeLinecap="round"/>
  <path d="M40 214Q155 151 276 220L290 385Q150 435 25 382Z" fill="#70615a" stroke="#342e32" strokeWidth="17"/>
  <path d="M56 347Q170 390 262 350L245 426L48 420Z" fill="#433a39"/>
  {!push&&<>
  <path d={'M56 249Q'+(-10+arm*15)+' 290 '+(-25+arm*75)+' '+(405-arm*100)} stroke="#4b3e3c" strokeWidth="71" strokeLinecap="round" fill="none"/>
  <path d={'M56 249Q'+(-10+arm*15)+' 290 '+(-25+arm*75)+' '+(405-arm*100)} stroke="#a98b72" strokeWidth="55" strokeLinecap="round" fill="none"/>
  <circle cx={-25+arm*75} cy={405-arm*100} r="38" fill="#ab917b" stroke="#51443e" strokeWidth="9"/>
  <path d={'M255 249Q320 330 '+(315+arm*36)+' '+(383-arm*50)} stroke="#493b37" strokeWidth="71" strokeLinecap="round" fill="none"/>
  <path d={'M255 249Q320 330 '+(315+arm*36)+' '+(383-arm*50)} stroke="#a88b74" strokeWidth="54" strokeLinecap="round" fill="none"/>
  <circle cx={315+arm*36} cy={383-arm*50} r="39" fill="#ab917b" stroke="#51443e" strokeWidth="9"/>
  </>}
  <g transform={'translate(0 '+sway+')'}>
   <path d="M93 78Q163 17 233 83L253 212Q170 271 66 214Z" fill="#b2967b" stroke="#463735" strokeWidth="15"/>
   <path d="M94 106Q126 18 214 57L240 106Q169 88 94 106Z" fill="#372f31"/>
   <ellipse cx="165" cy="152" rx="47" ry="36" fill="#e8d2ab" stroke="#63554d" strokeWidth="9"/>
   {asleep?<path d="M132 157Q166 178 201 157" stroke="#38313a" strokeWidth="11" fill="none"/>:<><ellipse cx="168" cy="155" rx="22" ry="26" fill="#d0ab73"/><circle cx="170" cy="157" r="14" fill="#302f34"/><circle cx="177" cy="149" r="5" fill="#fff0ce"/></>}
   <path d="M144 194Q167 204 190 194" stroke="#674f47" strokeWidth="9" fill="none"/>
   <path d="M88 200Q166 263 245 199" stroke="#504039" strokeWidth="10" fill="none"/>
  </g>
  </g>
 </g>;
};
const Boulder:React.FC<{x:number;y:number;scale?:number;roll?:number}>=({x,y,scale=1,roll=0})=><g transform={'translate('+x+' '+y+') scale('+scale+') rotate('+roll+')'}>
 <path d="M-345 -115L-220 -326L78 -365L305 -230L369 72L260 290L-47 376L-290 210Z" fill="#6b6668" stroke="#2f3037" strokeWidth="28"/>
 <path d="M-224 -310L-40 -170L135 -290M-345 -115L-90 9L89 -120L305 -230M-290 210L-90 9L-47 376M89 -120L260 290L-47 376" stroke="#9c9493" strokeWidth="17" fill="none" opacity=".68"/>
 <path d="M-310 65L-86 112L-20 328M105 -148L270 72" stroke="#424249" strokeWidth="17" fill="none" opacity=".8"/>
 </g>;
type Role='penelope'|'telemachus'|'circe'|'hermes'|'athena'|'nausicaa'|'calypso'|'suitor'|'nurse'|'mother'|'crew'|'seer';
const roleTint:Record<Role,[string,string,string]>={
 penelope:['#294e57','#d3a188','#2b2533'],telemachus:['#748081','#c49370','#43302e'],
 circe:['#285b45','#d7a17b','#49332e'],hermes:['#968354','#d8ad86','#725533'],
 athena:['#536c88','#c99a78','#342a42'],nausicaa:['#b87b60','#d8a487','#5c423a'],
 calypso:['#ddd1b5','#ddb28d','#9b8055'],suitor:['#853f43','#b98c67','#413239'],
 nurse:['#6c5461','#bfa18c','#cdc6ba'],mother:['#857a93','#bda6a1','#67596b'],
 crew:['#657b72','#b48a67','#362d2b'],seer:['#747382','#b29e92','#e3dcca']
};
const RoleActor:React.FC<{role:Role;x:number;y:number;scale?:number;t:number;gesture?:string;opacity?:number}>=({role,x,y,scale=1.4,t,gesture='',opacity=1})=>{
 const [fabric,skin,hair]=roleTint[role],lift=gesture==='reach'?Math.min(1,t/2):0,arms=gesture==='work'?Math.sin(t*5)*28:0;
 const elderly=role==='nurse'||role==='seer',robe=role!=='telemachus'&&role!=='crew'&&role!=='suitor';
 return <g opacity={opacity} transform={'translate('+x+' '+(y+Math.sin(t*1.3)*1.5)+') scale('+scale+')'}>
  <ellipse cx="0" cy="22" rx="93" ry="13" fill="#131b23" opacity=".23"/>
  {robe?<path d="M-67 -228L-112 10H113L67 -228Z" fill={fabric} stroke="#2c2a30" strokeWidth="10"/>:<><path d="M-62 -226H69L75 -34L-70 -34Z" fill={fabric} stroke="#2e2c30" strokeWidth="10"/><path d="M-49 -25L-55 12M49 -25L55 12" stroke="#866c5d" strokeWidth="36" strokeLinecap="round"/></>}
  <path d="M-65 -228Q-137 -185 -132 -116" stroke={fabric} strokeWidth="37" fill="none" strokeLinecap="round"/>
  <path d="M-130 -115L-109 -62" stroke={skin} strokeWidth="26" fill="none" strokeLinecap="round"/>
  <path d={'M67 -225Q130 -178 '+(112-lift*15)+' '+(-95-lift*95+arms)} stroke={fabric} strokeWidth="38" fill="none" strokeLinecap="round"/>
  <path d={'M'+(112-lift*15)+' '+(-95-lift*95+arms)+'l'+(4-lift*25)+' 30'} stroke={skin} strokeWidth="26" fill="none" strokeLinecap="round"/>
  <path d="M-50 -262H50V-222H-50Z" fill={skin}/>
  <path d="M-74 -341Q-64 -427 5 -426Q83 -418 76 -336L69 -280Q6 -239 -64 -285Z" fill={skin} stroke="#514039" strokeWidth="9"/>
  <path d="M-75 -340Q-81 -432 13 -432Q86 -425 76 -328L55 -377Q-12 -355 -75 -340Z" fill={hair}/>
  {elderly&&<path d="M-70 -364Q-50 -429 29 -425" stroke="#e0d2b7" strokeWidth="16" fill="none"/>}
  <path d="M-49 -321l22 -5M21 -325l23 4" stroke="#493738" strokeWidth="7"/>
  <circle cx="-33" cy="-309" r="6" fill="#2c292e"/><circle cx="29" cy="-309" r="6" fill="#2c292e"/>
  <path d="M-5 -300l-7 30 17 4" stroke="#9d715a" strokeWidth="5" fill="none"/>
  <path d="M-22 -252Q0 -245 23 -257" stroke="#624a45" strokeWidth="6" fill="none"/>
  {(role==='athena'||role==='hermes')&&<path d="M-65 -370Q0 -454 76 -376" fill="none" stroke="#f1ce87" strokeWidth="17"/>}
 </g>;
};
const Dog:React.FC<{t:number;x?:number;y?:number;wag?:boolean}>=({t,x=290,y=1450,wag=false})=><g transform={'translate('+x+' '+y+')'}>
 <ellipse cy="71" rx="189" ry="20" fill="#23282c" opacity=".23"/>
 <path d={'M-142 -101Q-225 -171 '+(-224+Math.sin(t*9)*(wag?39:3))+' '+(-109-Math.sin(t*9)*9)} stroke="#8c684a" strokeWidth="30" fill="none" strokeLinecap="round"/>
 <path d="M-125 -128L-143 55M-39 -130L-46 60M86 -115L99 62M130 -105L133 56" stroke="#b18b5e" strokeWidth="32" strokeLinecap="round"/>
 <path d="M-148 -181Q-55 -252 105 -194L159 -96Q-13 -44 -144 -104Z" fill="#b18b5e" stroke="#52473a" strokeWidth="10"/>
 <g transform={'translate(148 -161) rotate('+(-9+Math.sin(t*1.3)*12)+')'}>
  <ellipse rx="70" ry="65" fill="#bb966b" stroke="#584838" strokeWidth="8"/>
  <path d="M-56 -42L-69 -109L-9 -71M35 -51L63 -116L79 -29" fill="#71573e"/>
  <circle cx="-20" cy="-8" r="8" fill="#24252d"/><circle cx="34" cy="-9" r="8" fill="#24252d"/>
  <ellipse cx="8" cy="22" rx="16" ry="10" fill="#4b3b35"/>
 </g></g>;
const Cow:React.FC<{x:number;y:number;size:number;t:number}>=({x,y,size,t})=><g transform={'translate('+x+' '+y+') scale('+size+')'}>
 <ellipse cy="12" rx="144" ry="18" fill="#303329" opacity=".18"/>
 {[[-91,0],[-27,11],[62,5],[103,4]].map(([a,b],i)=><path key={i} d={'M'+a+' -96L'+(a+b+Math.sin(t*1.5+i)*4)+' '+(-3)} stroke="#d6bd9d" strokeWidth="24" strokeLinecap="round"/>)}
 <path d="M-146 -203Q-32 -270 104 -209L132 -123Q-42 -75 -151 -136Z" fill="#dfcaad" stroke="#59514b" strokeWidth="9"/>
 <path d="M-82 -234Q-26 -189 -63 -137M51 -207L81 -137" stroke="#8f785f" strokeWidth="40" fill="none"/>
 <path d="M102 -214Q160 -267 201 -203L195 -106Q146 -80 114 -136Z" fill="#dfc7a7" stroke="#5e5048" strokeWidth="9"/>
 <path d="M144 -242l-5 -52 31 40M179 -243l42 -43 -13 54" fill="#c9b187" stroke="#5c4f47" strokeWidth="6"/>
 <ellipse cx="178" cy="-135" rx="31" ry="25" fill="#b79b89"/><circle cx="161" cy="-203" r="6"/><circle cx="196" cy="-206" r="6"/>
 </g>;
const heroScaleForGait=(world:string,sea:boolean)=>world==='cave'?.88:sea?1.38:1.56;
const actionIn=(action:string,...checks:string[])=>checks.includes(action);
const OnlyScene:React.FC<{action:string;time:number;duration:number;world:string}>=({action,time:t,duration:d,world})=>{
 const q=ease(t/Math.max(.5,d-.8)),a=action,p=clamp(t/d);
 const sea=SEA.has(world);
 const heroNo=new Set(['weavingNight','boulderSeals','lotusEnchantment','cyclopsArrival','cyclopsSleeping','giantsAttack','boatsDestroyed','circeWelcomes','enchantedCup','menTransform','motherAppears','wingedSirens','sacredHerd','crewHunger','forbiddenFeast','calypsoShelter','nausicaaFinds','telemachusSeeks','athenaGuides','dangerousReturn','sonApproaches','argosHears','argosLooks','suitorsFeast','bowAttempt','penelopeApproaches','facesUncertain','oliveTreeReveal','palaceRestored','familyAtOlive','islandPanorama']);
 const showHero=!heroNo.has(a);
 const heroWalk=/Landing|Departure|Approaches|Rescue|Escape|Entry|Return|Approach|Meet|Plan|Rises|Greeting|shoreWake|caveDiscovery|fleetDeparture|lotusRescue|ithacaDiscovered|shepherdHut|nightPalaceEntry|shoreRescue|nausicaaFinds/i.test(a);
 const pose:WarriorPose=actionIn(a,'fatherSonMeet','motherAppears','handsPassGhost','penelopeApproaches','recognitionDawns','reunionEmbrace','familyAtOlive')?'embrace':
 actionIn(a,'argosGreeting','argosRises')?'pet':
 actionIn(a,'bagUnknotted','wineToGiant','enchantedCup','hermesHerb','raftCarpentry','oldNurseWashes','scarDiscovered','bowBends','arrowTargets','bedSecret')?'craft':
 actionIn(a,'darkStorm','shipBraces','poseidonRises','thunderBreaksShip','raftStorm','scyllaStrikes','giantsAttack')?'brace':
 actionIn(a,'motherAppears','facesUncertain','lyreLament','quietNight','odysseusWaits')?'grieve':
 actionIn(a,'cyclopsPlea','nameRevealed','seerWarns','fatherSonPlan')?'point':
 heroWalk?'walk':'listen';
 // Root translation is permitted only when legs actually run a moving gait.
 // Petting, embracing and crafting must not slide on planted feet.
 const rootMoves=heroWalk&&pose==='walk';
 const heroX=rootMoves?105+165*clamp(t/d):180;
 const heroLocalSpeed=rootMoves?(165/d)/heroScaleForGait(world,sea):undefined;
 const heroY=actionIn(a,'cyclopsArrival','boulderSeals','prisonersWatch','wineToGiant','cyclopsSleeping','stakePrepared','ramEscape','cyclopsPlea')?985:sea?760:730;
 const heroScale=heroScaleForGait(world,sea);
 const hero=<g transform={'translate('+heroX+' '+heroY+') scale('+heroScale+')'}><Odysseus time={t} pose={pose} speed={heroLocalSpeed} civilian={world==='argos'||world==='wash'||world==='penelope'||world==='bed'||world==='finale'||world==='ithaca'}/></g>;
 return <g>
   {/* Foreground props and supporting animation are action-specific, never generic camera pans of stills. */}
   {/* Distinct household action: Penelope's loom, its shuttle moves while the thread changes length. */}
   {actionIn(a,'ithacaWaiting','weavingNight')&&<>
    <RoleActor role="penelope" x={760} y={1530} scale={1.42} t={t} gesture="work"/>
    {a==='ithacaWaiting'&&<RoleActor role="telemachus" x={285} y={1530} scale={.82} t={t}/>}
    <g transform="translate(395 1000)">
     <path d="M-185 -100V570M165 -100V570M-185 -100H165M-185 570H165" stroke="#8f6548" strokeWidth="31" fill="none"/>
     {[0,1,2,3,4,5,6,7,8].map(i=><path key={i} d={'M'+(-153+i*36)+' -70V'+(210+q*190)} stroke="#e4c59c" strokeWidth="7" opacity=".9"/>)}
     <rect x="-170" y="175" width="325" height={Math.max(35,145+(a==='weavingNight'?-q:q)*100)} fill="#b38c71" stroke="#d2b69b" strokeWidth="7" opacity=".88"/>
     <path d={'M'+lerp(-170,155,cycle(t*1.3))+' 75h70'} stroke="#f6ddbc" strokeWidth="21" strokeLinecap="round"/>
    </g>
   </>}
   {/* Waking on the Ithacan shore and receiving help are separate visible events. */}
   {actionIn(a,'shoreRescue','shoreWake')&&<>
    <path d="M0 1430Q400 1280 1080 1435V1920H0Z" fill="#c1a783" opacity=".7"/>
    {a==='shoreRescue'&&<RoleActor role="nausicaa" x={775} y={1550} scale={1.36} t={t} gesture="reach"/>}
    {[0,1,2,3].map(i=><path key={i} d={'M'+(-100+i*330+q*28)+' '+(1360+i%2*45)+'q160 -38 280 0'} stroke="#d2dedd" strokeWidth="12" fill="none" opacity=".4"/>)}
   </>}

   {actionIn(a,'burningTroia','fleetDeparture','rowingHome','lotusLanding','lotusRescue','nameRevealed','shipBraces','homeOnHorizon','windsReleased','fleetTrapped','boatsDestroyed','lastShipEscapes','waxInEars','tiedToMast','wingedSirens','rowingPastVoices','straitRevealed','whirlpoolTurns','scyllaStrikes','shipNarrowEscape','thunderBreaksShip','aloneAdrift','raftLaunch','raftStorm','giftsAboard','sleepingReturn')&&
     <Ship x={540+(actionIn(a,'rowingHome','lastShipEscapes','shipNarrowEscape','sleepingReturn')?q*105:0)} y={1355} scale={actionIn(a,'fleetDeparture','fleetTrapped','burningTroia')?.72:1.18} time={t} wave={world==='seaStorm'||world==='strait'?1.7:.5} broken={a==='thunderBreaksShip'}/>}
   {actionIn(a,'burningTroia','fleetDeparture','fleetTrapped','boatsDestroyed')&&[0,1,2].map(i=><Ship key={i} x={210+i*260} y={1100+i%2*50} scale={.4+i*.12} time={t+i} broken={a==='boatsDestroyed'&&i!==2}/>)}
   {actionIn(a,'burningTroia','fleetDeparture')&&[0,1,2,3,4].map(i=><path key={i} d={'M'+(i*220+30)+' '+(930-i%3*70)+'q-20 -58 26 -123q4 64 38 112Z'} fill="#e68c47" opacity={.4+.3*Math.sin(t*5+i)}/>)}
   {actionIn(a,'lotusLanding','lotusOffering','lotusEnchantment','lotusRescue')&&[0,1,2].map(i=><g key={i}>
     <RoleActor role="crew" x={200+i*290} y={1550} scale={1.05} t={t} gesture={a==='lotusRescue'?'reach':'work'}/>
     <path d={'M'+(240+i*290)+' 1040q35 -90 75 -25q-40 39 -75 25Z'} fill="#b983ab" opacity={a==='lotusRescue'?1:.75}/>
    </g>)}
   {actionIn(a,'caveDiscovery','cyclopsArrival','boulderSeals','prisonersWatch','wineToGiant','cyclopsSleeping','stakePrepared','ramEscape','cyclopsPlea','nameRevealed')&&<>
     {a!=='caveDiscovery'&&<Cyclops x={a==='boulderSeals'?lerp(780,530,ease(t/Math.max(1,d*.86))):140} y={195} scale={2.5} t={t} push={a==='boulderSeals'} asleep={a==='cyclopsSleeping'||a==='stakePrepared'||a==='ramEscape'}/>}
     {a==='boulderSeals'&&(()=>{
       // Continuous blocking: giant advances from the right, rock travels from beside him
       // to the exact cave center. Both articulated arms visibly remain in contact.
       const advance=ease(t/Math.max(1,d*.86)),rockX=lerp(1100,545,advance),giantX=lerp(780,530,advance);
       const left={x:rockX+285,y:1063-advance*28},right={x:rockX+451,y:1090-advance*15};
       const upperL={x:giantX+56*2.5,y:195+249*2.5},upperR={x:giantX+255*2.5,y:195+249*2.5};
       const armPath=(s:{x:number;y:number},e:{x:number;y:number},bend:number)=>
         'M'+s.x+' '+s.y+'Q'+(s.x*.46+e.x*.54)+' '+(s.y+80+bend)+' '+e.x+' '+e.y;
       return <g>
        <g transform="translate(210 1090) scale(.64)"><Odysseus time={t} pose="brace"/></g>
        <Boulder x={rockX} y={1260} scale={1.46} roll={-q*13}/>
        {[{s:upperL,e:left,bend:-44},{s:upperR,e:right,bend:34}].map((arm,i)=><g key={i}>
          <path d={armPath(arm.s,arm.e,arm.bend)} stroke="#453a3b" strokeWidth="122" fill="none" strokeLinecap="round"/>
          <path d={armPath(arm.s,arm.e,arm.bend)} stroke="#a78a73" strokeWidth="101" fill="none" strokeLinecap="round"/>
          <path d={armPath(arm.s,arm.e,arm.bend)} stroke="#d1ae8d" strokeWidth="16" fill="none" strokeLinecap="round" opacity=".6"/>
          <ellipse cx={arm.e.x} cy={arm.e.y} rx="71" ry="67" fill="#b89a7e" stroke="#53433d" strokeWidth="16"/>
          {[0,1,2].map(j=><path key={j} d={'M'+(arm.e.x-34+j*27)+' '+(arm.e.y-9)+'q-9 -32 -16 -32'} stroke="#8b6e60" strokeWidth="11" strokeLinecap="round" fill="none"/>)}
         </g>)}
        {[0,1,2,3].map(i=><ellipse key={i} cx={rockX-350+i*185} cy={1628-Math.sin(t*7+i)*18} rx={25+advance*22} ry={9+advance*6} fill="#baa99f" opacity={advance*(1-advance)*.7}/>)}
       </g>;
      })()}
     {a==='cyclopsArrival'&&<Boulder x={1220} y={1270} scale={1.46}/>}
     {a==='prisonersWatch'&&<Boulder x={545} y={1260} scale={1.46}/>}
     {a==='wineToGiant'&&<><path d="M690 1050L760 960L820 1032L800 1168Z" fill="#8d3c42" stroke="#e1bc8d" strokeWidth="12"/><path d="M810 1042Q890 950 910 1080" fill="none" stroke="#c28874" strokeWidth="30"/></>}
     {a==='stakePrepared'&&<path d={'M'+lerp(300,580,q)+' '+lerp(1455,1060,q)+'l330 -230'} stroke="#bb9663" strokeWidth="36" strokeLinecap="round" fill="none"/>}
     {a==='cyclopsPlea'&&<><path d="M515 820L565 905" stroke="#ab6c4d" strokeWidth="28"/><circle cx="580" cy="980" r="30" fill="#a47b60"/></>}
     {a==='ramEscape'&&<Boulder x={545+q*820} y={1260} scale={1.46}/>} 
     {a==='ramEscape'&&[0,1,2].map(i=><g key={i} transform={'translate('+(160+i*280+q*65)+' 1590)'}><ellipse cx="0" cy="-85" rx="104" ry="63" fill="#d6c9a9" stroke="#5b504d" strokeWidth="9"/><ellipse cx="91" cy="-85" rx="42" ry="35" fill="#cdbf9f"/><path d="M-60 -42v62M48 -40v60" stroke="#a99375" strokeWidth="24"/></g>)}
    </>}
   {actionIn(a,'poseidonRises','darkStorm','shipBraces','raftStorm')&&[0,1,2,3,4,5].map(i=><path key={i} d={'M'+(i*220-130)+' '+(270+i%3*130)+'l'+(65+Math.sin(t*4+i)*15)+' 280'} stroke="#d4e7eb" strokeWidth={5+i%2*4} opacity=".65"/>)}
   {a==='poseidonRises'&&<g transform={'translate(640 '+(320-q*70)+')'} opacity=".62"><path d="M-170 650Q-270 80 0 -80Q250 40 170 670Z" fill="#4a8796" stroke="#c8dbe2" strokeWidth="25"/><circle cy="115" r="112" fill="#8ca9b2"/><path d="M0 -40V350M-85 0H85" stroke="#dfdde0" strokeWidth="20"/></g>}
   {actionIn(a,'aeolusGift','homeOnHorizon','bagUnknotted','windsReleased')&&<>
    <path d={'M'+(675+q*26)+' '+(1035-q*70)+'q-90 -80 -94 55q-42 220 75 270q151 -50 98 -220q-40 -76 -79 -105Z'} fill="#956d52" stroke="#44372f" strokeWidth="14"/>
    <path d="M592 1020q75 19 164 6" stroke="#e8c18b" strokeWidth="20" opacity={a==='bagUnknotted'?1:.7}/>
    {(a==='bagUnknotted'||a==='windsReleased')&&[0,1,2,3].map(i=><path key={i} d={'M690 1030q'+(220+q*200)+' '+(-200-i*20)+' '+(350+q*310)+' '+(-290-i*80)} fill="none" stroke="#d1e5e6" strokeWidth={17+i*5} opacity={q*.8}/>)}
   </>}
   {actionIn(a,'giantsAttack','boatsDestroyed','fleetTrapped','lastShipEscapes')&&[0,1].map(i=><g key={i}><Cyclops x={i*770-220} y={90+i*80} scale={1.9} t={t+i} push={a==='giantsAttack'}/><Boulder x={i*800+210+q*(a==='giantsAttack'?140:0)} y={1100+q*(a==='giantsAttack'?330:0)} scale={.28+i*.12}/></g>)}
   {actionIn(a,'circeWelcomes','enchantedCup','menTransform','hermesHerb','circeDefied','crewRestored')&&<>
    <RoleActor role={a==='hermesHerb'?'hermes':'circe'} x={755} y={1540} t={t} gesture="reach"/>
    {[0,1].map(i=><g key={i} opacity={a==='menTransform'?1-q*.8:a==='crewRestored'?q:1}><RoleActor role="crew" x={210+i*240} y={1510} scale={.91} t={t} gesture="work"/></g>)}
    {(a==='menTransform'||a==='crewRestored')&&[0,1].map(i=><g key={i} transform={'translate('+(230+i*240)+' 1625)'} opacity={a==='menTransform'?q:1-q}>
      <ellipse rx="105" ry="72" fill="#c8a18f"/><circle cx="76" cy="-35" r="45" fill="#c8a18f"/><ellipse cx="116" cy="-21" rx="34" ry="23" fill="#dcacac"/><path d="M82 -77l-18 -53 53 28" fill="#aa857a"/>
    </g>)}
    {a==='hermesHerb'&&<path d="M610 1200q-90 -120 -140 -30q90 20 140 30Z" fill="#86aa7a"/>}
    {a==='enchantedCup'&&<path d="M600 1040q-26 156 55 160q88 -11 65 -160Z" fill="#9e6b52" stroke="#d2b890" strokeWidth="12"/>}
   </>}
   {actionIn(a,'underworldGate','seerWarns','motherAppears','handsPassGhost')&&<>
    <RoleActor role={a==='seerWarns'?'seer':'mother'} x={730} y={1480} scale={1.45} t={t} opacity={.28+.2*Math.sin(t*1.7)}/>
    {a==='handsPassGhost'&&<path d={'M'+(490+q*180)+' 1080q130 -80 240 0'} stroke="#dac5e0" strokeWidth="14" opacity=".32" fill="none"/>}
   </>}
   {actionIn(a,'waxInEars','tiedToMast','wingedSirens','rowingPastVoices')&&<>
    {[0,1,2].map(i=><g key={i} transform={'translate('+(i*310+105)+' '+(830-i%2*80)+')'}>
      <path d="M-90 70Q-185 -70 -52 -30Q60 -190 125 -50L68 48Z" fill="#9288a0" stroke="#453f59" strokeWidth="12"/>
      <ellipse cy="30" rx="48" ry="79" fill="#c08d79"/><circle cy="-60" r="44" fill="#d4a18a"/>
      <path d="M-26 -100Q20 -145 49 -82" stroke="#41364a" strokeWidth="17" fill="none"/>
    </g>)}
    {(a==='tiedToMast'||a==='rowingPastVoices')&&<><path d="M539 670V1550" stroke="#7e5d42" strokeWidth="32"/><path d="M465 1050q90 40 150 0M460 1100q100 40 160 0" fill="none" stroke="#c4a17d" strokeWidth="17"/></>}
   </>}
   {actionIn(a,'straitRevealed','whirlpoolTurns','scyllaStrikes','shipNarrowEscape')&&<>
    {Array.from({length:8},(_,i)=><ellipse key={i} cx="210" cy="1510" rx={100+i*38+q*36} ry={32+i*22+q*13} fill="none" stroke="#8ba9b4" strokeWidth="14" opacity=".68" transform={'rotate('+(t*55)+' 210 1510)'}/>)}
    {[0,1,2,3,4,5].map(i=><g key={i} transform={'translate('+(850+i%3*55)+' '+(1360-(i%2)*95)+') rotate('+Math.sin(t*2.3+i)*26+')'}>
      <path d={'M0 0Q'+(i*30-90)+' -145 '+(-170+i*32)+' '+(-310-q*(a==='scyllaStrikes'?120:0))} fill="none" stroke="#53656e" strokeWidth="34" strokeLinecap="round"/>
      <ellipse cx={-170+i*32} cy={-310-q*(a==='scyllaStrikes'?120:0)} rx="33" ry="24" fill="#61767b"/><circle cx={-180+i*32} cy={-325-q*(a==='scyllaStrikes'?120:0)} r="5" fill="#f5dfbc"/>
    </g>)}
   </>}
   {actionIn(a,'sacredHerd','crewHunger','forbiddenFeast')&&[0,1,2,3].map(i=><Cow key={i} x={180+i*245} y={1570+i%2*80} size={.65+i*.11} t={t+i}/>)}
   {actionIn(a,'calypsoShelter','odysseusWaits','hermesDecree','raftCarpentry','raftLaunch')&&<>
    <RoleActor role={a==='hermesDecree'?'hermes':'calypso'} x={780} y={1550} scale={1.4} t={t} gesture={a==='hermesDecree'?'reach':''}/>
    {(a==='raftCarpentry'||a==='raftLaunch')&&[0,1,2,3,4].map(i=><g key={i}><path d={'M'+(150+i*150)+' '+(1550-q*120)+'l340 0'} stroke="#956a47" strokeWidth="31" strokeLinecap="round"/></g>)}
   </>}
   {actionIn(a,'nausicaaFinds','palaceWelcome','lyreLament','pastRetold','giftsAboard')&&<>
     <RoleActor role="nausicaa" x={780} y={1550} scale={1.5} t={t} gesture={a==='nausicaaFinds'?'reach':''}/>
     {(a==='lyreLament'||a==='pastRetold')&&<path d="M585 1130Q480 960 400 1090M585 1130Q670 940 750 1070M440 1040L680 1065" fill="none" stroke="#dbc28f" strokeWidth="19"/>}
    </>}
   {actionIn(a,'telemachusSeeks','athenaGuides','dangerousReturn','ithacaDiscovered','sonApproaches','fatherSonMeet','fatherSonPlan')&&<>
    <RoleActor role="telemachus" x={770-q*80} y={1560} scale={1.37} t={t} gesture={a==='fatherSonMeet'?'reach':''}/>
    {a==='athenaGuides'&&<RoleActor role="athena" x={280} y={1360} scale={1.2} t={t} opacity={.74} gesture="reach"/>}
   </>}
   {actionIn(a,'athenaDisguise','shepherdHut','nightPalaceEntry')&&<RoleActor role="athena" x={745} y={1510} scale={1.24} t={t} gesture="reach" opacity={a==='athenaDisguise'?.85:.45}/>}
   {actionIn(a,'argosHears','argosLooks','argosRises','argosGreeting')&&<Dog t={t} wag={a==='argosRises'||a==='argosGreeting'} x={290+q*(a==='argosRises'?42:0)} y={1550-q*(a==='argosRises'?20:0)}/>}
   {actionIn(a,'oldNurseWashes','scarDiscovered','nurseRecognizes','silenceAgreed')&&<>
    <RoleActor role="nurse" x={680} y={1525} scale={1.35} t={t} gesture="reach"/>
    <g transform="translate(455 1500)"><path d="M-204 0Q-155 150 0 170Q155 150 205 0Z" fill="#a2785b" stroke="#62483b" strokeWidth="13"/><ellipse rx="207" ry="55" fill="#6ca1a5" stroke="#d5d7bc" strokeWidth="10"/>
    {[0,1,2].map(i=><ellipse key={i} cx={-80+i*80} cy="5" rx={28+Math.sin(t*7+i)*5} ry="9" fill="none" stroke="#d7ebdf" strokeWidth="6"/>)}</g>
    {a==='scarDiscovered'&&<path d="M452 1330l110 37" stroke="#8c5147" strokeWidth="11"/>}
   </>}
   {actionIn(a,'suitorsFeast','bowAttempt','odysseusTakesBow','bowBends','arrowTargets','suitorsRecoil','hallSecured')&&<>
    {[0,1,2].map(i=><RoleActor key={i} role="suitor" x={170+i*340} y={1530} scale={1.13+i*.08} t={t+i} gesture={a==='suitorsRecoil'?'reach':''} opacity={a==='hallSecured'?.4:1}/>)}
    {(a==='bowAttempt'||a==='odysseusTakesBow'||a==='bowBends'||a==='arrowTargets')&&<g transform="translate(555 1070)">
      <path d={'M-100 175Q'+(-230-q*110)+' 0 -100 -185'} stroke="#825c39" strokeWidth="24" fill="none"/>
      <path d="M-100 175L-100 -185" stroke="#e4d0aa" strokeWidth="8"/>
      {a==='arrowTargets'&&<path d={'M-100 -18L'+(300+q*230)+' -18'} stroke="#d6b88c" strokeWidth="12"/>}
    </g>}
    {a==='arrowTargets'&&[0,1,2].map(i=><ellipse key={i} cx={800+i*72} cy="1360" rx="19" ry="75" fill="none" stroke="#ccb184" strokeWidth="13"/>)}
   </>}
   {actionIn(a,'penelopeApproaches','facesUncertain','memoriesReturn','recognitionDawns','handsReach','reunionEmbrace','quietNight','bedSecret','oliveTreeReveal','proofOfHome','familyAtOlive')&&
     <RoleActor role="penelope" x={760-q*(a==='reunionEmbrace'?190:75)} y={1555} scale={1.43} t={t} gesture={actionIn(a,'handsReach','reunionEmbrace','recognitionDawns')?'reach':''}/>}
   {actionIn(a,'bedSecret','oliveTreeReveal','proofOfHome','handsReach','reunionEmbrace','quietNight')&&<g>
     <path d="M110 1430H950V1690H110Z" fill="#806342" stroke="#3a302b" strokeWidth="20"/>
     <path d="M170 1392H900V1498H170Z" fill="#d9c197" stroke="#67503c" strokeWidth="18"/>
     <path d="M198 1690L198 1070Q180 920 290 810" stroke="#5d4a32" strokeWidth="63" fill="none" strokeLinecap="round"/>
     <ellipse cx="310" cy="835" rx="225" ry="90" fill="#67795d"/>
     <path d="M230 1510V1690M870 1510V1690" stroke="#9f7d50" strokeWidth="38"/>
   </g>}
   {actionIn(a,'fatherSonTogether','palaceRestored','familyAtOlive','morningReckoning')&&<RoleActor role="telemachus" x={800} y={1570} scale={1.4} t={t} gesture="reach"/>}
   {actionIn(a,'familyAtOlive','palaceRestored')&&<RoleActor role="penelope" x={620} y={1570} scale={1.4} t={t} gesture="reach"/>}
   {actionIn(a,'shoreSunrise','seaAtPeace','islandPanorama','finalSilhouette')&&<path d="M0 1500Q350 1410 700 1460T1080 1470V1920H0Z" fill="#d1b08b" opacity=".52"/>}
   {showHero&&hero}
 </g>;
};
export type OdysseyAnimationProps={offsetSeconds?:number;sampleSeconds?:number[]};
export const OdysseyFullAnimation:React.FC<OdysseyAnimationProps>=({offsetSeconds=0,sampleSeconds})=>{
 const frame=useCurrentFrame(),{fps}=useVideoConfig();
 let time=offsetSeconds+frame/fps;
 if(sampleSeconds?.length){const clip=3;const n=Math.min(sampleSeconds.length-1,Math.floor(frame/fps/clip));time=sampleSeconds[n]!+(frame/fps-n*clip)}
 time=clamp(time,0,ODYSSEY_TOTAL_SECONDS-.0001);
 const beat=getOdysseyBeat(time),local=time-beat.start,duration=beat.end-beat.start;
 const world=beat.action==='weavingNight'?'penelope':beat.action==='ithacaWaiting'?'ithaca':beat.location;
 const first=ODYSSEY_BEATS.find(b=>b.chapter===beat.chapter)?.id===beat.id;
 // Direct cinematic cuts between discrete actions: no 0.2+0.28s fade-to-black at each of 110 beats.
 // Original fades cost ~50 seconds of repeated dark flashes across the feature film.
 const alpha=1;
 const progress=clamp(local/duration);
 const zoom=beat.action==='boulderSeals'?1.07:beat.action==='prisonersWatch'?1.18:beat.action==='wineToGiant'?1.12:beat.action==='cyclopsArrival'?1:1.025+((Number(beat.id.split('-')[1])%3)*.035);
 const cameraX=(W-W*zoom)*.5, cameraY=(H-H*zoom)*.52;
 return <AbsoluteFill style={{backgroundColor:shade,overflow:'hidden'}}>
  <svg width={W} height={H} viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,opacity:alpha}}>
   <g transform={'translate('+cameraX+' '+cameraY+') scale('+zoom+')'}>
    <Stage world={world} id={beat.id} time={local} progress={progress}/>
    <OnlyScene action={beat.action} time={local} duration={duration} world={world}/>
   </g>
  </svg>
  {first&&<div style={{position:'absolute',top:175,left:75,right:75,color:'#f2debc',fontFamily:'Georgia,serif',fontSize:55,fontWeight:700,letterSpacing:2,textShadow:'0 2px 12px #14222a',opacity:ease(local/.5)*ease((4-local)/.8)}}>{beat.chapter}</div>}
 </AbsoluteFill>;
};