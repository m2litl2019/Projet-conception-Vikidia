#Ne fonctionne pas pour certains articles Wikipédia possédant des sous-titres comme des propositions d'articles homonymes => https://fr.wikipedia.org/wiki/Maus 

import urllib.request
import sys

def process_target_both(name):
	process_target(name, "https://fr.vikidia.org/wiki/"+ name, 'vikidia')
	process_target(name, "https://fr.wikipedia.org/wiki/" + name, 'wikipedia')

def process_target(target, url, suffix):

	req = urllib.request.Request(
		url, 
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)

	response = urllib.request.urlopen(req)
	#print(f.read().decode('utf-8'))

	#response = urllib.request.urlopen(url)
	html_doc = response.read()
	#print(html_doc)

	from bs4 import BeautifulSoup, Comment
	soup = BeautifulSoup(html_doc, 'html.parser')
	part = soup.find("div", {"id" : "mw-content-text"}) 

	#for div in part.findAll("div"): 
	#    div.decompose()

	for center in part.findAll("center"):
		center.decompose()

	for table in part.findAll("table"):
		table.decompose()

	for child in part.children:
		if isinstance(child, Comment):
			child.extract()

	def replace_by_text(part, tag):
		for child in part.findAll(tag):
			child.insert_before(child.text)
			child.decompose()
		return part

	replace_by_text(part, "a")
	replace_by_text(part, "b")
	replace_by_text(part, "i")
	replace_by_text(part, "strong")
	replace_by_text(part, "em")
	replace_by_text(part, "u")

	text = ''
	for child in part.findAll("p"):
		text += child.text

	print(text)
	f = open(target + '_' + suffix + '.txt', mode='w', encoding='utf8')
	f.write(text)
	f.close()

if __name__ == '__main__':
	article=["%C3%89checs","%C3%89l%C3%A9phant","Australie","Belgique ","Boulangerie","Caracal","Catherine_II_de_Russie","Ch%C3%A8vre","Chat","Cheval","Chien","Com%C3%A8te","D%C3%B4me_du_Rocher","Geyser","Homme_au_masque_de_fer","Ich_bin_ein_Berliner","Kurdistan","Indira_Gandhi","Kylian_Mbapp%C3%A9","L%C3%A9gionelle","L%C3%A9onard_de_Vinci","La_Ferme_des_animaux","Le_Lotus_bleu","Lille","Lyon","Marl%C3%A8ne_Dietrich","Massif_central","Mode_(habillement)","Monstre_de_Gila","Mosqu%C3%A9e","Napol%C3%A9on_Ier","Navette_spatiale_Bourane","Op%C3%A9ra_Garnier","Otto_Dix","Paris","Poivre","Portugal","Pyr%C3%A9n%C3%A9es","Rome","Rubik%27s_Cube","Saturn_V","Tyrannosaurus_rex","Vienne_(Is%C3%A8re)","Volcan"]
	for pouet in article:
		process_target_both(pouet)
