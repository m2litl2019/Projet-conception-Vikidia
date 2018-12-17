#-------------------------------------------------
# Import
#-------------------------------------------------

# standard
from enum import Enum
import datetime
import os
import os.path
# dynamic code
from importlib import reload
try:
    import whiteboard as wb
except ModuleNotFoundError:
    print('[WARN] Module whiteboard not found.')

#-------------------------------------------------
# Data model
#-------------------------------------------------

class Word:
    
    def __init__(self, form, lemma, pos, info, gov, dep):
        self.form = form
        if lemma == '_':
            self.lemma = f"?{form}"
        else:
            self.lemma = lemma
        self.pos = pos
        self.info = info
        self.gov = gov
        self.dep = dep

    def __str__(self):
        return f"{self.form}"
    
    def __repr__(self):
        return f"<Word {self.form, self.lemma, self.pos}>"

articles = {}
words = {}
words_count = {}
filtered = ['P', 'P+D', 'P+PRO',
            'NC', 'ADJ', 'CS',
            'V', 'VIMP', 'VINF', 'VPP', 'VPR', 'VS',
            'ADV', 'ADVWH', 'I',
            'PRO', 'PROREL', 'PROWH',
            'DET']
# ignored : CLO, CLR, CLS, ET, NPP

def load(fpath):
    f = open(fpath, mode='r', encoding='utf8')
    lines = f.readlines()
    nb_words = 0
    for line in lines:
        elements = line.split('\t')
        if len(elements) >= 4:
            form = elements[1]
            lemma = elements[2]
            typ1 = elements[3]
            #typ2 = elements[4] copy of typ1
            nb_words += 1
            if len(elements) >= 5:
                info = elements[5]
                #gov = elements[6]
                #dep = elements[7]
                #x3 = elements[8]
                #x4 = elements[9]
            else:
                info = None
            gov = None
            dep = None
        if typ1 not in filtered:
            continue
        if lemma == '_':
            lemma = f"?{form}" 
        #if form == 'sol' and lemma == '_':
        #    print(os.path.basename(fpath))
        key = lemma + '_' + typ1
        if key in words:
            words_count[key] += 1
        else:
            words[key] = Word(form, lemma, typ1, info, gov, dep)
            words_count[key] = 1
    f.close()
    name = os.path.splitext(os.path.basename(fpath))[0]
    articles[name] = nb_words


def dump():
    f = open('dump.txt', mode='w', encoding='utf8')
    sorted_by_num = sorted(words_count, key=lambda x: words_count[x], reverse=True)
    for key in sorted_by_num:
        w = words[key]
        nb = words_count[key]
        f.write(w.lemma + '\t' + w.pos + '\t' + str(nb) + '\n')
    f.close()

if __name__ == '__main__':
    #dir_in = r".\corpusComparableWikiVikiTAL\wikipedia"
    dir_in = r".\corpusComparableWikiVikiTAL\vikidia"
    file_names = os.listdir(dir_in)
    for fname in file_names:
        print('[INFO] Loading', fname)
        load(dir_in + os.sep + fname)
    # moyenne
    total = 0
    for key, val in articles.items():
        total += val
    print('Average =', total/len(articles))
    brunet = open('brunet.txt', mode='r', encoding='utf8')
    lines = brunet.readlines()
    words_of_brunet = list(set([k.rstrip() for k in lines]))
    in_brunet = []
    out_brunet = []
    #in_brunet_lemma = {}
    for key, w in words.items():
        if w.lemma in words_of_brunet and w.lemma not in in_brunet:
            in_brunet.append(w.lemma)
        elif w.lemma not in out_brunet:
            out_brunet.append(w.lemma)
            #if w.lemma not in in_brunet_lemma:
            #    in_brunet_lemma[w.lemma] = w.pos
            #else:
            #    print('Trying to add', w.lemma, w.pos)
            #    print('Already inside:', in_brunet_lemma[w.lemma])
            #    raise Exception(w.lemma + '_' + w.pos)
    print('In brunet =', len(in_brunet), 'Out brunet =', len(out_brunet))
    lemma_indistinct = []
    for key in words:
        lemma_indistinct.append(words[key].lemma)
    lemma_indistinct = list(set(lemma_indistinct))
    print('Couverture =', len(in_brunet) / len(lemma_indistinct))
    print('Total mots =', sum(words_count.values()))
    #dump()
    exit()

# http://joliciel-informatique.github.io/talismane/#tagset
# ADJ	Adjective
# ADV	Adverb
# ADVWH	Interrogative adverb
# CC	Coordinating conjunction
# CLO	Clitic (object)
# CLR	Clitic (reflexive)
# CLS	Clitic (subject)
# CS	Subordinating conjunction
# DET	Determinent
# DETWH	Interrogative determinent
# ET	Foreign word
# I	Interjection
# NC	Common noun
# NPP	Proper noun
# P	Preposition
# P+D	Preposition and determinant combined (e.g. "du")
# P+PRO	Preposition and pronoun combined (e.g. "duquel")
# PONCT	Punctuation
# PRO	Pronoun
# PROREL Relative pronoun
# PROWH	Interrogative pronoun
# V	Indicative verb
# VIMP	Imperative verb
# VINF	Infinitive verb
# VPP	Past participle
# VPR	Present participle
# VS	Subjunctive verb

# http://joliciel-informatique.github.io/talismane/#section2.3.5
# The CoNLL format used by Talismane outputs the following information in each row:

# The token number (starting at 1 for the first token)
# The original word form (or _ for an empty token)
# The lemma found in the lexicon (or _ when unknown)
# The part-of-speech tag
# The grammatical category found in the lexicon
# The additional morpho-syntaxic information found in the lexicon.
# Additional morpho-syntaxic information:
#   g=m|f: gender = male or female
#   n=p|s: number = plural or singluar
#   p=1|2|3|12|23|123: person = 1st, 2nd, 3rd (or a combination thereof if several can apply)
#   poss=p|s: possessor number = plural or singular
#   t=pst|past|imp|fut|cond: tense = present, past, imperfect, future or conditional. Verb mood is not included, since it is already in the postag.
# The token number of this token's governor (or 0 when the governor is the root)
# The label of the dependency governing this token
# Labels :
#   _
#   a_obj
#   aff
#   arg
#   ato
#   ats
#   aux_caus
#   aux_pass
#   aux_tps
#   comp
#   coord
#   de_obj
#   dep
#   dep_coord
#   det
#   mod
#   mod_rel
#   obj
#   p_obj
#   ponct
#   prep
#   root
#   sub
#   suj

