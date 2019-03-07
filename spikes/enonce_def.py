import sys 
import re 
import glob 
import os 

dossier = sys.argv[1]
fichier = 0 
tout_patron=0
sortie = open("enonces_def_VIKIDIA.csv", "w")  
sortie.write("id_fichier\tpatron\tnumPatron\tNumMoyenPatron\tcontexte\n")



patrons = ["c'est-à-dire","à savoir", "par exemple", "comme par exemple", "comme", "tel", "tels", "telle", "telles", "soit", "type de", "type d'","du type", "groupe de", "groupe d'", "race", "espèce de", "espèce d'", "sorte de", "sorte d'", "signifie", "signifient", "désigne", "désignent", "("] 


  
for fichiers in glob.glob(dossier+"/*.txt"):
	nomFichier = os.path.basename(fichiers)
	fichier +=1 
	lignes = 0
	numPatrons = 0
	with open(fichiers, "r") as fichiersViki:
		for ligne in fichiersViki : 
			lignes+=1
			texte=ligne
			numPatrons +=1 
			for element in patrons : 
				if element in texte : 
					#tout_patron += numPatrons
					sortie.write(nomFichier + "\t" + element +"\t"  + str(numPatrons) + "\t" + "na"+ "\t" + texte) 
"""
ICI ON VOULAIS CALCULER LA MOYENNE DES PATRONS PAR ARTICLE, SI ON ARRIVE A AVOIR L'INFO PARAGRAPHE ON POURRA LA FAIRE PAR PARAGRAPHE AUSSI 					
	if (tout_patron and numPatrons) > 0 :
		NbMoyenpatron = tout_patron / numPatrons
		sortie.write(nomFichier + "\t" + element + "\t" + str(numPatrons) + "\t" + str(NbMoyenpatron) +"\t" + texte)
				#	print(element, texte)
	print("en cours", fichier)
print("end")
					
"""		
sortie.close()
