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

test('narration-backed scene order matches inspected original episode storyboards',()=>{
 const expected:[number,string][]=[
  [2,'DEPOIS DE TROIA'],[22,'A PRIMEIRA PERDA'],[32,'O FRUTO DO ESQUECIMENTO'],
  [45,'A CAVERNA DE POLIFEMO'],[62,'O HOMEM CHAMADO NINGUÉM'],
  [80,'O PREÇO DE UM NOME'],[99,'OS VENTOS DE ÉOLO'],
  [120,'O PORTO SEM SAÍDA'],[135,'O FEITIÇO DE CIRCE'],
  [160,'NA TERRA DOS MORTOS'],[180,'O CANTO DAS SEREIAS'],
  [193,'ENTRE CILA E CARÍBDIS'],[212,'O REBANHO DO SOL'],
  [230,'SETE ANOS COM CALIPSO'],[249,'O TEAR DE PENÉLOPE'],
  [266,'À PROCURA DO PAI'],[286,'UMA JANGADA NO MAR'],
  [305,'ENTRE OS FEÁCIOS'],[327,'A PRAIA DE ÍTACA'],
  [348,'PAI E FILHO'],[366,'ARGOS'],[384,'A CICATRIZ'],
  [406,'O ARCO DE ODISSEU'],[424,'DOZE MACHADOS'],
  [445,'PENÉLOPE DESCE AO SALÃO'],[465,'O SEGREDO DA OLIVEIRA'],
  [482,'A LEMBRANÇA DE TROIA'],[486,'O REENCONTRO'],[505,'UM REMO EM TERRA FIRME'],
  [521,'O POMAR DE LAERTES'],[545,'A PAZ EM ÍTACA']
 ];
 for(const [second,chapter] of expected)
  assert.equal(getOdysseyBeat(second).chapter,chapter,'Original-film mismatch at '+second+'s');
 assert.equal(new Set(ODYSSEY_BEATS.map(x=>x.action)).size,ODYSSEY_BEATS.length);
 assert.ok(ODYSSEY_BEATS.length>=110);
});

test('Trojan-horse recollection plays exactly under the 08:00–08:05 spoken flashback',()=>{
 const before=getOdysseyBeat(479.983333);
 const horse=getOdysseyBeat(480);
 const endHorse=getOdysseyBeat(484.983333);
 const after=getOdysseyBeat(485);
 assert.equal(before.chapter,'O SEGREDO DA OLIVEIRA');
 assert.equal(horse.action,'horseMemory');
 assert.equal(endHorse.action,'horseMemory');
 assert.equal(horse.location,'troia');
 assert.equal(horse.start,480);
 assert.equal(horse.end,485);
 assert.equal(after.chapter,'O REENCONTRO');
 assert.notEqual(after.action,'horseMemory');
});
