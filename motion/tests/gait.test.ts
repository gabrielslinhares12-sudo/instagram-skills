import test from 'node:test';
import assert from 'node:assert/strict';
import {sampleGait,kneeIK,plantedWorldX} from '../src/actors/gait';

test('feet never slide in the middle of a planted stance',()=>{
 for(const [style,speed] of [['walk',100],['run',200],['creep',48]] as const){
  const period=style==='walk'?.96:style==='run'?.58:1.48;
  let prev:number|null=null;
  for(let t=.04;t<period*.39;t+=1/60){
   const g=sampleGait(t,style,speed);
   assert.equal(g.left.contact,true);
   const x=plantedWorldX(t,'left',style,speed);
   if(prev!==null)assert.ok(Math.abs(x-prev)<1e-7);
   prev=x;
  }
 }
});

test('both feet remain above ground and walk/creep always have a support',()=>{
 for(const style of ['walk','run','creep'] as const){
  for(let i=0;i<151;i++){
   const g=sampleGait(i/60,style,110);
   assert.ok(g.left.ankle.y<=553.01);
   assert.ok(g.right.ankle.y<=553.01);
   if(style!=='run')assert.ok(g.left.contact||g.right.contact);
  }
 }
});

test('inverse kinematics preserves human-like thigh/calf lengths',()=>{
 for(let x=-75;x<=75;x+=5)for(let y=494;y<=547;y+=7){
   const hip={x:145,y:395},ankle={x:hip.x+x,y};
   const knee=kneeIK(hip,ankle,91,87,-1);
   const a=Math.hypot(knee.x-hip.x,knee.y-hip.y);
   const b=Math.hypot(knee.x-ankle.x,knee.y-ankle.y);
   assert.ok(a<94&&a>80);
   assert.ok(b<94&&b>80);
 }
});

test('random-access render order does not affect a gait frame',()=>{
 for(const t of [0,.07,.35,2.04,6.4,19.82]){
  assert.deepEqual(sampleGait(t,'walk',94),sampleGait(t,'walk',94));
 }
});
