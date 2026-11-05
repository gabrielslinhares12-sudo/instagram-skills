import React,{useId} from 'react';

/**
 * Lúmino is modeled as a native 2D actor, not an image or a masked PNG.
 * All moving pieces are original SVG shapes: articulated two-link arms,
 * separate head rotation, eyes, bulb, gloves, magnifier and coat tails.
 * Visual reference: content/brand/lumino-original.png.
 * Intentional stylistic reconstruction for animation; review against master
 * before releasing. No mouth, legs or shoes.
 */
export type ActorGesture='idle'|'arrive'|'look'|'point'|'inspect'|'listen'|'react'|'discover'|'demo';
type Vec={x:number;y:number};
type PoseState={head:number;body:number;left:Vec;right:Vec;gaze:number;eyes:number;intensity:number;tail:number};
const BASE:PoseState={head:0,body:0,left:{x:155,y:672},right:{x:616,y:551},gaze:0,eyes:1,intensity:1,tail:0};
const POSES:Record<Exclude<ActorGesture,'demo'>,Partial<PoseState>>={
 idle:{},arrive:{head:-4,body:-2,right:{x:620,y:532}},
 look:{head:-9,gaze:-7,right:{x:618,y:565}},
 inspect:{head:-10,gaze:-9,left:{x:175,y:500},right:{x:612,y:572}},
 point:{head:4,gaze:8,right:{x:677,y:465}},
 listen:{head:7,gaze:-4,left:{x:175,y:660}},
 react:{head:-11,body:-4,left:{x:110,y:590},right:{x:650,y:485},eyes:.63,intensity:1.5},
 discover:{head:3,gaze:8,left:{x:172,y:505},right:{x:660,y:470},intensity:1.55}
};
type Timed={time:number;state:Partial<PoseState>};
const STORY:Timed[]=[
 {time:0,state:{head:-7,body:-2,left:{x:146,y:682},right:{x:612,y:555},gaze:-7,intensity:.85}},
 {time:2.2,state:{head:-1,left:{x:155,y:670},right:{x:617,y:550},gaze:-2,intensity:1}},
 {time:3.6,state:{head:-11,left:{x:177,y:492},right:{x:614,y:565},gaze:-9,intensity:1.2}},
 {time:5.5,state:{head:-6,left:{x:183,y:502},right:{x:627,y:559},gaze:-7,intensity:1.25}},
 {time:7.25,state:{head:5,left:{x:156,y:664},right:{x:680,y:497},gaze:9,intensity:1.22}},
 {time:8.35,state:{head:-13,body:-5,left:{x:128,y:598},right:{x:657,y:503},gaze:-9,eyes:.58,intensity:1.8}},
 {time:10,state:{head:2,body:1,left:{x:170,y:620},right:{x:625,y:540},gaze:4,eyes:1,intensity:1.4}}
];
const clamp=(n:number,a=0,b=1)=>Math.min(b,Math.max(a,n));
const ease=(x:number)=>{const t=clamp(x);return t*t*(3-2*t);};
const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
const merge=(a:PoseState,part:Partial<PoseState>):PoseState=>({
 ...a,...part,left:{...a.left,...part.left},right:{...a.right,...part.right}
});
function poseMix(a:PoseState,b:PoseState,k:number):PoseState{
 return {head:mix(a.head,b.head,k),body:mix(a.body,b.body,k),
 left:{x:mix(a.left.x,b.left.x,k),y:mix(a.left.y,b.left.y,k)},
 right:{x:mix(a.right.x,b.right.x,k),y:mix(a.right.y,b.right.y,k)},
 gaze:mix(a.gaze,b.gaze,k),eyes:mix(a.eyes,b.eyes,k),
 intensity:mix(a.intensity,b.intensity,k),tail:mix(a.tail,b.tail,k)};
}
export function sampleActor(gesture:ActorGesture,time:number):PoseState{
 const t=Math.max(0,time);
 let p:PoseState;
 if(gesture==='demo'){
   p=merge(BASE,STORY[0].state);
   for(let i=0;i<STORY.length-1;i++){
     const a=STORY[i],b=STORY[i+1];
     if(t>=a.time&&t<=b.time){
       p=poseMix(merge(BASE,a.state),merge(BASE,b.state),ease((t-a.time)/(b.time-a.time)));
       break;
     }
     if(t>b.time)p=merge(BASE,b.state);
   }
 }else{
   p=poseMix(BASE,merge(BASE,POSES[gesture]),ease(t/.65));
 }
 const bob=Math.sin(t*2.6);
 return {...p,head:p.head+Math.sin(t*1.3)*1.1,
   body:p.body+Math.sin(t*1.8)*.7,
   tail:Math.sin(t*2.2)*5,
   intensity:p.intensity*(1+.08*bob)};
}
export function solveArm(shoulder:Vec,wrist:Vec,a:number,b:number,bend:number):Vec{
 const dx=wrist.x-shoulder.x,dy=wrist.y-shoulder.y;
 const raw=Math.hypot(dx,dy);
 const dist=clamp(raw,Math.abs(a-b)+.001,a+b-.001);
 const ang=Math.atan2(dy,dx);
 const theta=Math.acos(clamp((a*a+dist*dist-b*b)/(2*a*dist),-1,1));
 return {x:shoulder.x+a*Math.cos(ang+bend*theta),
         y:shoulder.y+a*Math.sin(ang+bend*theta)};
}
const Ellipse:React.FC<{x:number;y:number;rx:number;ry:number;fill:string;stroke?:string;sw?:number}>=({x,y,rx,ry,fill,stroke,sw})=>
 <ellipse cx={x} cy={y} rx={rx} ry={ry} fill={fill} stroke={stroke} strokeWidth={sw}/>;
export const LuminoPuppet:React.FC<{time:number;gesture?:ActorGesture;darkness?:number;width?:string|number;height?:string|number}>=
 ({time,gesture='idle',darkness=0,width=740,height=850})=>{
 const ids=useId().replace(/[^a-zA-Z0-9]/g,'');
 const id=(name:string)=>'lumino-'+ids+'-'+name;
 const pose=sampleActor(gesture,time);
 const leftS={x:212,y:548},rightS={x:506,y:549};
 const leftE=solveArm(leftS,pose.left,140,130,-1);
 const rightE=solveArm(rightS,pose.right,148,135,1);
 const blink=gesture==='react'?pose.eyes:(Math.sin(time*3.2)> .997?.23:pose.eyes);
 const light=clamp(pose.intensity*(1-darkness),.08,2);
 const L='url(#'+id('metal')+')',G='url(#'+id('gold')+')',
       J='url(#'+id('jacket')+')',GL='url(#'+id('glass')+')',
       W='url(#'+id('white')+')';
 const arm=(s:Vec,e:Vec,w:Vec,order:'left'|'right')=><g key={order}>
   <path d={'M'+s.x+' '+s.y+' Q'+e.x+' '+e.y+' '+w.x+' '+w.y}
     fill="none" stroke="#201a11" strokeWidth="89" strokeLinecap="round"/>
   <path d={'M'+s.x+' '+s.y+' Q'+e.x+' '+e.y+' '+w.x+' '+w.y}
     fill="none" stroke={J} strokeWidth="75" strokeLinecap="round"/>
   <path d={'M'+s.x+' '+s.y+' Q'+e.x+' '+e.y+' '+w.x+' '+w.y}
     fill="none" stroke="#d5ad55" strokeWidth="8" strokeLinecap="round" opacity=".52"/>
   <Ellipse x={e.x} y={e.y} rx={41} ry={40} fill={J} stroke="#272016" sw={7}/>
   <g transform={'translate('+w.x+' '+w.y+')'}>
    <Ellipse x={0} y={0} rx={48} ry={45} fill={G} stroke="#221914" sw={8}/>
    <Ellipse x={0} y={0} rx={39} ry={37} fill="#1b1c1b"/>
   </g>
 </g>;
 return <svg viewBox="0 0 740 850" width={width} height={height} style={{overflow:'visible',display:'block'}}>
 <defs>
  <linearGradient id={id('gold')} x1="0" y1="0" x2="1" y2=".9">
   <stop stopColor="#fff1a8"/><stop offset=".20" stopColor="#f6b936"/>
   <stop offset=".46" stopColor="#906026"/><stop offset=".67" stopColor="#f9ce53"/>
   <stop offset="1" stopColor="#62401f"/>
  </linearGradient>
  <linearGradient id={id('metal')} x1="0" y1=".1" x2="1" y2="1">
   <stop stopColor="#49301c"/><stop offset=".25" stopColor="#db8f26"/>
   <stop offset=".48" stopColor="#ffe285"/><stop offset=".75" stopColor="#9c5c20"/>
   <stop offset="1" stopColor="#33251a"/>
  </linearGradient>
  <linearGradient id={id('jacket')} x1=".05" y1="0" x2=".95" y2="1">
   <stop stopColor="#d1af65"/><stop offset=".38" stopColor="#998354"/>
   <stop offset=".72" stopColor="#584d37"/><stop offset="1" stopColor="#bd9250"/>
  </linearGradient>
  <linearGradient id={id('glass')} x1="0" y1=".2" x2="1" y2=".9">
   <stop stopColor="#e9fff3" stopOpacity=".82"/><stop offset=".34" stopColor="#ffebaf" stopOpacity=".25"/>
   <stop offset=".72" stopColor="#fff0bd" stopOpacity=".57"/><stop offset="1" stopColor="#c7d1c5" stopOpacity=".74"/>
  </linearGradient>
  <linearGradient id={id('white')} x1=".1" y1="0" x2=".8" y2="1">
   <stop stopColor="#fffdf4"/><stop offset=".63" stopColor="#e0dacc"/><stop offset="1" stopColor="#8b8c88"/>
  </linearGradient>
  <radialGradient id={id('bulb')}>
   <stop stopColor="#ffffff"/><stop offset=".21" stopColor="#fffbcb"/>
   <stop offset=".55" stopColor="#ffe36d"/><stop offset="1" stopColor="#e99922" stopOpacity=".1"/>
  </radialGradient>
  <radialGradient id={id('halo')}>
   <stop stopColor="#ffde79" stopOpacity=".52"/><stop offset=".58" stopColor="#ffcf54" stopOpacity=".2"/>
   <stop offset="1" stopColor="#ffd874" stopOpacity="0"/>
  </radialGradient>
  <linearGradient id={id('lens')} x1="0" y1="0" x2="1" y2="1">
   <stop stopColor="#b9fcfa" stopOpacity=".8"/><stop offset=".5" stopColor="#11687b" stopOpacity=".47"/>
   <stop offset="1" stopColor="#7ab2b7" stopOpacity=".7"/>
  </linearGradient>
 </defs>
 <g transform={'translate(360 620) rotate('+pose.body+') translate(-360 -620)'}>
  {/* Arm bones are rigged independently from the lantern and coat. */}
  {arm(leftS,leftE,pose.left,'left')}
  {arm(rightS,rightE,pose.right,'right')}
  {/* Coat silhouette, independent hems and lapels. */}
  <path d={'M220 532 Q150 570 178 691 Q150 738 110 '+(805+pose.tail)+
   ' Q210 856 326 777 Q365 815 410 842 Q493 840 550 '+(807-pose.tail)+
   ' Q608 770 541 677 Q566 584 492 538 Q365 507 220 532Z'}
   fill="#2b251b" stroke="#191b1b" strokeWidth="17" strokeLinejoin="round"/>
  <path d={'M231 539 Q163 573 189 682 Q164 743 129 '+(795+pose.tail)+
    ' Q222 817 329 748 Q360 783 411 825 Q483 800 534 '+(788-pose.tail)+
    ' Q568 754 517 683 Q543 575 480 541Z'}
   fill={J} stroke="#d6b267" strokeWidth="8"/>
  <path d="M288 539L421 539L435 754Q361 797 315 734Z" fill="#322b23"/>
  <path d="M329 560L386 561L391 718L370 749L344 720Z" fill="#1b2428"/>
  <path d="M344 553L377 555L370 620L358 643L346 609Z" fill="#b38439" stroke="#352719" strokeWidth="5"/>
  <path d="M247 545L327 632L301 678L227 617Z" fill="#d4b576" stroke="#3a3025" strokeWidth="11"/>
  <path d="M468 548L393 646L424 672L508 591Z" fill="#c5a264" stroke="#372b20" strokeWidth="11"/>
  <path d="M300 672L233 776L315 751" stroke="#554630" strokeWidth="9" fill="none"/>
  <path d="M426 686L490 768L431 770" stroke="#51432d" strokeWidth="9" fill="none"/>
  {[0,1,2].map((n)=><g key={n}>
    <circle cx={275+(n%2)*176} cy={665+n*37} r="17" fill={G} stroke="#45301d" strokeWidth="6"/>
    <circle cx={272+(n%2)*176} cy={661+n*37} r="5" fill="#fff2ae"/>
   </g>)}
  {/* Separate head: tilt and scan without rotating the body. */}
  <g transform={'translate(360 524) rotate('+pose.head+') translate(-360 -524)'}>
   <ellipse cx="363" cy="314" rx="271" ry="286" fill={'url(#'+id('halo')+')'} opacity={clamp(light/1.6)}/>
   <path d="M263 515 Q350 557 469 510 L463 562 Q367 601 258 563Z" fill={G} stroke="#2a221b" strokeWidth="11"/>
   <path d="M165 183 C105 112 127 56 204 49 Q353 0 498 55 C574 82 593 125 560 196" fill="none" stroke="#221c16" strokeWidth="23"/>
   <path d="M171 181 C122 120 137 65 208 60 Q357 15 492 65 C561 92 574 126 553 185" fill="none" stroke={G} strokeWidth="13"/>
   <path d="M344 60 Q305 18 356 3 Q412 -7 414 55" fill="none" stroke="#382619" strokeWidth="20"/>
   <path d="M347 56 Q326 16 358 15 Q393 17 399 58" fill="none" stroke={L} strokeWidth="13"/>
   <ellipse cx="375" cy="63" rx="43" ry="26" fill={G} stroke="#3a2717" strokeWidth="9"/>
   {/* Glass dome and frame */}
   <path d="M206 174Q357 109 510 179Q593 248 572 397Q544 509 392 525Q225 524 155 423Q117 290 206 174Z"
     fill={GL} stroke="#352719" strokeWidth="26"/>
   <path d="M213 196Q360 137 495 196" fill="none" stroke="#fff7c8" strokeWidth="22" opacity=".65"/>
   <ellipse cx="373" cy="330" rx="116" ry="158" fill={'url(#'+id('bulb')+')'} opacity={clamp(light*.88)}/>
   <rect x="355" y="205" width="43" height="42" rx="8" fill={L} stroke="#6b431a" strokeWidth="8"/>
   <path d="M366 245V402M386 247V401" stroke="#fdf3ae" strokeWidth="10"/>
   <ellipse cx="375" cy="400" rx="51" ry="27" fill="#ffe89a" stroke="#e3aa2a" strokeWidth="7"/>
   <path d="M318 280Q351 250 368 303T419 286" stroke="#fff9dc" strokeWidth="10" fill="none" opacity={clamp(light)}/>
   {/* Cap and side hinge */}
   <path d="M197 205Q365 121 519 207L551 238Q365 179 173 244Z" fill={L} stroke="#241d16" strokeWidth="14"/>
   <path d="M249 125Q357 69 468 125L486 186Q363 147 232 188Z" fill={G} stroke="#2c2118" strokeWidth="12"/>
   {[0,1,2,3,4,5].map(n=><rect key={n} x={267+n*35} y={147+Math.sin(n/5*Math.PI)*-22} width="15" height="28" rx="7" fill="#211b16" transform={'rotate('+(n-2)*5+' '+(267+n*35)+' 155)'}/>)}
   <ellipse cx="162" cy="305" rx="33" ry="54" fill={L} stroke="#33231a" strokeWidth="12"/>
   <ellipse cx="564" cy="305" rx="29" ry="52" fill={G} stroke="#33231a" strokeWidth="11"/>
   {/* Animated glasses: eyes scan and blink independently of lantern. */}
   {[{x:276,y:362},{x:452,y:341}].map(({x,y},index)=><g key={index}>
     <ellipse cx={x} cy={y} rx="93" ry="99" fill="#231c18" stroke={G} strokeWidth="20"/>
     <ellipse cx={x} cy={y} rx="75" ry="80" fill="#041b27" stroke="#352b20" strokeWidth="6"/>
     <g transform={'translate('+pose.gaze+' 0) translate('+x+' '+y+') scale(1 '+blink+') translate('+(-x)+' '+(-y)+')'}>
       <path d={'M'+(x-38)+' '+(y+26)+' Q'+(x-49)+' '+(y-48)+' '+x+' '+(y-45)+
         ' Q'+(x+46)+' '+(y-40)+' '+(x+41)+' '+(y+17)}
         fill="none" stroke="#43ecff" strokeWidth="15" strokeLinecap="round"/>
       <path d={'M'+(x-33)+' '+(y+19)+' Q'+x+' '+(y-60)+' '+(x+32)+' '+(y+15)}
         fill="none" stroke="#bffaff" strokeWidth="4" opacity=".85"/>
     </g>
     <path d={'M'+(x-48)+' '+(y-56)+' Q'+x+' '+(y-88)+' '+(x+39)+' '+(y-66)}
       stroke="#ffffff" strokeWidth="8" opacity=".25" fill="none"/>
    </g>)}
   <path d="M365 355Q367 348 376 355" stroke="#3c2a20" strokeWidth="9" fill="none"/>
   <path d="M203 285Q200 415 267 458" stroke="#ffffff" strokeWidth="17" fill="none" opacity=".36"/>
  </g>
  {/* Real props attached to animated wrists, not separate stickers. */}
  <g transform={'translate('+pose.left.x+' '+pose.left.y+')'}>
    <path d="M-2 -12L-18 -102" stroke="#291e18" strokeWidth="31" strokeLinecap="round"/>
    <path d="M-2 -12L-18 -102" stroke={G} strokeWidth="20" strokeLinecap="round"/>
    <circle cx="-28" cy="-155" r="98" fill={'url(#'+id('lens')+')'} stroke="#291d13" strokeWidth="25"/>
    <circle cx="-28" cy="-155" r="94" fill="none" stroke={G} strokeWidth="19"/>
    <path d="M-79 -195Q-50 -227 -20 -212" fill="none" stroke="#d8ffff" strokeWidth="17" strokeLinecap="round" opacity=".86"/>
    <ellipse cx="4" cy="0" rx="46" ry="45" fill={W} stroke="#322925" strokeWidth="9"/>
    <path d="M-18 -12Q-28 -46 -8 -46Q19 -38 26 -3" fill={W} stroke="#47403b" strokeWidth="7"/>
    <path d="M-16 18Q6 35 30 16" stroke="#a7a7a0" strokeWidth="8" fill="none"/>
  </g>
  <g transform={'translate('+pose.right.x+' '+pose.right.y+')'}>
    <path d="M-17 4 Q-44 -18 -34 -42 Q-25 -60 0 -45 L20 -24 Q43 -45 55 -70 L100 -121 Q120 -134 135 -115 Q147 -97 131 -76 L79 -20 Q78 13 42 27Z"
      fill={W} stroke="#302823" strokeWidth="10" strokeLinejoin="round"/>
    <path d="M14 -21Q38 8 61 -5" fill="none" stroke="#77736b" strokeWidth="6"/>
    <path d="M42 -35L73 -48" stroke="#c2bbb0" strokeWidth="5"/>
  </g>
 </g>
 </svg>;
};
