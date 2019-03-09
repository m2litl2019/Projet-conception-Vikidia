from texteval import *
from presentation import Presentation
from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
from reperage_tpsV import reperage_tps
from indices_html import reperage_images_liens_viki
import datetime


p = Presentation('templates/maquette2.html')


VIKIBEST = 'vikibest'
print('== VIKIBEST par articles ==')



data = load(VIKIBEST,automerge = False)

for i in range(0,len(data)):
	article = data[i]
	res = {
    'GEN_TITLE' : article.tag[:-4],
    'GEN_URL' : '',
    'GEN_DATE' : str(datetime.datetime.now())}
	print()
	res.update(reperage_passive(VIKIBEST+"/"+article.tag))
	print()
	#res.update(reperage_pronoms(VIKIBEST))
	#print()
	#res.update(reperage_verbeconj_prorel_sub(VIKIBEST))
	#print()
	#res.update(reperage_tps(VIKIBEST))
	#print()
	#res.update(reperage_connecteurs(VIKIBEST))
	#print()
	#res.update(reperage_definition(VIKIBEST))
	#print()
	res.update(reperage_images_liens_viki(article.tag[:-12])) #url = nom du fichier sans le _vikidia.txt
	p.populate(res, i, name=article.tag[:-4])

p.ouput_all('results/multitests-articles')
