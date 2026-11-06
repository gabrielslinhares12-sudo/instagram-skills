import {test} from 'node:test';
import assert from 'node:assert/strict';
import {ODYSSEY_BEATS,ODYSSEY_EPISODES,ODYSSEY_TOTAL_SECONDS,verifyOdysseyTimeline,getOdysseyBeat,odysseyFrameCount} from '../src/odysseyTimeline';
test('continuous narrative timeline covers 560.1 seconds with unique choreography',()=>{
 assert.equal(verifyOdysseyTimeline(),true);
 assert.equal(ODYSSEY_BEATS.length,new Set(ODYSSEY_BEATS.map(x=>x.action)).size);
 assert.ok(ODYSSEY_BEATS.length>=95,'avoid repeated/recycled action shots');
 assert.ok(ODYSSEY_BEATS.every(x=>x.end>x.start&&x.end-x.start>=2));
 assert.equal(getOdysseyBeat(0).action,'burningTroia');
 assert.equal(getOdysseyBeat(560.1).action,'finalSilhouette');
 assert.equal(getOdysseyBeat(43).location,'cave');
 assert.equal(getOdysseyBeat(386).location,'wash');
});
test('three 60 fps episode boundaries preserve exact full duration',()=>{
 assert.equal(ODYSSEY_TOTAL_SECONDS,560.1);
 const frames=ODYSSEY_EPISODES.map(e=>odysseyFrameCount(e.start,e.end));
 assert.deepEqual(frames,[5316,13728,14562]);
 assert.equal(frames.reduce((a,b)=>a+b,0),33606);
 assert.equal(ODYSSEY_EPISODES[0].start,0);
 assert.equal(ODYSSEY_EPISODES[2].end,ODYSSEY_TOTAL_SECONDS);
});
test('full cyclops blocking is its own action between entrance and escape',()=>{
 const acts=ODYSSEY_BEATS.map(x=>x.action);
 assert.ok(acts.indexOf('cyclopsArrival')<acts.indexOf('boulderSeals'));
 assert.ok(acts.indexOf('boulderSeals')<acts.indexOf('ramEscape'));
 assert.ok(acts.indexOf('boulderSeals')>=0);
});