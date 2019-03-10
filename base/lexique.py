import sys
import re
import csv
from texteval import *
from reperage_verbeconj_prorel_sub import meanFromList

def remove_duplicates(lst, equals=lambda x, y: x == y): #fonction pour supprimer les lemmes en doublon, j'aurais pu faire un set mais j'ai trouvé ce bout de code pratique! C'est peut être un peu long à executer par contre
 
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


def extract_lemmas(target):
	#fichier=sys.argv[1]
	lemme=set()
	data = load(target)
	for sentence in data:
		for word in sentence:
			if word.pos == "NC" and word.lemma != "_" and not re.search(r"\d",word.lemma):
				lemme.add(word.lemma)
	#remove_duplicates(lemme)
	#print(lemme)
	return lemme


def compare_Manulex(lemme):
	forme=[]
	compteListe=0
	with open('manulex.csv', newline='', encoding='utf-16') as csvfile:
		tableau=csv.reader(csvfile, delimiter=',')
		for row in tableau:
			forme.append(row[1])

	for compo in lemme:
		if compo not in forme:
			compteListe+=1
	print(compteListe, " mots qui ne sont pas dans Manulex") #c'était juste pour tester, à voir si on fait un pourcentage, un score, etc...
	return {"SEMLEX_MANLUEX":compteListe}


def compute_polysemy_index(lemmas):
	with open("GLAWI.txt", encoding="utf-8") as glawi:
		indices_poly = []
		for line in glawi:
			
			forme = line.split("\t")
			if forme[0] == "n" and forme[1] in lemmas:
				indices_poly.append(int(forme[2]))
				
	#print(meanFromList(indices_poly))
	return {"SEMLEX_POLY_INDEX": meanFromList}

if __name__ == "__main__":
	lemmas = extract_lemmas("ema.bin")
	compare_Manulex(lemmas)
	compute_polysemy_index(lemmas)
