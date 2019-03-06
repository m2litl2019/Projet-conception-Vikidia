import sys
import re
from bs4 import BeautifulSoup

scoreHTML= 0
ponctuation=[".","!","?","...",";",":","\"","(",")","[","]", "/", "«", "»", "{","}"]
typographie=["n°","&","%","$","£","€","#","§","@", "+","=","\*", "<",">"]

with open("vikibest_html/Chat_vikidia.txt", "r") as fichier:

	soup = BeautifulSoup(fichier, 'html.parser')

	gras=soup.find_all('b')
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

	print(scoreHTML) # à normaliser avec le nombre de tokens