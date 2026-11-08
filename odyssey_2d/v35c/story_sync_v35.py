"""Speech-aware editorial cut map for original Rasalgethi 220.56s master.
Every scene begins/ends at the previously measured pause; beat boundaries
match audible substantial pauses where present, supplemented by clause timing.
This is NOT professional word-level forced alignment, which requires ASR QC.
"""
import re,json
from pathlib import Path

CUTS={
 1:[2.5,5.68,7.6],
 2:[12.44,17.47,20.29],
 3:[26.2,29.4,31.8],
 4:[37.6,40.36,42.95,43.91,45.92,49.26,51.63],
 5:[58.36,60.4,62.87],
 6:[71.53,73.2,76.72],
 7:[84.48,87.85,90.21],
 8:[94.42,97.37,100.6],
 9:[108.66,111.06,113.5],
 10:[121.22,124.81,126.22],
 11:[131.2,134.39,136.9],
 12:[142.95,148.31,150.46],
 13:[160.1,162.02,164.2],
 14:[170.5,173.67,177.07],
 15:[189.98,196.23,198.71],
 16:[208.1,210.05,215.09]
}

SPOKEN={
 1:["Um velho mendigo ergueu um arco", "diante de dezenas de guerreiros.", "Ninguém imaginava", "quem ele realmente era."],
 2:["Era Odisseu, o estrategista", "que ajudara a destruir Troia com um gigantesco cavalo de madeira.", "Após dez anos de guerra,", "ele finalmente partiu para casa."],
 3:["Mas a viagem começou com tragédias. Na terra dos cícones,", "perdeu homens em combate.", "Entre os lotófagos,", "precisou resgatar companheiros que haviam esquecido o próprio lar."],
 4:["Em uma caverna, foram aprisionados", "por Polifemo, um gigante de um olho só.", "Odisseu o embriagou,", "disse chamar-se Ninguém", "e cegou o monstro.", "Seus homens escaparam escondidos sob ovelhas.", "Mas, ao revelar seu verdadeiro nome,", "Odisseu provocou a vingança de Poseidon."],
 5:["Éolo lhe entregou um saco contendo os ventos perigosos.", "Seus homens o abriram por engano,", "afastando a frota de Ítaca.", "Depois, gigantes lestrigões destruíram quase todos os navios."],
 6:["Na ilha de Circe, seus companheiros", "foram transformados em porcos.", "Protegido por Hermes, Odisseu resistiu à magia", "e conseguiu libertá-los. Mas, antes de continuar, recebeu uma ordem terrível."],
 7:["Ele precisou descer aos limites do mundo dos mortos.", "Ali, Tirésias revelou os perigos restantes.", "Odisseu também encontrou a própria mãe,", "mas não conseguiu abraçá-la."],
 8:["Depois vieram as sereias.", "Seu canto atraía navegantes para a morte.", "Odisseu pediu para ser amarrado ao mastro,", "enquanto seus homens remavam com os ouvidos protegidos."],
 9:["Em um estreito mortal, precisou escolher entre Caríbdis,", "um redemoinho gigantesco, e Cila, um monstro de seis cabeças.", "O navio escapou, mas seis marinheiros", "morreram."],
 10:["Famintos, seus homens desobedeceram à ordem", "de não tocar nos rebanhos sagrados do Sol.", "Zeus destruiu o último navio com um raio.", "Todos morreram, menos Odisseu."],
 11:["Ele chegou à ilha de Calipso,", "que o manteve ali por sete anos e lhe ofereceu a imortalidade.", "Mas Odisseu só desejava voltar", "para Penélope e Telêmaco."],
 12:["Depois de outra tempestade, foi acolhido pelos feácios.", "Ao conhecerem sua história,", "eles o levaram de navio até Ítaca.", "Vinte anos depois, ele estava em casa."],
 13:["Mas seu palácio estava ocupado por pretendentes que queriam se casar com Penélope e tomar o reino.", "Ela resistia.", "Seu filho Telêmaco, agora adulto,", "também procurava notícias do pai."],
 14:["Disfarçado de mendigo, Odisseu reencontrou Telêmaco", "e preparou a vingança.", "Seu velho cão Argos o reconheceu.", "Mais tarde, a ama Euricleia descobriu sua identidade pela cicatriz."],
 15:["Penélope anunciou uma prova: quem armasse o arco de Odisseu e atravessasse doze machados com uma flecha poderia desposá-la.", "Todos falharam. O mendigo conseguiu.", "Era o rei.", "Com Telêmaco, derrotou os pretendentes."],
 16:["Penélope ainda duvidou, até ele revelar o segredo da cama construída sobre uma oliveira viva.", "Ela o reconheceu.", "Odisseu reencontrou o pai, Laertes, e Atena encerrou a vingança.", "Depois de vinte anos, finalmente estava em casa. Tem uma explicação."]
}

def remap(shots,scene_times):
 assert len(shots)==68 and len(scene_times)==17
 new=[]
 for s in range(1,17):
  part=[x for x in shots if x['scene']==s]
  bds=[scene_times[s-1],*CUTS[s],scene_times[s]]
  assert len(bds)==len(part)+1,(s,bds,len(part))
  assert len(SPOKEN[s])==len(part),(s,len(part))
  for j,shot in enumerate(part):
   assert bds[j]<bds[j+1],(s,j)
   a={**shot,'start_seconds_estimate':round(bds[j],3),'end_seconds_estimate':round(bds[j+1],3),
      'timing_method':'scene_pauses_and_manual_spoken_clauses',
      'caption_exact_original':SPOKEN[s][j], 'force_word_aligned':False}
   if s==8 and j==0:a['narrative_action']='Sereias aparecem cantando sobre ilha rochosa'
   if s==8 and j==1:a['narrative_action']='Marinheiros tapam ouvidos e manobram o navio'
   if s==8 and j==2:a['narrative_action']='Odisseu é amarrado firmemente ao mastro'
   if s==13 and j==2:a['narrative_action']='Telêmaco prepara viagem em busca de notícias do pai'
   new.append(a)
 assert len(new)==68
 for a,b in zip(new,new[1:]):assert abs(a['end_seconds_estimate']-b['start_seconds_estimate'])<.001
 return new

def validate_transcript(lines):
 norm=lambda s:re.sub(r'[^\w\s]','',s,flags=re.UNICODE).lower().split()
 for s,line in enumerate(lines,1):
  canon=norm(line); divided=norm(' '.join(SPOKEN[s]))
  if canon!=divided:
   k=next((j for j,(a,b) in enumerate(zip(canon,divided)) if a!=b),min(len(canon),len(divided)))
   raise AssertionError((s,k,canon[k:k+9],divided[k:k+9],len(canon),len(divided)))
 return True

def write(new,path):
 Path(path).write_text(json.dumps({'shots':new,'method':'Original 220.56s Rasalgethi; scene pause verified, selected beat splits from audio silence + spoken clause mapping; NOT word-level forced alignment'},ensure_ascii=False,indent=2))