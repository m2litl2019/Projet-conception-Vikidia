import sys
import re

#fichier=sys.argv[1]

with open("Vikidia_unique.tal", "r") as fichierTal:
	lecture=fichierTal.readlines()
	liste_de_phrases = []
	phrase = ''

	for ligne in lecture:
		if len(ligne) > 1:
			phrase += ligne
		else:
			liste_de_phrases.append(phrase)
			phrase = ''
				
	nbPronom=0
	index = 1
	for phrase in liste_de_phrases:
		p = re.compile(r'PRO')
		listeDeP = p.findall(phrase)
		if len(listeDeP) > 1:
			nb_PRO = len(listeDeP)
			print('Phrase', index, ': ', nb_PRO, ' PRO')
			index +=1