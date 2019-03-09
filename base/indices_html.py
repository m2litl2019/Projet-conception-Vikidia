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

if __name__== "__main__":
	#dossier = sys.argv[1]
	url = "Navette_spatiale_Bourane"
	reperage_images_liens_viki(url)
