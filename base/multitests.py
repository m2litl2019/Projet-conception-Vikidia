#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------

# Base
import datetime

# Project global
from texteval import *
from presentation import Presentation

# Project indices
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
from reperage_tpsV import reperage_tps
from indices_html import reperage_images_liens_viki, reperage_ponctuation
from reperage_def_con import reperage_connecteurs_flesch, reperage_definition
from lexique import extract_lemmas, compare_Manulex, compute_polysemy_index

#-----------------------------------------------------------
# Function
#-----------------------------------------------------------

def raw_indices(part):
    # Raw indices
    avg = 0
    nb_ponct = 0
    nb_pt_virg = 0
    nb_dbl_pt = 0
    nb_virg = 0
    nb_all_words = 0
    nb_words = 0
    for s in part:
        avg += len(s)
        for w in s:
            nb_all_words += 1
            if w.pos == 'PONCT':
                nb_ponct += 1
                if w.form == ';':
                    nb_pt_virg += 1
                elif w.form == ':':
                    nb_dbl_pt += 1
                elif w.form == ',':
                    nb_virg += 1
            else:
                nb_words += 1
    avg //= len(part)
    return {'SUR_NB_WORDS' : nb_words,
            'SUR_NB_ALL_WORDS' : nb_all_words,
            'SUR_WORD_LEN_AVG' : avg,
            'SUR_PONCTUATION' : nb_ponct,
            'SUR_AVG_PONCTUATION' : nb_ponct / nb_all_words,
            'SUR_PONCT_PT_VIRG' : nb_pt_virg,
            'SUR_AVG_PONCT_PT_VIRG' : nb_pt_virg / nb_all_words,
            'SUR_PONCT_DBL_PT' : nb_dbl_pt,
            'SUR_AVG_PONCT_DBL_PT' : nb_dbl_pt / nb_all_words,
            'SUR_PONCT_VIRG' : nb_virg,
            'SUR_AVG_PONCT_VIRG' : nb_virg / nb_all_words,
        }

def indices(title, path, url, debug=False):
    res = {
        'GEN_TITLE' : title,
        'GEN_URL' : url,
        'GEN_DATE' : str(datetime.datetime.now())
    }
    data = load(path)
    lemmas = extract_lemmas(data)
    print('==', title, '==')
    res.update(raw_indices(data))
    if debug: print()
    res.update(reperage_passive(data, debug=debug))
    if debug: print()
    res.update(reperage_pronoms(data, debug=debug))
    if debug: print()
    res.update(reperage_verbeconj_prorel_sub(data, debug=debug))
    if debug: print()
    res.update(reperage_tps(data, debug=debug))
    if debug: print()
    res.update(reperage_connecteurs_flesch(data, debug=debug))
    if debug: print()
    res.update(reperage_definition(data, debug=debug))
    if debug: print()
    res.update(compare_Manulex(lemmas, debug=debug))
    if debug: print()
    res.update(compute_polysemy_index(lemmas, debug=debug))
    if isinstance(res['SEMLEX_POLY_INDEX'], str):
        res.update({
            'SEMLEX_AVG_MANULEX' : res['SEMLEX_MANULEX'] / res['SUR_NB_WORDS'],
            'SEMLEX_AVG_POLY' : res['SEMLEX_POLY_INDEX']
            })
    else:
        res.update({
            'SEMLEX_AVG_MANULEX' : res['SEMLEX_MANULEX'] / res['SUR_NB_WORDS'],
            'SEMLEX_AVG_POLY' : res['SEMLEX_POLY_INDEX'] / res['SUR_NB_WORDS']
            })
    if debug: print()
    return res

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

# Calculating indices
#---------------------

all_res = {}

all_res['Littérature Enfant'] = indices(title='Littérature Enfant',
                                       path='litEnfant.zip',
                                       url='https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/litEnfant.tal')

all_res['EMA'] = indices(title='EMA',
        path='ema.tal',
        url='https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/ema.tal')

#all_res['Vikidia'] = indices(title='Vikidia',
#              path='Vikidia-TAL',
#              url='')

#all_res['Wikipedia'] = indices(title='Wikipedia',
#              path='Wikipedia-tal',
#              url='')

#all_res['ortho-tal'] = indices(title='Ortho corpus',
#                               path='ortho-tal',
#                               url='')

all_res['Maupassant'] = indices(title='Maupassant',
                                path='maupassant12.bin',
                                url='https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/maupassant12.bin')

all_res['Vikibest'] = indices(title='Vikibest',
                              path='vikibest',
                              url='https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/vikibest')

all_res['Vikidia "à simplifier"'] = indices(title='Vikidia "à simplifier"',
                                            path='VikiSimply-tal',
                                            url='https://github.com/m2litl2019/Projet-conception-Vikidia/blob/master/base/VikiSimply-tal')

#all_res['Monde Diplomatique'] = indices(title='Monde Diplomatique',
#                                        path='md_fr.bin',
#                                        url='https://github.com/m2litl2019/Projet-conception-Vikidia/tree/master/base/md_fr.tal')

# Output
#--------

p = Presentation('templates/maquette2.html')
nb = 0
for k, res in all_res.items():
    p.populate(res, nb, name=res['GEN_TITLE'])
    nb += 1
p.ouput_all('results/multitests')
