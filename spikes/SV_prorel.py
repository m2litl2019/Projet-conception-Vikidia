# -*- coding: utf8 -*-
"""
#auteur : ADG
#date : 09/02/2019
#projet Vikidia M2 LITL
#fonction : compter le nombre de verbes conjugués, le nombre de pronoms relatifs et le nombre de subordonnées
#entrée : un fichier Talismane .tal
#sortie : affichage des comptes sur le terminal
#commande : 
#python3 SV_prorel.py
#note: pour traiter plusieurs fichiers à la fois, utilisez SV_prorel_glob.py
"""

import sys
import re

with open("./orthoTAL/192_alegria.tal", "r") as fichierTal:
	lecture = fichierTal.readlines()
	liste_de_phrases = []
	phrase = ''

	for ligne in lecture:
		if len(ligne) > 1:
			phrase += ligne
		else:
			liste_de_phrases.append(phrase)
			phrase = ''
				
	nbSV = 0
	nbProRel = 0
	nbSubord = 0
	index = 0
	svTot = 0
	proRelTot = 0
	subordTot = 0
	
	for phrase in liste_de_phrases:
		index +=1
		
		sv = re.compile(r'\tV\t') #pour trouver les mots étiquetés "V"
		listeSV = sv.findall(phrase)
		
		pr = re.compile(r'\tPROREL\t') #pour trouver les mots étiquetés "PROREL"
		listeProRel = pr.findall(phrase)
		
		subord = re.compile(r'\tCS\t') #pour trouver les mots étiquetés "CS"
		listeSubord = subord.findall(phrase)
		
		nbSV = len(listeSV)
		nbProRel = len(listeProRel)
		nbSubord = len(listeSubord)
		
		print('Phrase', index, ':', nbSV, 'verbes conjugués,', nbProRel, 'pronoms relatifs', nbSubord, 'subordonnées')
		svTot += nbSV
		proRelTot += nbProRel
		subordTot += nbSubord
		
	print('Total :', index, 'phrases,', svTot, 'verbes conjugués,', proRelTot, 'pronoms relatifs et', subordTot, 'subordonnées.')
