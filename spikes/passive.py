# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 14:27:03 2019

@author: TO124473
"""


import re

#fichier=sys.argv[1]

with open("ema.tal", "r") as fichierTal:
	lecture=fichierTal.readlines()
	liste_de_phrases = []
	paragraphe=[]
	phrase = ''
	listePassive=[]

	for ligne in lecture:
		match=re.search(r"^<P.*",ligne) # Pour trouver les débuts de paragraphe=> dans Ema= un texte

		if len(ligne) > 1:
			phrase += ligne
		
		else:
			paragraphe.append(phrase)
			phrase = ''
				

	for phrase in paragraphe: 
		passive = re.search(r'aux_pass',phrase) #Suffisant si on pense qu'il y a qu'une seule forme passive par phrase 
		if passive:
			listePassive.append(phrase)
nbPhrase=len(paragraphe)
nbPassive=len(listePassive)

print(nbPhrase," ",nbPassive)
