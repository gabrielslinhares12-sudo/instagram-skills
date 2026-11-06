import test from 'node:test';
import assert from 'node:assert/strict';
import manifest from '../odyssey/PLANO-50-TOMADAS-3-EPISODIOS.json';

type Shot=typeof manifest.shots[number];
test('A Odisseia: 50 cinematic shots across the original 560.1 seconds',()=>{
 assert.equal(manifest.shots.length,50);
 assert.equal(manifest.source_duration_seconds,560.1);
 assert.equal(manifest.episodes.length,3);
 assert.equal(manifest.shots[0].start,0);
 assert.equal(manifest.shots.at(-1)?.end,560.1);
 assert.deepEqual([1,2,3].map(x=>manifest.shots.filter(s=>s.episode===x).length),[11,19,20]);
 for(let i=1;i<manifest.shots.length;i++){
   assert.equal(manifest.shots[i].start,manifest.shots[i-1].end,'no missing/overlapping narration interval');
 }
});
test('No recycled story shot IDs, sets or action blocking',()=>{
 const shots=manifest.shots as Shot[];
 for(const field of ['id','layout_signature','action'] as const){
  const items=shots.map(s=>s[field]);
  assert.equal(new Set(items).size,shots.length,'duplicate '+field);
 }
 for(const shot of shots){
  assert.ok(shot.character_scale_target_pct>=45,'cast too small: '+shot.id);
  assert.ok(shot.camera.length>10);
  assert.ok(shot.props.length>8);
  assert.equal(shot.needs_narration_alignment,true);
 }
});
test('Strict 4K/60 and no accidental publish or revoicing',()=>{
 assert.equal(manifest.quality_gates.native_width,2160);
 assert.equal(manifest.quality_gates.native_height,3840);
 assert.equal(manifest.quality_gates.fps,60);
 assert.equal(manifest.publication_approved,false);
 assert.match(manifest.narration,/Preservar voz original/);
 assert.equal(manifest.quality_gates.no_recycled_backplates,true);
 assert.equal(manifest.quality_gates.full_aac_voice_preserved,true);
});
