# -*- coding: utf8 -*-
"""
#auteur : ADG
#date : 09/02/2019
#projet Vikidia M2 LITL
#fonction : compter le nombre de verbes conjugués, le nombre de pronoms relatifs et le nombre de subordonnées
#entrée : un fichier Talismane .tal
#sortie : un fichier .csv contenant les comptes par fichier Talismane
#commande : 
#python3 SV_prorel_glob.py $dir
#$dir = chemin du dossier contenant les fichiers .tal 
"""

import sys
import re
import glob

grandTotSV = 0
grandTotProRel = 0
grandTotSubord = 0
grandTotPhrase = 0

dossier = sys.argv[1]
sortie = open("SV_prorel_subord_orthoCorpus.csv", "w")
print('Fichier', 'Phrases', 'Verbes conjugués', 'Pronoms relatifs', 'Subordonnées', sep = "\t", file = sortie)

for Tal in glob.glob(dossier+"/*.tal"):
	print("Traitement du", Tal, ".....")
	with open(Tal, "r") as fichierTal:
		lecture = fichierTal.readlines()
		liste_de_phrases = []
		phrase = ''

		for ligne in lecture:
			if len(ligne) > 1:
				phrase += ligne
			else:
				liste_de_phrases.append(phrase)
				phrase = ''
		
		nbPhrase = 0			
		nbSV = 0
		nbProRel = 0
		nbSubord = 0
		svTot = 0
		proRelTot = 0
		subordTot = 0
		
		for phrase in liste_de_phrases:
			nbPhrase +=1
			
			sv = re.compile(r'\tV\t') #pour trouver les mots étiquetés "V"
			listeSV = sv.findall(phrase)
			
			pr = re.compile(r'\tPROREL\t') #pour trouver les mots étiquetés "PROREL"
			listeProRel = pr.findall(phrase)
			
			subord = re.compile(r'\tCS\t') #pour trouver les mots étiquetés "CS"
			listeSubord = subord.findall(phrase)
			
			nbSV = len(listeSV)
			nbProRel = len(listeProRel)
			nbSubord = len(listeSubord)
			#print('Phrase', nbPhrase, ':', nbSV, 'verbes conjugués,', nbProRel, 'pronoms relatifs', nbSubord, 'subordonnées') #pour afficher le compte phrase par phrase
			svTot += nbSV
			proRelTot += nbProRel
			subordTot += nbSubord

		print(Tal, nbPhrase, svTot, proRelTot, subordTot, sep = "\t", file = sortie)
		
		grandTotSV += svTot
		grandTotProRel += proRelTot
		grandTotSubord += subordTot
		grandTotPhrase += nbPhrase
print ('Grand Total :', grandTotPhrase, grandTotSV, grandTotProRel, grandTotSubord, sep = "\t", file = sortie)
print ('Grand Total :', grandTotPhrase, 'phrases,', grandTotSV, 'verbes conjugués,', grandTotProRel, 'pronoms relatifs et', grandTotSubord, 'subordonnées.')
sortie.close()
