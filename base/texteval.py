#-----------------------------------------------------------
# Code to dialog with a Talismane server
# and process Talismane results.
#
# Inspired from:
# https://github.com/joliciel-informatique/talismane/blob/master/talismane_examples/src/main/java/com/joliciel/talismane/examples/TalismaneClient.java
#
#-----------------------------------------------------------

#-----------------------------------------------------------
# Import
#-----------------------------------------------------------

import sys
import pickle
from socket import socket, AF_INET, SOCK_STREAM
import os
import os.path
import zipfile

#-----------------------------------------------------------
# Connexion to an instance of Talismane
#-----------------------------------------------------------

def open_sock():
    """Open a connection to a running Talismane instance on the localhost"""
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('localhost', 7272))
    return sock


def send(cmd, debug=False):
    """Send data to a running Talismane instance"""
    sock = open_sock()
    cmd += '\f\f\f'
    if debug:
        print('Sending input to server:', cmd)
    sock.send(cmd.encode(encoding='utf-8'))
    # receive data
    chunks = []
    done = False
    while not done:
        chunk = sock.recv(2048)
        if chunk == b'':
            done = True
        chunks.append(chunk)
    res = b''.join(chunks)
    if debug:
        print('Server:', res)
    sock.close()
    return process_multilines(res.decode(encoding='utf-8').split('\n'))


#-----------------------------------------------------------
# Data model
#-----------------------------------------------------------

# A Multifile is composed of X Multiparts
#       A Multipart is composed of X Parts
#           A Part is composed of X Sentences
#               A Sentence is composed of X Words

class Multifile:

    def __init__(self):
        self.multiparts = []

    def __getitem__(self, i):
        return self.multiparts[i]

    def __call__(self, s):
        for m in self.multiparts:
            if m.filename == s:
                return m
        return None

    def __repr__(self):
        return f"A multifile of {len(self.multiparts)} multiparts."

    def append(self, mp):
        self.multiparts.append(mp)


class Multipart:

    def __init__(self, filename=None):
        self.parts = []
        self.filename = filename

    def append(self, p):
        self.parts.append(p)

    def __repr__(self):
        if self.filename is None:
            return f"A multipart of {len(self.parts)} parts."
        else:
            return f"Multipart for file {self.filename} of {len(self.parts)} parts."

    def __getitem__(self, i):
        return self.parts[i]

    def __len__(self):
        return len(self.sentences)


class Part:

    def __init__(self, tag=None):
        self.sentences = []
        self.tag = tag

    def append(self, s):
        if len(s) > 0:
            self.sentences.append(s)

    def extend(self, p):
        self.sentences.extend(p.sentences)
    
    def __repr__(self):
        if self.tag is None:
            return f"A part of {len(self.sentences)} sentences."
        else:
            return f"A {self.tag} part of {len(self.sentences)} sentences."
    
    def __getitem__(self, i):
        return self.sentences[i]

    def __len__(self):
        return len(self.sentences)

    @property
    def word_len(self):
        nb = 0
        for s in self.sentences:
            nb += s.word_len
        return nb

class Sentence:

    def __init__(self):
        self.words = []

    def append(self, w):
        self.words.append(w)
        w.sentence = self

    def __repr__(self):
        return f"A sentence of {len(self.words)} words."

    @property
    def form(self):
        f = []
        for w in self.words:
            f.append(w.form)
        return ' '.join(f)

    @property
    def lemmas(self):
        lem = []
        for w in self.words:
            lem.append(w.lemma)
        return ' '.join(lem)

    @property
    def formnum(self):
        f = []
        for w in self.words:
            f.append(w.form + ' (' + w.num + ')')
        return ' '.join(f)
    
    @property
    def char_len(self):
        nb = 0
        for w in self.words:
            nb += len(w.form)
        return nb

    @property
    def word_len(self):
        nb = 0
        for w in self.words:
            if w.pos != 'PONCT':
                nb += 1
        return nb
    
    def __len__(self):
        return len(self.words)

    def __getitem__(self, i):
        return self.words[i]

    def __call__(self, i):
        for w in self.words:
            if w.num == str(i):
                return w
        return None
        # Bug
        print('Searched: ', i)
        for w in self.words:
            print(w.num, w == str(i), w.gov, w.dep, w)
        #raise Exception('Word not found with num = ' + str(i))
    
    def search_coords(self):
        """ construit une liste des éléments coordonnés à chaque mot de la phrase
        par exemple dans la phrase : "La vie belle et jolie se passe bien" actualise l'attribut du mot belle avec son coordonné (jolie) 
        l'idée c'est de réutiliser ça dans la recherche des modifieurs de chaque nom (il suffit de regarder si un modifieur a des éléments
        coordonnés pour les compter)
        
        l'idée c'était de rendre cette méthode privée (ne l'appeer que dans le lecteur talsimane pour ne l'utiliser qu'un seul coup mais 
        je ne sais pas où la mettre"""
        # recherche d'éléments coordonnés
        for word in self.words:
            if word.dep == "dep_coord":
                coord = self(word.gov)
                #if self(coord.gov) is None:
                #    print(word)
                #    print(word.sentence.formnum)
                #    print(word.gov)
                if self(coord.gov) is not None:
                    self(coord.gov).coords.append(word)
    
    
    def get_dependents(self, w):
        """retourne liste de words ayant pour gouverneur le target"""
        dependents = []
        for word in self.words:
            if word.gov == w.num:
                dependents.append(word)
        return dependents
    
class Word:

    def __init__(self, num, form, lemma, pos, pos_lexicon, morphinfo, f7, f8, f9, f10):
        self.num = num          # The token number (starting at 1 for the first token)
        self.form = form        # The original word form (or _ for an empty token)
        self.lemma = lemma      # The lemma found in the lexicon (or _ when unknown)
        self.pos = pos          # The part-of-speech tag
        self.coords = []
        #self.pos_lexicon = pos_lexicon # The grammatical category found in the lexicon
        # The additional morpho-syntaxic information found in the lexicon.
        self.number = None      #     n=p|s: number = plural or singluar
        self.gender = None      #     g=m|f: gender = male or female
        self.person = None      #     p=1|2|3|12|23|123: person = 1st, 2nd, 3rd (or a combination thereof if several can apply)
        self.poss_number = None #     poss=p|s: possessor number = plural or singular
        self.tense = None       #     t=pst|past|imp|fut|cond: tense = present, past, imperfect, future or conditional. Verb mood is not included, since it is already in the postag.
        informations = morphinfo.split('|')
        for info in informations:
            infos = info.split('=')
            if len(infos) > 1:
                typ, val = infos[0], infos[1]
                if typ == 'n':
                    self.number = 'plural' if val == 'p' else 'singular'
                elif typ == 'g':
                    self.gender = 'male' if val == 'm' else 'female'
                elif typ == 'p':
                    self.person = val
                elif typ == 'poss':
                    self.possessor_number = 'plural' if val == 'p' else 'singular'
                elif typ == 't':
                    self.tense = val
        self.gov = f7            # The token number of this token's governor (or 0 when the governor is the root)
        self.dep = f8            # The label of the dependency governing this token
        #self.f9 = f9            
        #self.f10 = f10          
        self.sentence = None

    def __str__(self):
        return self.num + '. ' + self.form + ' / ' + self.lemma + ' (' + self.pos + ')'

    def __repr__(self):
        return str(self)

    def get_dependents(self):
        return self.sentence.get_dependents(self)


#-----------------------------------------------------------
# Convert Talismane output to the datamodel
#-----------------------------------------------------------

def process(directory, expected=10):
    if not os.path.isdir(directory):
        raise Exception("Not a directory: " + directory)
    mf = Multifile()
    for filename in os.listdir(directory):
        filepath = directory + os.sep + filename
        f = open(filepath, mode='r', encoding='utf8')
        content = f.readlines()
        f.close()
        mp = Multipart(filename)
        cur_part = None
        cur_sent = None
        for line in content:
            if len(line.strip()) <= 1:
                cur_part.append(cur_sentence)
                cur_sentence = Sentence()
            elif line == '<p>\n':
                # start of paragraph
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line in ['</p>\n', '</p><hr/>\n', '</blockquote>\n']:
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = None
                cur_sentence = None
            elif line == '</h2><h2>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h2')
                cur_sentence = Sentence()
            elif line == '</h3><h3>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h3')
                cur_sentence = Sentence()
            elif line.startswith('</p><h2>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h2')
                cur_sentence = Sentence()
            elif line.startswith('</h2><p>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line in [
                    '</p><h3>\n',
                    '</p><div class="floatnone"><h3>\n']:
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h3')
                cur_sentence = Sentence()
            elif line == '</h3><h4>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h4')
                cur_sentence = Sentence()
            elif line.startswith('</h3><p>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line in [
                    '</p><h4>\n',
                    '</h2><h4>\n'
                    ]:
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h4')
                cur_sentence = Sentence()
            elif line == '<img alt="Clin d\'œil" data-file-height="500" data-file-width="500" height="30" src="//download.vikidia.org/vikidia/fr/images/thumb/5/5f/Clin.png/30px-Clin.png" srcset="//download.vikidia.org/vikidia/fr/images/thumb/5/5f/Clin.png/45px-Clin.png 1.5x, //download.vikidia.org/vikidia/fr/images/thumb/5/5f/Clin.png/60px-Clin.png 2x" title="Clin d\'œil" width="30"/></p><h3>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h3')
                cur_sentence = Sentence()
            elif line == '<img alt="Attention" data-file-height="220" data-file-width="237" height="19" src="//download.vikidia.org/vikidia/fr/images/thumb/3/3f/Attention.svg/20px-Attention.svg.png" srcset="//download.vikidia.org/vikidia/fr/images/thumb/3/3f/Attention.svg/30px-Attention.svg.png 1.5x, //download.vikidia.org/vikidia/fr/images/thumb/3/3f/Attention.svg/40px-Attention.svg.png 2x" title="Attention" width="20"/>\n':
                continue
            elif line in [
                    '</h4><h5>Dans la mythologie grecque</h5><p>\n',
                    '</p><h5>Dans la mythologie scandinave</h5><p>\n',
                    '</p><h5>Dans la Bible</h5><p>\n',
                    '</p><h5>Dans les croyances populaires provençales</h5><p>\n',
                    '</p><h5>Dans la littérature</h5><p>\n',
                    '</h4><h5>Lait et fromage</h5><p>\n',
                    '</p><h5>Viande</h5><p>\n',
                    '</p><h5>Poils et peau</h5><p>\n',
                    '</h2><div class="floatnone"><p>\n',
                    '</p><div class="floatnone"><p>\n',
                    '</h4><h5>Lille au cœur du conflit</h5><p>\n',
                    '<h5>La Résistance lilloise</h5><p>\n',
                    '</p><h5>La Collaboration lilloise</h5><p>\n',
                    '</p><h5>Subvenir à ses besoins sous l\'Occupation</h5><p>\n',
                    '</p><h5>Les loisirs des Lillois sous l\'Occupation</h5><p>\n',
                    '<p></p><p></p><p>\n',
                    '<p></p><p>\n',
                    '</blockquote><p>\n',
                    '</p><blockquote><div>\n',
                    '</blockquote><p style="margin:-0.7em 0 0.3em 6em">— Hergé</p><p>\n',
                    '<div align="left" class="NavFrame" style="margin-bottom:1em; width:100%; border-style:solid; -moz-border-radius:0; -webkit-border-radius:0; border-radius:0; border-color:#AAAAAA;background-color:#FFFFFF" title="[afficher]"><p>\n',
                    '</h4><h5>Braderie</h5><p>\n',
                    '</blockquote><p style="margin:-0.7em 0 0.3em 6em">— Adolf Hitler.</p><blockquote><div>\n',
                    '</h3><h5>Les Joueurs de Skat (Die Skatspieler, 1920) et les « Gueules cassées »</h5><p>\n',
                    '<ul class="gallery mw-gallery-traditional"><li class="gallerybox" style="width: 155px"><div class="gallerytext"></p><p>\n',
                    '</h3><h5>Les Joueurs de Skat (Die Skatspieler, 1920) et les « Gueules cassées »</h5><p>\n',
                    '</p><li class="gallerybox" style="width: 155px"><div class="gallerytext"><p>\n',
                    '<li class="gallerybox" style="width: 155px"><div class="gallerytext"><p>\n',
                    '</h4><h5>Façade de la Nativité</h5><p>\n',
                    '</p><h5>Façade de la Passion</h5><p>\n',
                    '</p><h5>Façade de la Gloire</h5><p>\n',
                    ]:
                if cur_part is not None and cur_sentence is not None:
                    cur_part.append(cur_sentence)
                    mp.append(cur_part)
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line in [
                    '</blockquote><h2>\n',
                    '<p style="margin:-0.7em 0 0.3em 6em">— Article de journal, Poméranie, Allemagne, milieu des années 30.</p><h2>\n'
                    '</h4><h2>\n',
                    '<p style="margin:-0.7em 0 0.3em 6em">— Article de journal, Poméranie, Allemagne, milieu des années 30.</p><h2>\n',
                    '</h4><h2>\n']:
                if cur_part is not None and cur_sentence is not None:
                    cur_part.append(cur_sentence)
                    mp.append(cur_part)
                cur_part = Part('h2')
                cur_sentence = Sentence()
            elif line.startswith('</h4><p>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line.startswith('</h3><h2>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h2')
                cur_sentence = Sentence()
            elif line.startswith('</h2><h3>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('h3')
            elif line.startswith('</p><p>'):
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = Part('p')
                cur_sentence = Sentence()
            elif line == '<h3>\n':
                cur_part = Part('h3')
                cur_sentence = Sentence()
            elif line == '</h3>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = None
                cur_sentence = None
            elif line == '</h2>\n':
                cur_part.append(cur_sentence)
                mp.append(cur_part)
                cur_part = None
                cur_sentence = None
            elif line == '<h2>\n':
                cur_part = Part('h2')
                cur_sentence = Sentence()
            elif len(line.split('\t')) >= expected:
                if cur_part is None:
                    cur_part = Part()
                    cur_sentence = Sentence()
                # a word line
                cur_sentence.append(process_line(line))
            else:
                print('>>>' + line + '<<< [' + str(len(line)) + ']')
                raise Exception("Unknown line.")
        if len(cur_sentence) > 0:
            cur_part.append(cur_sentence)
            mp.append(cur_part)
        mf.append(mp)
    return mf


def process_line(line, expected=10, debug=False):
    elems = line.split('\t')
    if len(elems) >= expected:
        return Word(*elems[0:expected])
    else:
        if debug:
            o = '(' + str(len(elems)) + ')'
            print(f"{o:5}", ':', line)
        return None


def process_multilines(content, Tag=None):
    part = Part(tag=Tag)
    sentence = None
    for line in content:
        w = process_line(line)
        if w is not None:
            if sentence is None:
                sentence = Sentence()
            sentence.append(w)
        else:
            if sentence is not None:
                part.append(sentence)
                sentence = None
    return part


def process_file(filename, encoding='utf8',Tag=None):
    file = open(filename, mode='r', encoding = encoding)
    content = file.readlines()
    file.close()
    return process_multilines(content,Tag)


def console():
    cmd = None
    while cmd != 'exit':
        cmd = input('enter sentence: ')
        if cmd != 'exit':
            part = send(cmd, debug=True)
            for sentence in part.sentences:
                for word in sentence.words:
                    print('   ', word)


def load_bin(filename):
    return pickle.load(open(filename, mode='rb'))


def load(filename, automerge=True,tag=None):
    if filename.endswith('.tal') or filename.endswith('.txt'):
        return process_file(filename,encoding="utf8",Tag=tag)
    elif filename.endswith('.bin'):
        return load_bin(filename)
    elif filename.endswith('.zip'):
        archive = zipfile.ZipFile(filename, 'r')
        content = archive.open(filename.replace('.zip', '.tal'), mode='r').read().decode('utf8').split('\n')
        return process_multilines(content)
    elif os.path.isdir(filename):
        parts = []
        for f in os.listdir(filename):
            parts.append(load(filename + os.sep + f, tag=f))
        if automerge:
            return merge(parts)
        else:
            return parts
    else:
        raise Exception('Impossible to load: ' + filename)


def merge(multipart):
    merged = multipart[0]
    for p in range(1, len(multipart)):
        merged.sentences.extend(multipart[p].sentences)
    return merged


def txt2tal(target, encoding):
    f = open(target, mode='r', encoding=encoding)
    content = f.readlines()
    f.close()
    part = Part()
    logicalline = ''
    for phyline in content:
        if len(phyline) > 1:
            logicalline += ' '+ phyline.strip()
        elif len(logicalline) > 0:
            #print(logicalline)
            part.extend(send(logicalline))
            logicalline = ''
    if len(logicalline) > 0:
        #print(logicalline)
        part.extend(send(logicalline))
        logicalline = ''
    f = open(target.replace('.txt', '.bin'), mode='wb')
    pickle.dump(part, f)
    f.close()
    return part


#order = 'test_process_file'
order = 'do_process'
#order = 'tal2bin'
target = 'VikiSimply-tal' #'litEnfant.tal' #'orthoClean_tal' #'md_fr.tal'
option_dump = True
if __name__ == '__main__':
    if len(sys.argv) > 1:
        order = sys.argv[1]
    if order == 'console':
        console()
    elif order == 'test_send':
        part = send('Bonjour le monde !', debug=True)
        print(part)
    elif order == 'test_process_file':
        part = process_file('ema.tal', 'utf8')
        if option_dump:
            pickle.dump(part, open('ema.bin', mode='wb'))
    elif order == 'test_loading':
        part = load_bin('ema.bin')
    elif order == 'tal2bin':
        if target is None:
            target = sys.argv[2]
        try: encoding = sys.argv[3]
        except IndexError: encoding = 'utf8'
        part = load(target) #process_file(target, encoding)
        pickle.dump(part, open(target.replace('.tal', '.bin'), mode='wb'))
    elif order == 'loadbin':
        filename = sys.argv[2]
        part = load_bin(filename)
    elif order == 'txt2bin':
        target = sys.argv[2]
        try: encoding = sys.argv[3]
        except IndexError: encoding = 'utf8'
        part = txt2tal(target, encoding)
    elif order == 'test_process':
        mf = process('vikibest_tal_test')
    elif order == 'do_process':
        mf = process(target)
        if option_dump:
            pickle.dump(mf, open(target+'.bin', mode='wb'))
        
