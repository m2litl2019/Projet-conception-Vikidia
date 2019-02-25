from texteval import *
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub

EMA = 'ema.bin'
print('== EMA ==')
print()
reperage_passive(EMA)
print()
reperage_pronoms(EMA)
print()
reperage_verbeconj_prorel_sub(EMA)
print()

MAUPA = 'maupassant12.bin'
print('== MAUPASSANT ==')
print()
reperage_passive(MAUPA)
print()
reperage_pronoms(MAUPA)
print()
reperage_verbeconj_prorel_sub(MAUPA)
print()

VIKIBEST = 'vikibest'
print('== VIKIBEST ==')
print()
reperage_passive(VIKIBEST)
print()
reperage_pronoms(VIKIBEST)
print()
reperage_verbeconj_prorel_sub(VIKIBEST)
print()
