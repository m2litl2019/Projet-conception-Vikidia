import sys 
 
 
 
dossier = sys.argv[1]
NmotPh = 0 
Lmoyenne = [] 
with open(dossier) as ficher :

	for ligne in ficher :
		ligne = ligne.rstrip("\n") 
		ligne = ligne.split("\t") 
		#print(ligne)
		if len(ligne) > 1 : 
			NmotPh = ligne[0]
		else : 
			Lmoyenne.append(NmotPh)
			print(NmotPh)
somme = 0			
for i in Lmoyenne: 
	somme +=int(i)

moyenne = somme/len(Lmoyenne) 
#print(len(Lmoyenne), "\t", somme , "\t", moyenne)

	
		
