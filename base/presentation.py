class Presentation:

    def __init__(self, template):
        f = open(template, mode='r', encoding='utf8')
        self.template = f.read()
        f.close()

    def populate(self, dic):
        for key, val in dic.items():
            if type(val) == str and val.startswith('http'):
                val = f'<a href="{val}">{val}</a>'
            self.template = self.template.replace(key, str(val))

    def output(self, filename):
        f = open(filename, mode='w', encoding='utf8')
        f.write(self.template)
        f.close()

if __name__ == '__main__':
    p = Presentation('maquette.html')
    dummy = {
        'GEN_TITLE' : 'Titre 1',
        'GEN_URL' : 'http://www.test.com',
        'SURF_WORD_LENGTH' : 32,
        'GEN_NOTE' : 'Bien',
        'META_NB_LINKS' : 2,
        'META_NB_PICTURES' : 3,
        'META_NB_SECTION' : 5,
        'META_NB_PARAGRAPH' : 1,
        'SURF_AVG_WORD_LENGTH' : 10,
        'SURF_FLESCH_KINCAID' : 2,
        'SYN_RES1' : 5,
        }
    p.populate(dummy)
    p.output('results1.html')

