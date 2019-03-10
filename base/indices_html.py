import sys
import re
import glob 
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def reperage_images_liens_viki(url):
	req = Request("https://fr.vikidia.org/wiki/" + url, data = None, headers={"User-Agent":'Mozilla/5.0'})
	webpage = urlopen(req)
	html_doc = webpage.read()
	soup = BeautifulSoup(html_doc,"html.parser")
	nbImage = 0
	nbParag = 0
	nbH1 = 0 #lire mon commentaire en haut
	nbHx = 0
	nbLiens = 0

	imageOK = soup.select(".image")
	paragOK = soup.select("a[title]")
	h1OK = soup.select("h1")  #lire mon commentaire en haut
	hxOK = soup.select(".mw-headline")
	lienOK = soup.select("a[title]") #pour le moment, ce que j'ai fait, c'est de prendre tous les balises <a> qui possèdent un attribut "title" dedans...
	nbImage = len(imageOK)
	nbPara = len(paragOK)
	nbH1 = len(h1OK) #lire mon commentaire en haut
	nbHx = len(hxOK)
	nbLiens = len(lienOK)

	if nbParag == 0 and nbH1 == 0 and nbHx == 0:
		structure = 0
	else:
		structure = 1

	print("Nb images : ", nbImage) #nbLiens, "liens"
	print("Structure : ", structure)
	print("Nblinks : ", nbLiens)
	return { "META_NB_LINKS" : nbLiens,
			"META_NB_PICTURES" : nbImage,
			"STRUCTURE" : structure
	}

def reperage_ponctuation(url):
	req = Request("https://fr.vikidia.org/wiki/" + url, data = None, headers={"User-Agent":'Mozilla/5.0'})
	webpage = urlopen(req)
	html_doc = webpage.read()
	soup = BeautifulSoup(html_doc,"html.parser")
	gras=soup.find_all('b')
	scoreHTML= 0
	ponctuation=[".","!","?","...",";",":","\"","(",")","[","]", "/", "«", "»", "{","}"]
	typographie=["n°","&","%","$","£","€","#","§","@", "+","=","\*", "<",">"]
	if gras:
		scoreHTML+=(len(gras))
	italique=soup.find_all('i')
	if italique:
		scoreHTML+=(len(italique))
	souligne=soup.find_all('u')
	if souligne:
		scoreHTML+=(len(souligne))

	visible_text = soup.find_all('p')
	for element in visible_text:
		contenu=str(element.text)
		#print(contenu)
		nombre = re.finditer("[0-9]+(,[0-9]+)?", contenu)
		finAlinea= re.finditer("\r", contenu) # je ne suis pas sûre, l'auteur parle de fin d'alinéa donc je comprend ça comme un retour à la ligne, ajouter un \n?
		debutAlinea=re.finditer("^\t",contenu)
		if nombre: #je ne boucle pas pour les nombres afin de prendre en compte les nombres décimaux
			scoreHTML+=1
		if finAlinea:
			scoreHTML+=1
		if debutAlinea:
			scoreHTML+=1
		for caractere in contenu:
			majuscule = re.search("[A-Z]", caractere)
			if majuscule:
				scoreHTML+=1
			if caractere in ponctuation:
				scoreHTML+=1
			if caractere in typographie:
				scoreHTML+=1

	print("Score HTML", scoreHTML) # à normaliser avec le nombre de tokens
	return { "META_HTML_score" : scoreHTML}


if __name__== "__main__":
	#dossier = sys.argv[1]
	url = "Navette_spatiale_Bourane"
	reperage_images_liens_viki(url)
