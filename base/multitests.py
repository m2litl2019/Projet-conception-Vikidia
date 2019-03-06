from texteval import *
from presentation import Presentation
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
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


LITENF = 'litEnfant.tal'
res_litenf = {
    'GEN_TITLE' : 'LitEnfant',
    'GEN_URL' : 'https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/corpuslitenf',
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


p = Presentation('templates/maquette2.html')
p.populate(res_ema, 0)
p.populate(res_maupa, 1)
p.populate(res_vikibest, 2)
p.populate(res_litenf,3)
p.ouput_all('results/multitests')

