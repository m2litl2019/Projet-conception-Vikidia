"""
Il faudrait revoir le code pour compter le lien je crois...
Pour l'image, c'est bête ce que je propose mais ça marche (du moins avec l'article Boulangerie ça donne le bon compte),
à moins que vous ne sachez une autre façon moins bête ^^
"""

import sys
import re
from bs4 import BeautifulSoup

def has_title(tag):
    return tag.has_attr('title')

nbImage = 0
nbLiens = 0
with open("Boulangerie_vikidia.html", "r") as fichier:

	soup = BeautifulSoup(fichier, 'html.parser')
	imageOK = soup.select(".image")
	lienOK = soup.select("a[title]") #pour le moment, ce que j'ai fait, c'est de prendre tous les balises <a> qui possèdent un attribut "title" dedans...
	nbImage = len(imageOK)
	nbLiens = len(lienOK)

print("Il y a", nbImage, "images et", nbLiens, "liens.")
