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
