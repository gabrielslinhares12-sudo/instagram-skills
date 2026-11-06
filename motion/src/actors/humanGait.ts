// Deterministic 2D two-bone gait for frame-exact Remotion rendering (60 fps).
// No random drift, sliding feet or time-dependent integration.
export type GaitMode='idle'|'walk'|'creep'|'run';
export type Vec2=Readonly<{x:number;y:number}>;
export type LegPose=Readonly<{hip:Vec2;knee:Vec2;ankle:Vec2;toe:Vec2;planted:boolean;footAngle:number}>;
export type GaitPose=Readonly<{left:LegPose;right:LegPose;bob:number;tilt:number;armSwing:number;pace:number}>;
const TAU=2*Math.PI;
const clamp=(v:number,a:number,b:number)=>Math.max(a,Math.min(b,v));
const smooth=(x:number)=>{const p=clamp(x,0,1);return p*p*(3-2*p)};
const frac=(x:number)=>x-Math.floor(x);
export const HIP_LEFT=Object.freeze({x:142,y:401});
export const HIP_RIGHT=Object.freeze({x:211,y:401});
const KNEE_FORWARD=-1;
export function twoBoneIK(hip:Vec2,ankle:Vec2,upper:number,lower:number):Vec2{
 const dx=ankle.x-hip.x,dy=ankle.y-hip.y,raw=Math.hypot(dx,dy);
 const d=clamp(raw,Math.abs(upper-lower)+.0001,upper+lower-.0001);
 const nx=raw>0?dx/raw:0,ny=raw>0?dy/raw:1;
 const base=(upper*upper-lower*lower+d*d)/(2*d);
 const height=Math.sqrt(Math.max(0,upper*upper-base*base));
 return {x:hip.x+base*nx-KNEE_FORWARD*height*ny,y:hip.y+base*ny+KNEE_FORWARD*height*nx};
}
export function sampleGait(seconds:number,mode:GaitMode='walk'):GaitPose{
 const t=Math.max(0,seconds),active=mode!=='idle';
 const pace=mode==='run'?2.35:mode==='creep'?.82:mode==='walk'?1.45:0;
 const extent=mode==='run'?86:mode==='creep'?36:64;
 const lift=mode==='run'?62:mode==='creep'?22:42;
 const stance=mode==='run'?.43:mode==='creep'?.70:.61;
 const phase=t*pace;
 const leg=(hip:Vec2,offset:number):LegPose=>{
  if(!active){const ankle={x:hip.x+3,y:540};return {hip,knee:twoBoneIK(hip,ankle,95,92),ankle,toe:{x:ankle.x+31,y:549},planted:true,footAngle:0};}
  const p=frac(phase+offset),planted=p<stance,interval=planted?p/stance:(p-stance)/(1-stance);
  const dx=planted?extent*(1-2*interval):extent*(-1+2*smooth(interval));
  const ankle={x:hip.x+dx,y:540-(planted?0:lift*Math.sin(Math.PI*interval))};
  const knee=twoBoneIK(hip,ankle,95,92);
  const footAngle=planted?(p<stance*.18?-8:p>stance*.77?13:0):(1-interval)*(-19)+interval*8;
  return {hip,knee,ankle,toe:{x:ankle.x+33,y:ankle.y+9},planted,footAngle};
 };
 return {left:leg(HIP_LEFT,0),right:leg(HIP_RIGHT,.5),
  bob:active?Math.sin(TAU*phase*2)*4.7+(mode==='run'?6:0):Math.sin(t*1.8)*1.3,
  tilt:active?Math.sin(TAU*phase)*1.65:Math.sin(t*.9)*.5,
  armSwing:active?Math.sin(TAU*phase)*(mode==='run'?25:mode==='creep'?8:15):Math.sin(t*1.8)*1.3,
  pace};
}
