try:
    import xlwt
except ModuleNotFoundError:
    XLWT = False
else:
    XLWT = True

class Presentation:

    def __init__(self, template):
        f = open(template, mode='r', encoding='utf8')
        self.template = f.read()
        f.close()
        self.keys = {}
    
    def populate(self, dic):
        self.keys.update(dic)

    def output_html(self, filename):
        for key, val in self.keys.items():
            if type(val) == str and val.startswith('http'):
                val = f'<a href="{val}">{val}</a>'
            self.template = self.template.replace(key, str(val))
        f = open(filename, mode='w', encoding='utf8')
        f.write(self.template)
        f.close()

    def output_excel(self, filename):
        if not XLWT: raise Exception('xlwt not installed. Do "pip install xlwt" before.')
        wb = xlwt.Workbook(encoding='utf8')
        ws = wb.add_sheet("Results")
        ws.col(0).width = 256 * 50
        ws.col(1).width = 256 * 30
        row = 0
        for key, val in self.keys.items():
            ws.write(row, 0, key, xlwt.easyxf('font: bold on;'))
            ws.write(row, 1, val)
            row += 1
        wb.save(filename)

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
    p.output_html('results1.html')
    p.output_excel('results1.xls')

