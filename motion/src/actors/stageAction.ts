// Shared world-space choreography. Lever and the glove target the same point.
// No camera-specific "magic numbers" scattered across visual components.
export const ease=(n:number)=>{const t=Math.max(0,Math.min(1,n));return t*t*(3-2*t);};
export const remap=(t:number,start:number,end:number)=>ease((t-start)/(end-start));
export type Point={x:number;y:number};
export const actorScale=1.05;
export const actorOrigin={x:115,y:652};
export const leverPivot={x:905,y:1290};
export const leverLength=108;
export function actorDrift(t:number):number{
 const points:[number,number][]=[[0,-180],[2.8,0],[6,0],[9.5,-40]];
 for(let i=0;i<points.length-1;i++){
   const [t0,x0]=points[i],[t1,x1]=points[i+1];
   if(t<=t1)return x0+(x1-x0)*Math.max(0,Math.min(1,(t-t0)/(t1-t0)));
 }
 return -40;
}
export function leverProgress(t:number):number{return remap(t,6.85,8.1);}
export function leverAngle(t:number):number{return -46+76*leverProgress(t);}
export function leverKnob(t:number):Point{
 const a=leverAngle(t)*Math.PI/180;
 return {x:leverPivot.x+leverLength*Math.sin(a),
         y:leverPivot.y-leverLength*Math.cos(a)};
}
export function leverGripWrist(t:number):Point{
 const knob=leverKnob(t);
 return {
  x:(knob.x-actorOrigin.x-actorDrift(t))/actorScale-120,
  y:(knob.y-actorOrigin.y)/actorScale+112
 };
}
export function wristFingerWorld(wrist:Point,t:number):Point{
 return {x:actorOrigin.x+actorDrift(t)+actorScale*(wrist.x+120),
         y:actorOrigin.y+actorScale*(wrist.y-112)};
}
