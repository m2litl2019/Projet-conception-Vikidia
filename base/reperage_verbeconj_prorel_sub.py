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
ajout du calcul de la longueur moyenne des phrases 

"""

from texteval import load, Part

def meanFromList(liste):
    if len(liste) == 0:
        return '0 elements'
    else:
        return sum(liste)/len(liste)

def reperage_verbeconj_prorel_sub(target, debug=False):
    if isinstance(target, Part):
        data = target
    else:
        data = load(target)
    svTot = 0
    proRelTot = 0
    subordTot = 0
    nbModNcAll = []
    positionsV = []
    nb_phrase = 0
    longueur_phrase = []
    nb_verbs = 0
    all_tenses = []
    for sentence in data:
        longueur_phrase.append(len(sentence.words))
        #listeSV = []
        listeProRel = []
        listeSubord = []
        positionV = 0
        for word in sentence:
            if word.pos == 'PROREL':
                listeProRel.append(word)
            elif word.pos.startswith('V'):
                nb_verbs += 1
                if word.tense is not None:
                    for tense in word.tense.split(','):
                        if tense not in all_tenses:
                            all_tenses.append(tense)
                #listeSV.append(word)
                if positionV == 0:
                    positionV = word.num
                    positionsV.append(float(word.num))
            elif word.pos == 'CS':
                listeSubord.append(word)
            elif word.pos == 'NC':
                nbMod = 0
                for dep in sentence.get_dependents(word):
                    if dep.dep.startswith("mod"):
                        nbMod += 1
                        for coord in dep.coords:
                            nbMod += 1
                nbModNcAll.append(nbMod)
        #nbSV = len(listeSV)
        nbProRel = len(listeProRel)
        nbSubord = len(listeSubord)
        if debug:
            print('Phrase', nb_phrase, ':', nb_verbs, 'verbes conjugués,', nbProRel, 'pronoms relatifs', nbSubord, 'subordonnées',positionV, "position du premier verbe")
        #svTot += nb_verbs
        proRelTot += nbProRel
        subordTot += nbSubord
        
        nb_phrase += 1
    if debug:
        print('reperage_verbeconj_prorel_sub on', target)
        print('Total phrases             :', nb_phrase)
        print('Verbes conjugués          :', nb_verbs)
        print('Pronoms relatifs          :', proRelTot)
        print('Subordonnées              :', subordTot)
        print('Moyenne V1                :', meanFromList(positionsV))
        print('Moyenne modifieurs par NC :', meanFromList(nbModNcAll))
    return {
        'GEN_SENTENCE_LEN' : nb_phrase,
        'SYN_NB_VERBS_PER_SENTENCE' : nb_verbs / nb_phrase,
        'SYN_NB_VERBAL_TENSE' : len(all_tenses),
        'SYN_VERBAL_TENSE' : all_tenses,
        'VERBECONJ_PROREL_VERBES_CONJ' : nb_verbs,
        'VERBECONJ_PROREL_PRONOM_REL' : proRelTot,
        'VERBECONJ_PROREL_SUB' : subordTot,
        'VERBECONJ_PROREL_AVG_V1' : meanFromList(positionsV),
        'SYN_NB_MODIFIERS_PER_NOUN' : meanFromList(nbModNcAll),
        'GEN_WORD_LENGTH' : data.word_len,
        'AVG_SENTENCE_LEN' : meanFromList(longueur_phrase)
        }

if __name__ == '__main__':
    reperage_verbeconj_prorel_sub('ema.tal', debug=DEBUG)
