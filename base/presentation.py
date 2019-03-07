try:
    import xlwt
except ModuleNotFoundError:
    XLWT = False
else:
    XLWT = True

class Presentation:

    def __init__(self, templatefile):
        self.templatefile = templatefile
        self.set_of_keys = []
        self.set_of_names = []
    
    def populate(self, dic, who=0, coherency=True, name='Unknown'):
        if who == len(self.set_of_keys):
            self.set_of_keys.append({})
        elif who > len(self.set_of_keys):
            raise Exception('set_of_keys to small : ' + str(len(self.set_of_keys)))
        self.set_of_names.append(name)
        if coherency:
            for k, v in dic.items():
                if k in self.set_of_keys[who]:
                    if v != self.set_of_keys[who][k]:
                        raise Exception("Multiple values for key: " + k)
        self.set_of_keys[who].update(dic)

    def output_html(self, filename):
        for who in range(0, len(self.set_of_keys)):
            f = open(self.templatefile, mode='r', encoding='utf8')
            template = f.read()
            f.close()
            for key, val in self.set_of_keys[who].items():
                if type(val) == str and val.startswith('http'):
                    val = f'<a href="{val}">{val}</a>'
                if type(val) == float:
                    val = f"{val:.3f}"
                template = template.replace(key, str(val))
            f = open(filename.replace('.html', '_' + str(who) + '.html'), mode='w', encoding='utf8')
            f.write(template)
            f.close()

    def output_excel(self, filename):
        if not XLWT: raise Exception('xlwt not installed. Do "pip install xlwt" before.')
        wb = xlwt.Workbook(encoding='utf8')
        ws = wb.add_sheet("Results")
        ws.col(0).width = 256 * 50
        all_keys = []
        for who in range(0, len(self.set_of_keys)):
            for k in self.set_of_keys[who]:
                if k not in all_keys:
                    all_keys.append(k)
        # corpus names
        for j in range(0, len(self.set_of_names)):
            ws.write(j + 1, 0, self.set_of_names[j], xlwt.easyxf('font: bold on;'))
        # values
        for i in range(0, len(all_keys)):
            ws.write(0, i + 1, all_keys[i], xlwt.easyxf('font: bold on;'))
            for j in range(0, len(self.set_of_keys)):
                k = all_keys[i]
                if k in self.set_of_keys[j]:
                    ws.write(j + 1, i + 1, self.set_of_keys[j][k])
                else:
                    ws.write(j + 1, i + 1, 0)
        #for i in range(0, len(self.set_of_keys)):
        #    ws.col(1 + i).width = 256 * 30
        # corpus pour ligne
        # indice en colonne
        # pb des keys !!! tous n'ont pas les mêmes
        #for who in range(0, len(self.set_of_keys)):
        #    row = 0
        #    for key, val in self.set_of_keys[who].items():
        #        if who == 0:
        #            ws.write(row, 0, key, xlwt.easyxf('font: bold on;'))
        #        ws.write(row, who + 1, val)
        #        row += 1
        wb.save(filename)

    def ouput_all(self, name):
        self.output_html(name + '.html')
        self.output_excel(name + '.xls')

if __name__ == '__main__':
    # only one set of keys
    p = Presentation('templates/maquette.html')
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
    p.output_html('results/results1.html')
    p.output_excel('results/results1.xls')
    # two set of keys
    p = Presentation('templates/maquette.html')
    p.populate(dummy, 0)
    dummy2 = {
        'GEN_TITLE' : 'Titre 2',
        'GEN_URL' : 'http://www.toto.com',
        'SURF_WORD_LENGTH' : 24,
        'GEN_NOTE' : 'Mauvais',
        'META_NB_LINKS' : 1,
        'META_NB_PICTURES' : 0,
        'META_NB_SECTION' : 24,
        'META_NB_PARAGRAPH' : 2,
        'SURF_AVG_WORD_LENGTH' : 3,
        'SURF_FLESCH_KINCAID' : 0,
        'SYN_RES1' : 12,
        }
    p.populate(dummy2, 1)
    p.ouput_all('results/results2') # don't but html or xls at the end
