// Original, deterministic 60-second cinematic soundtrack, synthesized offline.
// No third-party tracks or paid audio API. Does not pretend to be narration.
import fs from 'node:fs';
import path from 'node:path';
const rate=22050,duration=60,size=rate*duration;
const buf=Buffer.allocUnsafe(44+size*2);
buf.write('RIFF',0);buf.writeUInt32LE(buf.length-8,4);buf.write('WAVE',8);
buf.write('fmt ',12);buf.writeUInt32LE(16,16);buf.writeUInt16LE(1,20);
buf.writeUInt16LE(1,22);buf.writeUInt32LE(rate,24);buf.writeUInt32LE(rate*2,28);
buf.writeUInt16LE(2,32);buf.writeUInt16LE(16,34);
buf.write('data',36);buf.writeUInt32LE(size*2,40);
const notes=[110,146.83,164.81,130.81,110,98,123.47,110,146.83,110];
const TAU=2*Math.PI;
let seed=14823;
const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296-.5;};
for(let i=0;i<size;i++){
 const t=i/rate,section=Math.min(9,Math.floor(t/6)),n=notes[section],shot=t%6;
 const fade=Math.max(0,Math.min(1,t/1.5,(60-t)/2));
 const pad=(Math.sin(TAU*n*t)+.33*Math.sin(TAU*(n/2)*t)+.23*Math.sin(TAU*(n*1.5)*t))*.077;
 const chord=.028*Math.sin(TAU*(n*1.2)*t)+.018*Math.sin(TAU*(n*1.5)*t);
 const punch=t%1.5,drum=Math.exp(-punch*21)*(.16*Math.sin(TAU*50*t)+rnd()*.065);
 const accent=Math.exp(-shot*13)*(.13*Math.sin(TAU*75*t)+rnd()*.095);
 const pluck=t%3,lyre=.086*Math.sin(TAU*(n*2)*t)*Math.exp(-pluck*3.0);
 const air=.009*rnd();
 const amp=(pad+chord+drum+accent+lyre+air)*fade;
 buf.writeInt16LE(Math.round(Math.max(-.9,Math.min(.9,amp))*32767),44+i*2);
}
const dest=path.join(process.cwd(),'public','audio','odisseu-original-score.wav');
fs.mkdirSync(path.dirname(dest),{recursive:true});
fs.writeFileSync(dest,buf);
console.log('Generated',dest,'duration',duration,'bytes',buf.length);
