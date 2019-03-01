from texteval import *
from presentation import Presentation
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub

EMA = 'ema.tal'
res_ema = {}
print('== EMA ==')
print()
res_ema.update(reperage_passive(EMA))
print()
res_ema.update(reperage_pronoms(EMA))
print()
res_ema.update(reperage_verbeconj_prorel_sub(EMA))
print()

MAUPA = 'maupassant12.bin'
res_maupa = {}
print('== MAUPASSANT ==')
print()
res_maupa.update(reperage_passive(MAUPA))
print()
res_maupa.update(reperage_pronoms(MAUPA))
print()
res_maupa.update(reperage_verbeconj_prorel_sub(MAUPA))
print()

VIKIBEST = 'vikibest'
res_vikibest = {}
print('== VIKIBEST ==')
print()
res_vikibest.update(reperage_passive(VIKIBEST))
print()
res_vikibest.update(reperage_pronoms(VIKIBEST))
print()
res_vikibest.update(reperage_verbeconj_prorel_sub(VIKIBEST))
print()

p = Presentation('templates/maquette2.html')
p.populate(res_ema, 0)
p.populate(res_maupa, 1)
p.populate(res_vikibest, 2)
p.ouput_all('results/multitests')

