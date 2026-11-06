/** Deterministic ground-aware gait. Planted feet remain fixed in world coordinates. */
export type XY={x:number;y:number};
export type GaitStyle='walk'|'run'|'creep'|'limp'|'stand';
export type FootPose={ankle:XY;toe:XY;heel:XY;contact:boolean;phase:number;pitch:number};
export type GaitFrame={left:FootPose;right:FootPose;bodyY:number;hipSway:number;lean:number;armPhase:number;style:GaitStyle;speed:number;cycleSeconds:number};
const clamp=(n:number,a:number,b:number)=>Math.min(b,Math.max(a,n));
const smooth=(x:number)=>{const n=clamp(x,0,1);return n*n*(3-2*n);};
const frac=(n:number)=>n-Math.floor(n);
const profiles:Record<GaitStyle,{period:number;stance:number;lift:number;bob:number;lean:number}>={
 walk:{period:.96,stance:.64,lift:27,bob:8,lean:2.0},
 run:{period:.58,stance:.43,lift:59,bob:16,lean:7.6},
 creep:{period:1.48,stance:.73,lift:15,bob:4,lean:5.0},
 limp:{period:1.24,stance:.71,lift:18,bob:7,lean:4.3},
 stand:{period:2.00,stance:1,lift:0,bob:1,lean:0}
};
const foot=(t:number,offset:number,speed:number,style:GaitStyle,ground:number):FootPose=>{
 const p=profiles[style];
 if(style==='stand')return {ankle:{x:0,y:ground},toe:{x:21,y:ground+7},heel:{x:-21,y:ground+7},contact:true,phase:0,pitch:0};
 const phase=frac(t/p.period+offset);
 const stanceDist=Math.abs(speed)*p.period*p.stance;
 let dx:number,y:number,pitch:number,contact:boolean;
 if(phase<p.stance){
   // Derivative of dx with respect to seconds exactly cancels root travel.
   dx=stanceDist/2-Math.abs(speed)*p.period*phase;
   const contactFrac=phase/p.stance;
   y=ground+(contactFrac<.13?3*(1-contactFrac/.13):0);
   pitch=contactFrac<.15?-11*(1-contactFrac/.15):contactFrac>.79?7*(contactFrac-.79)/.21:0;
   contact=true;
 }else{
   const swing=(phase-p.stance)/(1-p.stance);
   dx=-stanceDist/2+stanceDist*smooth(swing);
   y=ground-p.lift*Math.sin(Math.PI*swing);
   pitch=17*Math.sin(Math.PI*swing);
   contact=false;
 }
 if(style==='limp'&&offset===.5){y=ground-(ground-y)*.6;pitch*=.65;}
 const direction=speed<0?-1:1;
 const x=dx*direction;
 return {ankle:{x,y},toe:{x:direction*24,y:y+10-Math.sin(pitch*Math.PI/180)*12},heel:{x:-direction*17,y:y+9+Math.sin(pitch*Math.PI/180)*9},contact,phase,pitch:pitch*direction};
};
export function kneeIK(hip:XY,ankle:XY,thigh=87,shin=87,forward=1):XY{
 let dx=ankle.x-hip.x,dy=ankle.y-hip.y;
 const d=Math.max(.001,Math.hypot(dx,dy));
 const reach=clamp(d,Math.abs(thigh-shin)+.1,thigh+shin-.1);
 dx*=reach/d;dy*=reach/d;
 const unitX=dx/reach,unitY=dy/reach;
 const along=(thigh*thigh-shin*shin+reach*reach)/(2*reach);
 const height=Math.sqrt(Math.max(0,thigh*thigh-along*along));
 return {x:hip.x+unitX*along+height*(-unitY)*forward,
         y:hip.y+unitY*along+height*unitX*forward};
}
export function sampleGait(t:number,style:GaitStyle,speed:number,ground=550):GaitFrame{
 const p=profiles[style],seconds=Math.max(0,t),moving=style!=='stand';
 const left=foot(seconds,0,moving?speed:0,style,ground);
 const right=foot(seconds,.5,moving?speed:0,style,ground);
 const stridePhase=seconds/p.period*2*Math.PI;
 const bodyY=moving?-p.bob*(.3+.7*Math.abs(Math.cos(stridePhase))):Math.sin(seconds*1.6);
 const hipSway=moving?Math.sin(stridePhase)*2.4:Math.sin(seconds*.75)*.5;
 const lean=(speed<0?-1:1)*p.lean;
 return {left,right,bodyY,hipSway,lean,armPhase:Math.sin(stridePhase),style,speed,cycleSeconds:p.period};
}
export function plantedWorldX(t:number,side:'left'|'right',style:GaitStyle,speed:number):number{
 const f=sampleGait(t,style,speed);
 const part=side==='left'?f.left:f.right;
 return t*speed+part.ankle.x;
}
