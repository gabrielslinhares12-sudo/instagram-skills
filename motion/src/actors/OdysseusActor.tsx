import React from 'react';
export type WarriorPose='listen'|'plan'|'point'|'craft'|'climb'|'creep'|'run'|'open'|'victory';
type XY={x:number;y:number};
const ease=(n:number)=>{const x=Math.min(1,Math.max(0,n));return x*x*(3-2*x);};
const between=(a:number,b:number,k:number)=>a+(b-a)*k;
const elbow=(a:XY,w:XY,bend:number):XY=>{
 const dx=w.x-a.x,dy=w.y-a.y;return {x:(a.x+w.x)/2+bend*dy*.25,y:(a.y+w.y)/2-bend*dx*.25};
};
/** Native 2D animation of the mythological Odysseus. Original drawing. */
export const Odysseus:React.FC<{time:number;pose:WarriorPose;night?:boolean}>=({time,pose,night=false})=>{
 const t=Math.max(0,time),k=ease(t/.7),walk=Math.sin(t*10);
 const running=pose==='run',rightTarget:XY=pose==='open'?{x:310,y:298}:
   pose==='point'||pose==='plan'?{x:316,y:164}:
   pose==='craft'?{x:330,y:218}:pose==='climb'?{x:260,y:151}:{x:265,y:369};
 const leftTarget:XY=pose==='open'?{x:70,y:291}:pose==='craft'?{x:57,y:215}:
   pose==='creep'?{x:89,y:299}:{x:75,y:348};
 const R={x:between(267,rightTarget.x,k),y:between(342,rightTarget.y,k)+(running?walk*22:0)};
 const L={x:between(80,leftTarget.x,k),y:between(345,leftTarget.y,k)-(running?walk*22:0)};
 const swing=Math.sin(t*1.4)*7+(running?walk*16:0);
 const body=Math.sin(t*1.7)*.7+(running?walk*1.8:0);
 const forearm=(shoulder:XY,wrist:XY,bend:number)=>{const e=elbow(shoulder,wrist,bend);
 return <g>
  <path d={'M'+shoulder.x+' '+shoulder.y+'Q'+e.x+' '+e.y+' '+wrist.x+' '+wrist.y} stroke="#2d2525" strokeWidth="48" strokeLinecap="round" fill="none"/>
  <path d={'M'+shoulder.x+' '+shoulder.y+'Q'+e.x+' '+e.y+' '+wrist.x+' '+wrist.y} stroke="#b97857" strokeWidth="36" strokeLinecap="round" fill="none"/>
  <path d={'M'+shoulder.x+' '+shoulder.y+'Q'+e.x+' '+e.y+' '+wrist.x+' '+wrist.y} stroke="#e4b28b" strokeWidth="8" strokeLinecap="round" opacity=".4" fill="none"/>
  <circle cx={e.x} cy={e.y} r="19" fill="#aa6d4d" stroke="#53382d" strokeWidth="6"/>
  <ellipse cx={wrist.x} cy={wrist.y} rx="25" ry="29" fill="#db9c70" stroke="#362b2a" strokeWidth="7"/>
  <path d={'M'+(wrist.x+10)+' '+(wrist.y-8)+'l16 -17'} stroke="#e0b08b" strokeWidth="11" strokeLinecap="round"/>
 </g>};
 return <svg width="100%" height="100%" viewBox="0 0 370 600" style={{overflow:'visible',display:'block'}}>
 <defs>
  <linearGradient id="bronze-greek" x1="0" y1="0" x2="1" y2=".8">
   <stop stopColor="#ffe5a1"/><stop offset=".27" stopColor="#bd864f"/>
   <stop offset=".64" stopColor="#7c482f"/><stop offset="1" stopColor="#ebb475"/>
  </linearGradient>
  <linearGradient id="cloak-greek" x1="0" y1="0" x2="1" y2="1">
   <stop stopColor="#d46758"/><stop offset=".47" stopColor="#933b43"/><stop offset="1" stopColor="#432632"/>
  </linearGradient>
  <linearGradient id="skin-greek" x1="0" y1="0" x2="1" y2="1">
   <stop stopColor="#f8cf9e"/><stop offset=".5" stopColor="#c58b66"/><stop offset="1" stopColor="#795042"/>
  </linearGradient>
  <linearGradient id="fabric-greek" x1="0" y1="0" x2="1" y2="1">
   <stop stopColor="#f0dfb8"/><stop offset=".54" stopColor="#a99a79"/><stop offset="1" stopColor="#615a53"/>
  </linearGradient>
 </defs>
 <g transform={'translate(180 320) rotate('+body+') translate(-180 -320)'}>
  {[{x:145,k:running?walk*25:0,dir:-1},{x:213,k:running?-walk*25:0,dir:1}].map((z,i)=><g key={i} transform={'translate('+z.k*.18+' '+Math.min(0,z.k)+')'}>
   <path d={'M'+z.x+' 398L'+(z.x+z.dir*8)+' 470L'+(z.x+z.dir*30)+' 537'}
    stroke="#362926" strokeWidth="47" strokeLinecap="round"/>
   <path d={'M'+z.x+' 408L'+(z.x+z.dir*8)+' 470'}
    stroke="#cc946a" strokeWidth="35" strokeLinecap="round"/>
   <path d={'M'+(z.x+z.dir*8)+' 472L'+(z.x+z.dir*29)+' 537'}
    stroke="#a57251" strokeWidth="32" strokeLinecap="round"/>
   <path d={'M'+(z.x+z.dir*30)+' 528L'+(z.x+z.dir*13)+' 550L'+(z.x+z.dir*61)+' 558Z'}
    fill="#342726" stroke="#1c1e20" strokeWidth="10"/>
   <path d={'M'+(z.x+z.dir*11)+' 479L'+(z.x+z.dir*28)+' 519'}
    stroke="#e6b67d" strokeWidth="7"/>
  </g>)}
  <path d={'M116 244Q42 260 '+(50+swing)+' 354Q'+(22+swing)+' 450 '+(12+swing)+' 503Q91 497 163 444L247 244Z'}
   fill="url(#cloak-greek)" stroke="#342127" strokeWidth="11"/>
  <path d={'M104 266Q72 395 '+(27+swing)+' 485'} stroke="#eb9881" strokeWidth="7" opacity=".35" fill="none"/>
  {forearm({x:123,y:264},L,-1)}
  {forearm({x:233,y:257},R,1)}
  <path d="M112 234Q180 207 244 238L264 352L235 409L122 410L96 352Z"
   fill="url(#fabric-greek)" stroke="#2e2928" strokeWidth="13"/>
  <path d="M126 249L238 248L231 349L127 347Z"
   fill="url(#bronze-greek)" stroke="#4d362b" strokeWidth="11"/>
  <path d="M125 280L232 273M127 311L233 308M128 336L230 333" stroke="#f9d496" strokeWidth="6" opacity=".63"/>
  <path d="M158 248Q168 303 179 346M208 250Q199 300 188 344"
   stroke="#503d32" strokeWidth="9" opacity=".55" fill="none"/>
  <path d="M112 347H245L240 393H117Z" fill="#70513d" stroke="#302b2c" strokeWidth="8"/>
  {[0,1,2,3,4].map(i=><path key={i} d={'M'+(128+i*26)+' 387l-12 43'}
   stroke="#b99160" strokeWidth="23" strokeLinecap="round"/>)}
  <path d="M118 249L149 302L125 321L95 269Z" fill="#c7a071" stroke="#332a27" strokeWidth="9"/>
  <path d="M240 251L211 298L234 319L265 269Z" fill="#b99570" stroke="#332a27" strokeWidth="9"/>
  <circle cx="181" cy="281" r="17" fill="#efc680" stroke="#6e4b2f" strokeWidth="6"/>
  <path d="M152 208H214L208 243H156Z" fill="#b37b5d" stroke="#3d2c27" strokeWidth="8"/>
  <g transform={'translate(180 213) rotate('+(pose==='plan'?-3:pose==='victory'?4:0)+') translate(-180 -213)'}>
   <path d="M142 141Q175 117 216 140Q232 173 218 207L201 230L160 230L136 203Q123 166 142 141Z"
     fill="url(#skin-greek)" stroke="#3a2928" strokeWidth="10"/>
   <path d="M137 184Q155 214 166 214L174 251Q206 239 222 194L202 221L178 232L155 218Z"
     fill="#302527" stroke="#292426" strokeWidth="8"/>
   <path d="M132 149Q146 110 208 123Q227 130 229 154L210 147L197 134L150 145Z"
     fill="#272428"/>
   <path d="M151 175h18M191 173h18" stroke="#2e2524" strokeWidth="8"/>
   <ellipse cx="164" cy="181" rx="4" ry="5" fill="#0e1b20"/>
   <ellipse cx="203" cy="179" rx="4" ry="5" fill="#0e1b20"/>
   <path d="M181 180L175 201L186 205" fill="none" stroke="#82563f" strokeWidth="6"/>
   <path d="M159 220Q181 230 207 218" fill="none" stroke="#64402f" strokeWidth="6"/>
   <path d="M137 152Q181 118 223 151L221 130Q178 95 146 129Z"
    fill="url(#bronze-greek)" stroke="#3f2a26" strokeWidth="10"/>
   <path d="M140 130L142 103Q185 72 221 105L224 135" fill="url(#bronze-greek)"
    stroke="#352626" strokeWidth="8"/>
   <path d="M147 110Q174 52 218 67Q253 75 267 102Q214 79 170 100Z"
    fill="url(#cloak-greek)" stroke="#3c242c" strokeWidth="9"/>
  </g>
  {night&&<path d="M117 237Q178 218 247 242" stroke="#c1dae4" strokeWidth="6" opacity=".22"/>}
 </g>
 </svg>;
};
