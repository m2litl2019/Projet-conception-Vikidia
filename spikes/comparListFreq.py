import sys
import re
import csv

def remove_duplicates(lst, equals=lambda x, y: x == y):
 
    # Normalement en Python on adore le duck typing, mais là cet algo suppose
    # l'usage d'une liste, donc on met un gardefou.
    if not isinstance(lst, list):
        raise TypeError('This function works only with lists.')
 
    # là on est sur quelque chose qui ressemble vachement plus à du code C ^^
    i1 = 0
    l = (len(lst) - 1)
 
    # on itère mécaniquement sur la liste, à l'ancienne, avec nos petites
    # mains potelées.
    while i1 < l:
 
        # on récupère chaque élément de la liste, sauf le dernier
        elem = lst[i1]
 
        # on le compare à l'élément suivant, et chaque élément après
        # l'élément suivant
        i2 = i1 + 1
        while i2 <= l:
            # en cas d'égalité, on retire l'élément de la liste, et on
            # décrément la longueur de la liste ainsi amputée
            if equals(elem, lst[i2]):
                del lst[i2]
                l -= 1
            i2 += 1
 
        i1 += 1
 
    return lst

compteListe=0
#fichier=sys.argv[1]
lemme=[]
with open("Vikidia_unique.tal", "r") as fichierTal:
	lecture=fichierTal.readlines()
	for ligne in lecture:
		elements=ligne.split("\t")
		if len(elements) >= 4:
			lemme.append(elements[2])
			
	#lemme.remove("(")
	remove_duplicates(lemme)
	print(lemme)

			
forme=[]
with open('manulex.csv', newline='', encoding='utf-16') as csvfile:
	tableau=csv.reader(csvfile, delimiter=',')
	for row in tableau:
		forme.append(row[1])

for compo in lemme:
	if compo not in forme:
		compteListe+=1
print(compteListe, " mots qui ne sont pas dans Manulex")
