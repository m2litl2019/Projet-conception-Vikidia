from texteval import *
from presentation import Presentation
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
from reperage_tpsV import reperage_tps
from reperage_def_con import reperage_connecteurs_flesch
from reperage_def_con import reperage_definition
import datetime

EMA = 'ema.tal'
res_ema = {
    'GEN_TITLE' : 'EMA',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/ema.tal',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== EMA ==')
print()
res_ema.update(reperage_passive(EMA))
print()
res_ema.update(reperage_pronoms(EMA))
print()
res_ema.update(reperage_verbeconj_prorel_sub(EMA))
print()
res_ema.update(reperage_tps(EMA))
print()
res_ema.update(reperage_connecteurs(EMA))
print()
res_ema.update(reperage_definition(EMA))
print()
res_ema.update(compare_Manulex(lemmas))
print()
res_ema.update(compute_polysemy_index(lemmas))
print()

Wikipedia = 'Wikipedia-tal'
res_Wikipedia = {
    'GEN_TITLE' : 'Wikipedia',
    'GEN_URL' : '',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== Wikipedia ==')
print()
res_Wikipedia.update(reperage_passive(Wikipedia))
print()
res_Wikipedia.update(reperage_pronoms(Wikipedia))
print()
res_Wikipedia.update(reperage_verbeconj_prorel_sub(Wikipedia))
print()
res_Wikipedia.update(reperage_tps(Wikipedia))
print()
res_Wikipedia.update(reperage_connecteurs(Wikipedia))
print()
res_Wikipedia.update(reperage_definition(Wikipedia))
print()
  
ORTHO = 'ortho-tal'
res_ORTHO = {
    'GEN_TITLE' : 'ORTHO',
    'GEN_URL' : '',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== ORTHO ==')
print()
res_ORTHO.update(reperage_passive(ORTHO))
print()
res_ORTHO.update(reperage_pronoms(ORTHO))
print()
res_ORTHO.update(reperage_verbeconj_prorel_sub(ORTHO))
print()
res_ORTHO.update(reperage_tps(ORTHO))
print()
res_ORTHO.update(reperage_connecteurs(ORTHO))
print()
res_ORTHO.update(reperage_definition(ORTHO))
print()
print()
res_ORTHO.update(compare_Manulex(lemmas))
print()
res_ORTHO.update(compute_polysemy_index(lemmas))
print()

MAUPA = 'maupassant12.bin'
res_maupa = {
    'GEN_TITLE' : 'MAUPASSANT',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/maupassant12.bin',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== MAUPASSANT ==')
print()
res_maupa.update(reperage_passive(MAUPA))
print()
res_maupa.update(reperage_pronoms(MAUPA))
print()
res_maupa.update(reperage_verbeconj_prorel_sub(MAUPA))
print()
res_maupa.update(reperage_tps(MAUPA))
print()
res_maupa.update(reperage_connecteurs(MAUPA))
print()
res_maupa.update(reperage_definition(MAUPA))
print()
res_maupa.update(compare_Manulex(lemmas))
print()
res_maupa.update(compute_polysemy_index(lemmas))
print()
VIKIBEST = 'vikibest'
res_vikibest = {
    'GEN_TITLE' : 'VIKIBEST',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/vikibest',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== VIKIBEST ==')
print()
res_vikibest.update(reperage_passive(VIKIBEST))
print()
res_vikibest.update(reperage_pronoms(VIKIBEST))
res_vikibest.update(reperage_pronoms(VIKIBEST))
print()
res_vikibest.update(reperage_verbeconj_prorel_sub(VIKIBEST))
print()
res_vikibest.update(reperage_tps(VIKIBEST))
print()

res_vikibest.update(reperage_connecteurs(VIKIBEST))
print()
res_vikibest.update(reperage_definition(VIKIBEST))
print()

VIKIRANDOM = 'VikiRandom-tal'
res_vikirandom = {
    'GEN_TITLE' : 'VIKIRANDOM',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/VikiRandom-tal',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== Des articles au hasard de Vikidia ==')
print()
res_vikirandom.update(reperage_passive(VIKIRANDOM))
print()
res_vikirandom.update(reperage_pronoms(VIKIRANDOM))
res_vikirandom.update(reperage_pronoms(VIKIRANDOM))
print()
res_vikirandom.update(reperage_verbeconj_prorel_sub(VIKIRANDOM))
print()
res_vikirandom.update(reperage_tps(VIKIRANDOM))
print()
res_vikirandom.update(reperage_connecteurs(VIKIRANDOM))
print()
res_vikirandom.update(reperage_definition(VIKIRANDOM))
print()

vikisimply= 'VikiSimply-tal'
res_vikisimply = {
    'GEN_TITLE' : 'VikiSimply',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/VikiSimply-tal',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== VIKIDIA "à simplifier" ==')
print()
res_vikisimply.update(reperage_passive(vikisimply))
print()
res_vikisimply.update(reperage_pronoms(vikisimply))
print()
res_vikisimply.update(reperage_verbeconj_prorel_sub(vikisimply))
print()
res_vikisimply.update(reperage_tps(vikisimply))
print()
res_vikisimply.update(reperage_connecteurs(vikisimply))
print()
res_vikisimply.update(reperage_definition(vikisimply))
print()

LITENF = 'litEnfant.bin'
res_litenf = {
    'GEN_TITLE' : 'LitEnfant',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/litEnfant.tal',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== Corpus littéraire 6eme / 5eme ==')
print()
res_litenf.update(reperage_passive(LITENF))
print()
res_litenf.update(reperage_pronoms(LITENF))
res_litenf.update(reperage_pronoms(LITENF))
print()
res_litenf.update(reperage_verbeconj_prorel_sub(LITENF))
print()
res_litenf.update(reperage_tps(LITENF))
print()

res_litenf.update(reperage_connecteurs(LITENF))
print()
res_litenf.update(reperage_definition(LITENF))
print()

MONDEDIPLO = 'md_fr.bin'
res_md = {
    'GEN_TITLE' : 'Monde diplomatique',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/md_fr.tal',
    'GEN_DATE' : str(datetime.datetime.now())
}
print('== Corpus du Monde Diplomatique ==')
print()
res_md.update(reperage_passive(MONDEDIPLO))
print()
res_md.update(reperage_pronoms(MONDEDIPLO))
res_md.update(reperage_pronoms(MONDEDIPLO))
print()
res_md.update(reperage_verbeconj_prorel_sub(MONDEDIPLO))
print()
res_md.update(reperage_tps(MONDEDIPLO))
print()
print()
res_md.update(reperage_connecteurs(MONDEDIPLO))
print()
res_md.update(reperage_definition(MONDEDIPLO))
res_md.update(compare_Manulex(lemmas))
print()
res_md.update(compute_polysemy_index(lemmas))
print()

p = Presentation('templates/maquette2.html')
p.populate(res_litenf, 0, name='Litérature Enfant')
p.populate(res_ema, 1, name='EMA')
p.populate(res_maupa, 2, name='Maupassant')
p.populate(res_vikibest, 3, name='Vikibest')
p.populate(res_md, 4, name='Monde Diplomatique')
p.populate(res_vikirandom, 5, name='Vikidia (random)')
p.populate(res_vikisimply, 6, name='Vikidia "à simplifier"')
p.populate(res_ORTHO, 7, name='Ortho corpus')
p.populate(res_Wikipedia, 8, name='Wikipédia')
p.ouput_all('results/multitests')
