/** Locked edit map for the recovered 560.10s Portuguese narration.
 * Each beat is a separate physical action, not a reused loop or stock still.
 * Boundaries are source-video timecodes; sub-beats are provisional until speech QC.
 */
export type OdysseyBeat = {id:string;start:number;end:number;chapter:string;location:string;action:string;characters:string[]};
type Section={start:number;end:number;title:string;place:string;beats:readonly string[]};
const sections:Section[]=[
 {start:0,end:27,title:'O FIM DE TROIA',place:'troia',beats:['burningTroia','fleetDeparture','rowingHome','ithacaWaiting','weavingNight']},
 {start:27,end:39,title:'A TERRA DO LÓTUS',place:'lotus',beats:['lotusLanding','lotusOffering','lotusEnchantment','lotusRescue']},
 {start:39,end:76,title:'O CICLOPE POLIFEMO',place:'cave',beats:['caveDiscovery','cyclopsArrival','boulderSeals','prisonersWatch','wineToGiant','cyclopsSleeping','stakePrepared','ramEscape','cyclopsPlea','nameRevealed']},
 {start:76,end:89,title:'A MALDIÇÃO DO MAR',place:'seaStorm',beats:['poseidonRises','darkStorm','shipBraces']},
 {start:89,end:108,title:'O PRESENTE DE ÉOLO',place:'wind',beats:['aeolusGift','homeOnHorizon','bagUnknotted','windsReleased']},
 {start:108,end:122,title:'OS LESTRIGÕES',place:'harbor',beats:['fleetTrapped','giantsAttack','boatsDestroyed','lastShipEscapes']},
 {start:122,end:148,title:'CIRCE E OS ENCANTAMENTOS',place:'circe',beats:['circeWelcomes','enchantedCup','menTransform','hermesHerb','circeDefied','crewRestored']},
 {start:148,end:170,title:'O REINO DOS MORTOS',place:'hades',beats:['underworldGate','seerWarns','motherAppears','handsPassGhost']},
 {start:170,end:184,title:'O CANTO DAS SEREIAS',place:'sirens',beats:['waxInEars','tiedToMast','wingedSirens','rowingPastVoices']},
 {start:184,end:201,title:'CILA E CARÍBDIS',place:'strait',beats:['straitRevealed','whirlpoolTurns','scyllaStrikes','shipNarrowEscape']},
 {start:201,end:221,title:'O GADO DO SOL',place:'cattle',beats:['sacredHerd','crewHunger','forbiddenFeast','thunderBreaksShip','aloneAdrift']},
 {start:221,end:255,title:'OS ANOS COM CALIPSO',place:'calypso',beats:['calypsoShelter','odysseusWaits','hermesDecree','raftCarpentry','raftLaunch','raftStorm','shoreRescue']},
 {start:255,end:286,title:'OS FEÁCIOS',place:'phaeacia',beats:['nausicaaFinds','palaceWelcome','lyreLament','pastRetold','giftsAboard','sleepingReturn']},
 {start:286,end:317.4,title:'TELÊMACO',place:'journey',beats:['telemachusSeeks','athenaGuides','dangerousReturn','ithacaDiscovered','sonApproaches']},
 {start:317.4,end:358,title:'O REGRESSO A ÍTACA',place:'ithaca',beats:['shoreWake','athenaDisguise','shepherdHut','fatherSonMeet','fatherSonPlan','nightPalaceEntry']},
 {start:358,end:375,title:'ARGOS',place:'argos',beats:['argosHears','argosLooks','argosRises','argosGreeting']},
 {start:375,end:396,title:'A CICATRIZ',place:'wash',beats:['oldNurseWashes','scarDiscovered','nurseRecognizes','silenceAgreed']},
 {start:396,end:433,title:'O DESAFIO DO ARCO',place:'bow',beats:['suitorsFeast','bowAttempt','odysseusTakesBow','bowBends','arrowTargets','suitorsRecoil','hallSecured']},
 {start:433,end:455,title:'PENÉLOPE',place:'penelope',beats:['penelopeApproaches','facesUncertain','memoriesReturn','recognitionDawns']},
 {start:455,end:495,title:'A CAMA DE OLIVEIRA',place:'bed',beats:['bedSecret','oliveTreeReveal','proofOfHome','handsReach','reunionEmbrace','quietNight']},
 {start:495,end:560.1,title:'O LAR RECONQUISTADO',place:'finale',beats:['morningReckoning','fatherSonTogether','palaceRestored','familyAtOlive','shoreSunrise','seaAtPeace','islandPanorama','finalSilhouette']}
];
export const ODYSSEY_TOTAL_SECONDS=560.1;
export const ODYSSEY_EPISODES=[
 {number:1,name:'A maldição de Poseidon',start:0,end:88.6},
 {number:2,name:'Monstros e deuses',start:88.6,end:317.4},
 {number:3,name:'O retorno a Ítaca',start:317.4,end:560.1},
] as const;
export const ODYSSEY_BEATS:OdysseyBeat[]=sections.flatMap(s=>
 s.beats.map((action,i)=>{
   const start=s.start+(s.end-s.start)*i/s.beats.length;
   const end=s.start+(s.end-s.start)*(i+1)/s.beats.length;
   return {id:`s${sections.indexOf(s)+1}-${i+1}`,start,end,chapter:s.title,location:s.place,action,
      characters: action.includes('cyclops')||action.includes('boulder')?['Odisseu','Polifemo']: action.includes('penelope')||action.includes('bed')?['Odisseu','Penélope']:['Odisseu']};
 }));
export const getOdysseyBeat=(seconds:number):OdysseyBeat=>{
 const s=Math.min(ODYSSEY_TOTAL_SECONDS-.0001,Math.max(0,seconds));
 return ODYSSEY_BEATS.find(b=>s>=b.start&&s<b.end)??ODYSSEY_BEATS[ODYSSEY_BEATS.length-1]!;
};
export const odysseyFrameCount=(from:number,to:number,fps=60)=>Math.round((to-from)*fps);
export const verifyOdysseyTimeline=()=>{
 if(ODYSSEY_BEATS[0]?.start!==0)return false;
 for(let i=1;i<ODYSSEY_BEATS.length;i++)if(Math.abs(ODYSSEY_BEATS[i-1]!.end-ODYSSEY_BEATS[i]!.start)>1e-5)return false;
 return Math.abs(ODYSSEY_BEATS[ODYSSEY_BEATS.length-1]!.end-ODYSSEY_TOTAL_SECONDS)<1e-6;
};
