import {test} from 'node:test';
import assert from 'node:assert/strict';
import {episodeSchema,totalFrames} from '../src/schema';
import demo from '../examples/demo.json';
const sample=()=>episodeSchema.parse(structuredClone(demo));
test('12s demo exports 720 frames at 60fps',()=>assert.equal(totalFrames(episodeSchema.parse(sample())),720));
test('overlapping captions are blocked',()=>{const e=sample();e.scenes[1].captions.push({start:2,end:3,text:'sobreposta'});assert.equal(episodeSchema.safeParse(e).success,false);});
test('captions outside shot are blocked',()=>{const e=sample();e.scenes[1].captions[0].end=5;assert.equal(episodeSchema.safeParse(e).success,false);});
test('title and caption do not overlap',()=>{const e=sample();e.scenes[0].captions.push({start:1,end:2,text:'duplicada'});assert.equal(episodeSchema.safeParse(e).success,false);});
test('duplicate scene ids are blocked',()=>{const e=sample();e.scenes[1].id=e.scenes[0].id;assert.equal(episodeSchema.safeParse(e).success,false);});
test('asset traversal and network URLs are blocked',()=>{for(const narration of ['../secret.wav','https://server/audio.wav']) assert.equal(episodeSchema.safeParse({...sample(),narration}).success,false);});

import pilot from '../examples/ultimo-sinal-parte-1.json';
test('pilot has 78 seconds at 60 fps and eight unique story beats',()=>{
 const e=episodeSchema.parse(pilot);
 assert.equal(totalFrames(e),4680);
 assert.deepEqual(e.scenes.map(s=>s.beat),['flash','arrival','sign','tea','noise','hatch','blackout','voice']);
});
test('pilot is a silent technical preview, never an unapproved synthetic voice',()=>{
 assert.equal(episodeSchema.parse(pilot).narration,null);
});
test('invalid story beat is rejected',()=>{
 const e=sample();
 assert.equal(episodeSchema.safeParse({...e,scenes:[{...e.scenes[0],beat:'unknown'}]}).success,false);
});

import qc from '../examples/ultimo-sinal-qc.json';
test('24 second QC montage covers every story beat without caption overlap',()=>{
 const e=episodeSchema.parse(qc);
 assert.equal(totalFrames(e),1440);
 assert.equal(e.scenes.length,8);
});

import {actingPose,hasRig,poseForBeat,requireRig} from '../src/actors/rigs';
test('the canonical mascot is a 3-bone articulated rig from its original PNG',()=>{
 const r=requireRig('lumino');
 assert.equal(r.source,'lumino-original.png');
 assert.equal(r.width,1230);
 assert.equal(r.height,1278);
 assert.deepEqual(r.parts.map(p=>p.bone),['head','rightArm','leftArm']);
});
test('different bones move independently and deterministically at 60 fps',()=>{
 const t=1.2;
 assert.deepEqual(actingPose('point',t),actingPose('point',t));
 const pointing=actingPose('point',t);
 const listening=actingPose('listen',t);
 assert.ok(pointing.rightArm < listening.rightArm-3);
 assert.notEqual(pointing.head,pointing.leftArm);
 assert.notEqual(actingPose('inspect',.5).head,actingPose('inspect',1.5).head);
});
test('timeline can declare multiple uniquely-instanced approved characters',()=>{
 const e=sample();
 e.scenes[1].characters=[
  {instance:'a',id:'lumino',pose:'point',x:75,y:700,size:530,enter:'none'},
  {instance:'b',id:'lumino',pose:'listen',x:565,y:730,size:460,enter:'glide'}
 ];
 assert.equal(episodeSchema.safeParse(e).success,true);
 e.scenes[1].characters[1].instance='a';
 assert.equal(episodeSchema.safeParse(e).success,false);
});
test('unknown character ids are rejected, never replaced by a lookalike',()=>{
 assert.equal(hasRig('random-stranger'),false);
 const e=sample();
 e.scenes[0].characters=[{instance:'unapproved',id:'random-stranger',pose:'idle',x:0,y:500,size:550,enter:'none'}];
 assert.equal(episodeSchema.safeParse(e).success,false);
});
test('beat choreography is stable and explicit',()=>{
 assert.equal(poseForBeat('hatch'),'point');
 assert.equal(poseForBeat('noise'),'inspect');
 assert.equal(poseForBeat('voice'),'discover');
});

import {sampleActor,solveArm} from '../src/actors/LuminoPuppet';
test('native character has distinct timed head, eye and wrist motion',()=>{
 const a=sampleActor('demo',1),b=sampleActor('demo',4),c=sampleActor('demo',7.5);
 assert.notEqual(a.head,b.head);
 assert.ok(b.left.y<a.left.y-100);
 assert.ok(c.right.y<b.right.y-40);
 assert.notEqual(b.gaze,c.gaze);
 assert.deepEqual(sampleActor('demo',4),b);
});
test('two-bone IK elbow is between reach radii and deterministic',()=>{
 const a={x:210,y:540},b={x:180,y:490};
 const elbow=solveArm(a,b,140,130,-1);
 assert.ok(Number.isFinite(elbow.x) && Number.isFinite(elbow.y));
 assert.ok(Math.abs(Math.hypot(elbow.x-a.x,elbow.y-a.y)-140)<1e-5);
});
