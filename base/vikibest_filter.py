import bs4
import os

def replace_by_text(part, tag):
    for child in part.findAll(tag):
        try:
            child.insert_before(child.text)
        except ValueError as ve:
            pass #print(child)
        child.decompose()

# Bug:
# div class="mw-references-wrap" => not deleted in Chien
# chat des sables => nothing produced
# ferme des animaux => nothing produced
# texte après le dernier </p>
# img not deleted
# Monstre de gila => texte avant le premier <p>
# <p></p> (paragraphe vide)
# Tyrannosaure_vikidia.txt => img dans une ligne dont il faut conserver la fin !
nb = 0
for filename in os.listdir('vikibest'):
    html_doc = open('vikibest_html' + os.sep + filename, mode='rb')
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    part = soup.find("div", {"id" : "mw-content-text"})
    for child in part.children:
        if isinstance(child, bs4.Comment):
            child.extract()
    for table in part.findAll("table"):
        table.decompose()
    toc = part.find("div", {"id" : "toc"})
    if toc is not None:
        toc.decompose()
    sup = part.find("div")
    if sup is not None:
        sup.decompose()
    ref = part.find("div", {"class" : "mw-references-wrap"}) # not deleted in Chien
    if ref is not None:
        ref.decompose()
    for center in part.findAll("center"):
        center.decompose()
    for img in part.findAll("div", {"style" : "margin-bottom: 5px; text-indent: 30px;"}):
        img.decompose()
    for gal in part.findAll("ul", {"class" : "gallery mw-gallery-packed"}):
        gal.decompose()
    for sup in part.findAll("sup"):
        sup.decompose()
    for small in part.findAll("small"):
        small.decompose()
    replace_by_text(part, "span")
    replace_by_text(part, "a")
    replace_by_text(part, "b")
    replace_by_text(part, "i")
    replace_by_text(part, "strong")
    replace_by_text(part, "em")
    replace_by_text(part, "u")
    decompose = False
    for child in part.children:
        if child.name == 'div' and 'class' in child.attrs and child.attrs['class'][0].startswith('thumb'):
            child.decompose()
        elif child.name == 'img': # never deleted
            child.decompose()
        elif child.name == 'h2' and child.text.startswith('Voir aussi'):
            child.decompose()
            decompose = True
        elif decompose:
            try:
                child.decompose()
            except AttributeError:
                pass
    txt = str(part)
    txt = txt.replace('δ', '')
    txt = txt.replace('[modifier | modifier le wikicode]', '')
    txt = txt.replace('\n\n', '')
    txt = txt.replace('<div style="clear:both;"></div>', '')
    txt = txt.replace('<div class="mw-content-ltr" dir="ltr" id="mw-content-text" lang="fr">', '')
    txt = txt.replace('><', '>\n<')
    txt = txt.replace('<p>', '<p>\n')
    txt = txt.replace('<h2>', '<h2>\n')
    txt = txt.replace('<h3>', '<h3>\n')
    txt = txt.replace('<h4>', '<h4>\n')
    txt = txt.replace('</h2>', '\n</h2>\n')
    txt = txt.replace('</h3>', '\n</h3>\n')
    txt = txt.replace('</h4>', '\n</h4>\n')
    txt = txt.replace('<ul>', '')
    txt = txt.replace('</ul>', '')
    txt = txt.replace('<ol>', '')
    txt = txt.replace('</ol>', '')
    txt = txt.replace('<li>', '<p>\n')
    txt = txt.replace('</li>', '\n</p>')
    txt = txt.replace('<dl>', '')
    txt = txt.replace('</dl>', '')
    txt = txt.replace('<dt>', '<p>\n')
    txt = txt.replace('</dt>', '\n</p>')
    txt = txt.replace('<dd>', '<p>\n')
    txt = txt.replace('</dd>', '\n</p>')
    txt = txt.replace('</p>\n</p>', '</p>\n')
    txt = txt.replace('</div>', '')
    txt = txt.replace('<div class="center">', '')
    txt = txt.replace('<div class="toc_niveau_2" style=";">', '') # Otto Dix
    txt = txt.replace('<div class="magnify">', '<p>\n')
    txt = txt.replace('<br/>', '')
    txt = txt.replace('<br>', '')
    final_txt = ''
    lines = txt.split('\n')
    prev = None
    p_open = False
    for lin in lines:
        lin = lin.strip()
        if len(lin) > 0:
            if lin.startswith('<img '):
                continue
            if lin.startswith('<div class="thumb'):
                continue
            if lin.startswith('<div style="'):
                continue
            if lin.startswith('<div align="'):
                continue
            if lin.startswith('<div class="NavEnd">'):
                continue

            if lin in ['<p>', '<h2>', '<h3>', '<h4>']:
                if p_open == True:
                    final_txt += '</p>\n'
                if lin == '<p>':
                    p_open = True
                else:
                    p_open = False
            elif lin == '</p>':
                p_open = False
            
            if prev is None:
                final_txt += lin + '\n'
            elif prev == '</p>' and lin == '</p>':
                pass
            else:
                final_txt += lin + '\n'
            prev = lin
    txt = final_txt
    #print(txt)
    f = open('vikibest_div' + os.sep + filename, mode='w', encoding='utf8')
    f.write(txt)
    f.close()
    nb += 1
    print(nb)

