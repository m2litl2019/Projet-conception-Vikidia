import sys
import re

fichier=sys.argv[1]

with open(fichier, "r") as fichierTalismane:
	lecture=fichierTalismane.readlines()
	idPhrase = 0
	texte = ""
	Verbes = ""
	
	for ligne in lecture:
		if len(ligne) > 1:
			texte += ligne
			#print(texte)
		else:
			texte = ""
		
		match = re.findall(r'(\d+)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\t(.*?)\n', texte) 
		
		for i in match :
			nb_VINF=0
			nb_VPP = 0
			nb_VPR = 0
			nb_V = 0
			POS = i[3]
			temps = i [5]
			
		
		if POS == "VINF" : 
			nb_VINF+=1 
			print ( POS, nb_VINF, temps)
		elif POS == "VPP" : 
			nb_VPP +=1
			print(POS, nb_VPP, temps) 
		elif POS == "VPR" :
			nb_VPR +=1 
			print(POS, nb_VPR, temps)
		elif POS == 'V' : 
			nb_V +=1 
			print(POS, nb_V, temps)


		#je voudrais garder que les "t=...", et  ensuite calculer combien y en a (en combinaison avec le nombre de V/VPP/VPR/ qui correspondent).
		 




		
					
		

		
