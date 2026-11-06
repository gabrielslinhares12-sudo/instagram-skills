import {test} from 'node:test';
import assert from 'node:assert/strict';
import {TROIA_CUES} from '../src/TroiaFilm';

test('Odisseu e Troia: 10 sequências de seis segundos, duração final 60s',()=>{
 assert.equal(TROIA_CUES.length,10);
 assert.equal(TROIA_CUES.length*6*60,3600);
 assert.equal(TROIA_CUES[9].text.endsWith('Tem uma explicação.'),true);
});
test('a história distingue mito de fato e usa um protagonista histórico-mitológico',()=>{
 assert.match(TROIA_CUES[2].text,/Segundo a mitologia/);
 assert.match(TROIA_CUES[1].text,/Odisseu/);
});
test('todas cenas têm título curto e texto narrável',()=>{
 assert.equal(TROIA_CUES.every(x=>x.title.length<=32&&x.text.length>=55),true);
});
