/** Original-master-verified Odyssey timing map (560.1s), visually audited each 10s.
 * Scene titles and chronology correspond to the real 2026 original with its burnt PT captions.
 * New rigs must animate the action at the same spoken moment, never generic B-roll.
 */
export type OdysseyBeat={id:string;start:number;end:number;chapter:string;location:string;action:string;characters:string[]};
type Section={start:number;end:number;title:string;place:string;beats:readonly string[]};
export const ODYSSEY_TOTAL_SECONDS=560.1;
const sections:Section[]=[
{"start":0,"end":17,"title":"DEPOIS DE TROIA","place":"troia","beats":["burningTroia","fleetDeparture","rowingHome","ithacaWaiting","penelopeWaits"]},
{"start":17,"end":28,"title":"A PRIMEIRA PERDA","place":"troia","beats":["ciconesClash","ciconesReinforcements","menRetreat"]},
{"start":28,"end":38,"title":"O FRUTO DO ESQUECIMENTO","place":"lotus","beats":["lotusLanding","lotusOffering","lotusEnchantment","lotusRescue"]},
{"start":38,"end":55,"title":"A CAVERNA DE POLIFEMO","place":"cave","beats":["caveDiscovery","cyclopsArrival","boulderSeals","prisonersWatch"]},
{"start":55,"end":76,"title":"O HOMEM CHAMADO NINGUÉM","place":"cave","beats":["wineToGiant","cyclopsSleeping","stakePrepared","cyclopsPlea","ramEscape"]},
{"start":76,"end":88.6,"title":"O PREÇO DE UM NOME","place":"seaStorm","beats":["nameRevealed","poseidonPlea","darkStorm"]},
{"start":88.6,"end":113,"title":"OS VENTOS DE ÉOLO","place":"wind","beats":["aeolusGift","homeOnHorizon","bagUnknotted","windsReleased"]},
{"start":113,"end":127,"title":"O PORTO SEM SAÍDA","place":"harbor","beats":["fleetTrapped","giantsAttack","boatsDestroyed","lastShipEscapes"]},
{"start":127,"end":148,"title":"O FEITIÇO DE CIRCE","place":"circe","beats":["circeWelcomes","enchantedCup","menTransform","hermesHerb","circeDefied","crewRestored"]},
{"start":148,"end":175,"title":"NA TERRA DOS MORTOS","place":"hades","beats":["underworldGate","seerWarns","motherAppears","handsPassGhost","companionGhost"]},
{"start":175,"end":188,"title":"O CANTO DAS SEREIAS","place":"sirens","beats":["waxInEars","tiedToMast","wingedSirens","rowingPastVoices"]},
{"start":188,"end":205,"title":"ENTRE CILA E CARÍBDIS","place":"strait","beats":["straitRevealed","whirlpoolTurns","scyllaStrikes","shipNarrowEscape"]},
{"start":205,"end":224,"title":"O REBANHO DO SOL","place":"cattle","beats":["sacredHerd","crewHunger","forbiddenFeast","thunderBreaksShip","aloneAdrift"]},
{"start":224,"end":239,"title":"SETE ANOS COM CALIPSO","place":"calypso","beats":["calypsoShelter","odysseusWaits","calypsoYearn"]},
{"start":239,"end":258,"title":"O TEAR DE PENÉLOPE","place":"penelope","beats":["suitorsFeast","penelopeLoom","weavingNight","loomUnravels","penelopeRefuses"]},
{"start":258,"end":276,"title":"À PROCURA DO PAI","place":"journey","beats":["telemachusSeeks","athenaGuides","nestorMeeting","dangerousReturn","ambushEscape"]},
{"start":276,"end":295,"title":"UMA JANGADA NO MAR","place":"calypso","beats":["hermesDecree","raftCarpentry","raftLaunch","raftStorm","shoreRescue"]},
{"start":295,"end":316.167,"title":"ENTRE OS FEÁCIOS","place":"phaeacia","beats":["nausicaaFinds","palaceWelcome","lyreLament","pastRetold","giftsAboard","sleepingReturn"]},
{"start":316.167,"end":338,"title":"A PRAIA DE ÍTACA","place":"ithaca","beats":["shoreWake","ithacaDiscovered","shoreKneel","athenaDisguise"]},
{"start":338,"end":358,"title":"PAI E FILHO","place":"ithaca","beats":["shepherdHut","fatherSonMeet","fatherSonPlan","sonEmbrace"]},
{"start":358,"end":374,"title":"ARGOS","place":"argos","beats":["argosHears","argosLooks","argosRises","argosGreeting"]},
{"start":374,"end":396,"title":"A CICATRIZ","place":"wash","beats":["nightPalaceEntry","suitorStoolThrown","oldNurseWashes","scarDiscovered","nurseRecognizes","silenceAgreed"]},
{"start":396,"end":416,"title":"O ARCO DE ODISSEU","place":"bow","beats":["bowAttempt","odysseusTakesBow","bowBends","arrowTargets"]},
{"start":416,"end":435,"title":"DOZE MACHADOS","place":"bow","beats":["axeChallenge","arrowThroughAxes","suitorsRecoil","hallSecured"]},
{"start":435,"end":455,"title":"PENÉLOPE DESCE AO SALÃO","place":"penelope","beats":["penelopeApproaches","facesUncertain","nurseAnnounces","recognitionDawns"]},
{"start":455,"end":480,"title":"O SEGREDO DA OLIVEIRA","place":"bed","beats":["bedSecret","oliveTreeReveal","proofOfHome","memoriesReturn","horseMemory"]},
{"start":480,"end":495,"title":"O REENCONTRO","place":"penelope","beats":["handsReach","reunionEmbrace","quietNight","familyReunited"]},
{"start":495,"end":515,"title":"UM REMO EM TERRA FIRME","place":"journey","beats":["oarInland","oarTraveler","oarBuried"]},
{"start":515,"end":528,"title":"O POMAR DE LAERTES","place":"finale","beats":["oliveOrchard","laertesRecognition","ancestralTrees"]},
{"start":528,"end":560.1,"title":"A PAZ EM ÍTACA","place":"finale","beats":["morningReckoning","athenaCeasefire","peaceAssembly","familyAtOlive","seaAtPeace","finalSilhouette"]}
];
export const ODYSSEY_EPISODES=[
 {number:1,name:'A maldição de Poseidon',start:0,end:88.6},
 {number:2,name:'Monstros e deuses',start:88.6,end:317.4},
 {number:3,name:'O retorno a Ítaca',start:317.4,end:560.1},
] as const;
export const ODYSSEY_BEATS:OdysseyBeat[]=sections.flatMap((s,chapterIndex)=>
 s.beats.map((action,i)=>{
  const start=s.start+(s.end-s.start)*i/s.beats.length;
  const end=s.start+(s.end-s.start)*(i+1)/s.beats.length;
  const characters=action.toLowerCase().includes('cyclops')||action.toLowerCase().includes('boulder')
   ?['Odisseu','Polifemo']:(action.toLowerCase().includes('penelope')||action.toLowerCase().includes('bed'))
   ?['Odisseu','Penélope']:action.toLowerCase().includes('telemachus')?['Telêmaco']:['Odisseu'];
  return {id:`s${chapterIndex+1}-${i+1}`,start,end,chapter:s.title,location:s.place,action,characters};
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
