"""
#auteur   : ADG
#date     : 09/02/2019
#version  : 2 - mise à jour compléxité syntaxique
#projet   : Vikidia M2 LITL
#fonction : compter le nombre de verbes conjugués, le nombre de pronoms relatifs et le nombre de subordonnées + nb mots moyen avant verbe principal
#entrée   : un fichier Talismane .tal
#sortie   : affichage des comptes sur le terminal
#commande : python3 reperage_verbeconj_prorel_sub.py

commentaire version : compte les modifieurs des NC (mais il n'y a pas encore accès aux coordonnés de ces modifieurs --> mesure pas très efficace du coup car ne compte pas tous les modifieurs (s'appuie sur v2 de texteval.py que je n'ai pas modifiée a souhait total)
"""

from texteval import load
import pandas as pd
import numpy as np

DEBUG = False

def meanFromList(liste):
    return pd.Series(liste).astype(float).mean()

def reperage_verbeconj_prorel_sub(target, debug=DEBUG):
    data = load(target)
    svTot = 0
    proRelTot = 0
    subordTot = 0
    nbModNcAll = []
    positionsV = []
    nb_phrase = 0
    for sentence in data:
        listeSV = []
        listeProRel = []
        listeSubord = []
        positionV = 0
        for word in sentence:
            if word.pos == 'PROREL':
                listeProRel.append(word)
            elif word.pos.startswith('V'):
                listeSV.append(word)
                if positionV == 0:
                    positionV = word.num
                    positionsV.append(word.num)
            elif word.pos == 'CS':
                listeSubord.append(word)
            elif word.pos == "NC":
                nbMod = 0
                for dep in sentence.get_dependents(word):
                    if dep.dep.startswith("mod"):
                        nbMod += 1
                        print(dep.dep,dep.form)
                        for coord in dep.coords:
                            nbMod += 1
                nbModNcAll.append(nbMod)
        nbSV = len(listeSV)
        nbProRel = len(listeProRel)
        nbSubord = len(listeSubord)
        if debug:
            print('Phrase', nb_phrase, ':', nbSV, 'verbes conjugués,', nbProRel, 'pronoms relatifs', nbSubord, 'subordonnées',positionV,"position du premier verbe")
        svTot += nbSV
        proRelTot += nbProRel
        subordTot += nbSubord
        
        nb_phrase += 1
    print('reperage_verbeconj_prorel_sub on', target)
    print('Total phrases             :', nb_phrase)
    print('Verbes conjugués          :', svTot)
    print('Pronoms relatifs          :', proRelTot)
    print('Subordonnées              :', subordTot)
    print('Moyenne V1                :', meanFromList(positionsV))
    print('Moyenne modifieurs par NC :', meanFromList(nbModNcAll))


if __name__ == '__main__':
    reperage_verbeconj_prorel_sub('ema.tal', debug=DEBUG)
