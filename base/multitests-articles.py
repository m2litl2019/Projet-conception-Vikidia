from texteval import *
from presentation import Presentation
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
from reperage_tpsV import reperage_tps
from indices_html import reperage_images_liens_viki, reperage_ponctuation
from reperage_def_con import reperage_connecteurs_flesch, reperage_definition
from lexique import extract_lemmas, compare_Manulex, compute_polysemy_index
import datetime


p = Presentation('templates/maquette2.html')


VIKIBEST = 'vikibest'
#print('== VIKIBEST par articles ==')
#data = load(VIKIBEST,automerge = False)

#for i in range(0,len(data)):
    #article = data[i]
    #res = {
    #'GEN_TITLE' : article.tag[:-4],
    #'GEN_URL' : '',
    #'GEN_DATE' : str(datetime.datetime.now())}
    #print()
    #res.update(reperage_passive(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_pronoms(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_verbeconj_prorel_sub(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_tps(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_connecteurs_flesch(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_connecteurs_flesch(VIKIBEST+"/"+article.tag))
    #print()
    #res.update(reperage_images_liens_viki(article.tag[:-12],"vikidia")) #url = nom du fichier sans le _vikidia.txt
    #res.update(reperage_ponctuation(article.tag[:-12],"vikidia"))
    #p.populate(res, i, name=article.tag[:-4])
    
    
    
VIKIDIA = 'vikidia-TAL'
print('== Vikidia gros par articles ==')

data = load(VIKIDIA,automerge = False)

for i in range(0,len(data)):
    try:
        article = data[i]
        res = {
            'GEN_TITLE' : article.tag[:-4],
            'GEN_URL' : '',
            'GEN_DATE' : str(datetime.datetime.now())}
        print()
        res.update(reperage_passive(VIKIDIA+"/"+article.tag))
        print()
        res.update(reperage_pronoms(VIKIDIA+"/"+article.tag))
        print()
        res.update(reperage_verbeconj_prorel_sub(VIKIDIA+"/"+article.tag))
        print()
        res.update(reperage_tps(VIKIDIA+"/"+article.tag))
        print()
        res.update(reperage_connecteurs_flesch(VIKIDIA+"/"+article.tag))
        print()
        res.update(reperage_definition(VIKIDIA+"/"+article.tag))
        lemmas = extract_lemmas(VIKIDIA+"/"+article.tag)
        res.update(compare_Manulex(lemmas))
        res.update(compute_polysemy_index(VIKIDIA+"/"+article.tag))
        res.update(reperage_images_liens_viki(article.tag[:-12],"vikidia")) #url = nom du fichier sans le _wikipedia.txt
        res.update(reperage_ponctuation(article.tag[:-12],"vikidia"))
        p.populate(res, i, name=article.tag[:-4])
    except ZeroDivisionError:
        continue
    
    
WIKIPEDIA = 'Wikipedia-TAL'
print('== Wikipedia gros par articles ==')

data = load(WIKIPEDIA,automerge = False)

for i in range(0,len(data)):
    try:
        article = data[i]
        res = {
            'GEN_TITLE' : article.tag[:-4],
            'GEN_URL' : '',
            'GEN_DATE' : str(datetime.datetime.now())}
        print()
        res.update(reperage_passive(WIKIPEDIA+"/"+article.tag))
        print()
        res.update(reperage_pronoms(WIKIPEDIA+"/"+article.tag))
        print()
        res.update(reperage_verbeconj_prorel_sub(WIKIPEDIA+"/"+article.tag))
        print()
        res.update(reperage_tps(WIKIPEDIA+"/"+article.tag))
        print()
        res.update(reperage_connecteurs_flesch(WIKIPEDIA+"/"+article.tag))
        print()
        res.update(reperage_definition(WIKIPEDIA+"/"+article.tag))
        lemmas = extract_lemmas(WIKIPEDIA+"/"+article.tag)
        res.update(compare_Manulex(lemmas))
        res.update(compute_polysemy_index(WIKIPEDIA+"/"+article.tag))
        res.update(reperage_images_liens_viki(article.tag[:-14],"wikipedia")) #url = nom du fichier sans le _wikipedia.txt
        res.update(reperage_ponctuation(article.tag[:-14],"wikipedia"))
        p.populate(res, i, name=article.tag[:-4])
    except ZeroDivisionError:
        continue

p.ouput_all('results/multitests-articles')
