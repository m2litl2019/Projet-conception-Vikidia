import sys
import re
import glob


# vérifier que ça ne prenne pas en compte la typo entre les balises
score= 0
ponctuation=[".","!","?","...",";",":","\"","(",")", "[","]", "/", "«", "»", "{","}"]
typographie=["n°","&","%","$","£","€","#","§","@", "+","=","\*", "<",">"]

with open("fichier.html", "r") as fichier:
	for ligne in fichier:


		for element in ligne: 
			if element == "[A-Z]": 
				score += 1
			if element == "[0-9]+?":
				score += 1
			if element in ponctuation:
				score+=1
			if element in typographie:
				score+=1
			if element == "\r": # je ne suis pas sûre, l'autre parle de fin d'alinéa donc je comprend ça comme un retour à la ligne, ajouter un \n?
				score+=1
			if element == "^\t": #début d'alinéa
				score+=1
			if element == "<b>":
				score+=1
			if element == "<i>":
				score+=1
			if element == "<u>":
				score+=1

	print(score) # à normaliser avec le nombre de tokens
	

	
	
	