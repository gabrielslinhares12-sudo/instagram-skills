import React from 'react';
import {LuminoPuppet,type ActorGesture} from './LuminoPuppet';
import {requireRig,type Pose} from './rigs';

// Every cast member in the production timeline must render as an acting puppet,
// with character-specific joints and facial animation. No static PNG fallback.
export const CharacterActor:React.FC<{
  id:string;pose:Pose;time:number;light?:number;
}>=({id,pose,time,light=1})=>{
 requireRig(id); // strict allowlist: unknown characters block the render
 switch(id){
  case 'lumino':
   return <LuminoPuppet width="100%" height="auto" gesture={pose as ActorGesture} time={time}
    darkness={Math.max(0,Math.min(1,1-light))}/>;
  default:
   throw new Error('Personagem sem modelo animado: '+id);
 }
};
