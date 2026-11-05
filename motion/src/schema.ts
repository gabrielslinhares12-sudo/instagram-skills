import {z} from 'zod';
const asset = z.string().regex(/^[a-zA-Z0-9][a-zA-Z0-9_./-]*$/).refine(p => !p.split('/').includes('..'), 'Asset deve estar em public/');
const cue = z.object({start:z.number().nonnegative(), end:z.number().positive(), text:z.string().min(1).max(72)}).strict();
export const episodeSchema = z.object({
  title:z.string().min(1).max(60),
  narration:asset.nullable().default(null),
  scenes:z.array(z.object({
    id:z.string().min(1), duration:z.number().min(1).max(90),
    environment:z.enum(['laboratory','city','observatory','lighthouse','pier','cottage','underfloor','lantern']),
    heading:z.string().max(40).default(''),
    beat:z.enum(['flash','arrival','sign','tea','noise','hatch','blackout','voice']).optional(),
    headingSeconds:z.number().min(0).max(3).default(0),
    actor:z.enum(['enter','float','discover']).default('float'),
    side:z.enum(['left','right']).default('right'),
    camera:z.enum(['push','pan','static']).default('push'),
    background:z.object({kind:z.enum(['image','video']),src:asset,credit:z.string().min(1)}).strict().optional(),
    captions:z.array(cue).default([]),
    sounds:z.array(z.object({src:asset,start:z.number().nonnegative(),duration:z.number().positive(),volume:z.number().min(0).max(1)}).strict()).default([])
  }).strict()).min(1).max(30)
}).strict().superRefine((episode,ctx)=>{
  const ids=new Set<string>();
  episode.scenes.forEach((s,i)=>{
    const error=(message:string)=>ctx.addIssue({code:'custom',path:['scenes',i],message});
    if(ids.has(s.id)) error('ID de cena duplicado'); ids.add(s.id);
    if(s.headingSeconds>s.duration) error('Título fora da cena');
    let end=0;
    for(const c of s.captions){
      if(c.start<end||c.end<=c.start||c.end>s.duration) error('Legendas sobrepostas, fora de ordem ou fora da cena');
      if(c.start<s.headingSeconds) error('Título e legenda não podem disputar a tela');
      end=c.end;
    }
    for(const sound of s.sounds) if(sound.start+sound.duration>s.duration) error('Som ultrapassa cena');
  });
});
export type Episode=z.infer<typeof episodeSchema>;
export type Scene=Episode['scenes'][number];
export const FPS=60;
export const frames=(seconds:number)=>Math.round(seconds*FPS);
export const totalFrames=(episode:Episode)=>episode.scenes.reduce((n,s)=>n+frames(s.duration),0);
