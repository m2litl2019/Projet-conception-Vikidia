"""
MAJ 07/03 : j'ai désactivé le code pour compter les liens
et j'ai rajouté un bout de code pour la structuration.
En gros, si la page contient au moins un des balises <p> ou <h1> ou <h2, 3, etc.>, structure vaut 1.
S'il n'y a ni balise <p>, ni <h1>, ni <h2, 3, etc.>, structure vaut 0.
Mais /!\ je crois que tous les articles, même les plus pourris, possèdent un <h1> non ? (= leur titre correspond à <h1> ?)
Si c'est le cas, on pourra enlever la partie où on cherche les <h1> de notre critère.

06/03 :
Il faudrait revoir le code pour compter le lien je crois...
Pour l'image, c'est bête ce que je propose mais ça marche (du moins avec l'article Boulangerie ça donne le bon compte),
à moins que vous ne sachez une autre façon moins bête ^^
"""

import sys
import re
from bs4 import BeautifulSoup

nbImage = 0
nbParag = 0
nbH1 = 0 #lire mon commentaire en haut
nbHx = 0
#nbLiens = 0
with open("Boulangerie_vikidia.html", "r") as fichier:

	soup = BeautifulSoup(fichier, 'html.parser')
	imageOK = soup.select(".image")
	paragOK = soup.select("a[title]")
	h1OK = soup.select("h1")  #lire mon commentaire en haut
	hxOK = soup.select(".mw-headline")
	#lienOK = soup.select("a[title]") #pour le moment, ce que j'ai fait, c'est de prendre tous les balises <a> qui possèdent un attribut "title" dedans...
	nbImage = len(imageOK)
	nbPara = len(paragOK)
	nbH1 = len(h1OK) #lire mon commentaire en haut
	nbHx = len(hxOK)
	#nbLiens = len(lienOK)

if nbParag == 0 and nbH1 == 0 and nbHx == 0:
	structure = 0
else:
	structure = 1
	
print("Il y a", nbImage, "images.") #nbLiens, "liens"
print("Structure :", structure)
