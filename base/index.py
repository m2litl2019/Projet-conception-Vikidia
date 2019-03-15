import cgi 
import datetime
import copy

from scrappingWikiViki import process_target
from presentation import Presentation
from texteval import Part, Sentence, send

from reperage_passive import reperage_passive
from reperage_pronoms import reperage_pronoms
from reperage_verbeconj_prorel_sub import reperage_verbeconj_prorel_sub
from reperage_tpsV import reperage_tps
from indices_html import reperage_images_liens_viki, reperage_ponctuation
from reperage_def_con import reperage_connecteurs_flesch, reperage_definition
from lexique import extract_lemmas, compare_Manulex, compute_polysemy_index

form = cgi.FieldStorage()
print("Content-type: text/html; charset=iso-8859-1\n")

if form.getvalue("name") is not None:
    # Get HTML
    url = form.getvalue("name")
    name = url.split('/')[-1]
    text, html_brut = process_target('vikidia', url, None,
                                     display=False,
                                     output=True,
                                     strip=True,
                                     output_string=True,
                                     get_both=True)
    if text is None:
        text = '<span style="background-color: red; color: white;">Error while retrieving HTML</span>'
    # Build output header
    html = """
    <head>
        <title>Analyse</title>
    </head>
    <body width="100%">
        <h2 id="sum">Summary</h2>
        <ol>
          <li><a href="#text">Text retrieved from page</a></li>
          <li><a href="#tal">Talismane output</a></li>
          <li><a href="#ind">Indices</a></li>
        </ol>
        <h2 id="text">Text retrieved from page</h2>
        <a href="#sum">Back to summary</a><br><br>"""
    # Build Text ouput
    html += '<b><a href="' + url + '">' + url +'</a></b><br><br>'
    html += """<div style="background-color: #EFEFEF; border: 1px solid grey;">"""
    html += text.replace('\u2032', '')
    html += '</div>'
    # Send to Talismane
    part = send(text)
    # Build Talismane output
    html += '<h2 id="tal">Talismane output</h2><a href="#sum">Back to summary</a><br><br><div style="background-color: #EFEFEF; border: 1px solid grey;"><ol>'
    for s in part:
        html += '<li><ol>'
        for w in s:
            html += '<li>' + str(w).replace('\u2032', '') + '</li>'
        html += '</ol></li>'
    html += '</div>'
    # Process Indices
    #p = Part()
    #s = Sentence()
    #for w in words:
    #    if w.pos == 'PONCT' and w.form in ['.', '!', '?']:
    #        p.append(s)
    #        s = Sentence()
    #    else:
    #        s.append(w)
    res = {
        'GEN_TITLE' : name,
        'GEN_URL' : url,
        'GEN_DATE' : str(datetime.datetime.now())
    }
    try:
        # Raw indices
        avg = 0
        nb_ponct = 0
        nb_pt_virg = 0
        nb_dbl_pt = 0
        nb_virg = 0
        nb_all_words = 0
        nb_words = 0
        for s in part:
            avg += len(s)
            for w in s:
                nb_all_words += 1
                if w.pos == 'PONCT':
                    nb_ponct += 1
                    if w.form == ';':
                        nb_pt_virg += 1
                    elif w.form == ':':
                        nb_dbl_pt += 1
                    elif w.form == ',':
                        nb_virg += 1
                else:
                    nb_words += 1
        avg //= len(part)
        res.update({'SUR_WORD_LEN_AVG' : avg,
                    'SUR_PONCTUATION' : nb_ponct,
                    'SUR_AVG_PONCTUATION' : nb_ponct / nb_all_words,
                    'SUR_PONCT_PT_VIRG' : nb_pt_virg,
                    'SUR_AVG_PONCT_PT_VIRG' : nb_pt_virg / nb_all_words,
                    'SUR_PONCT_DBL_PT' : nb_dbl_pt,
                    'SUR_AVG_PONCT_DBL_PT' : nb_dbl_pt / nb_all_words,
                    'SUR_PONCT_VIRG' : nb_virg,
                    'SUR_AVG_PONCT_VIRG' : nb_virg / nb_all_words,
                    })
        # Indices on Talismane output
        res.update(reperage_passive(part))
        res.update(reperage_pronoms(part))
        res.update(reperage_verbeconj_prorel_sub(part))
        res.update(reperage_tps(part))
        res.update(reperage_connecteurs_flesch(part))
        res.update(reperage_definition(part))
        lemmas = extract_lemmas(part)
        res.update(compare_Manulex(lemmas))
        res.update(compute_polysemy_index(part))
        if isinstance(res['SEMLEX_POLY_INDEX'], str):
            res.update({
                'SEMLEX_AVG_MANULEX' : res['SEMLEX_MANULEX'] / nb_words,
                'SEMLEX_AVG_POLY' : res['SEMLEX_POLY_INDEX']
            })
        else:
            res.update({
                'SEMLEX_AVG_MANULEX' : res['SEMLEX_MANULEX'] / nb_words,
                'SEMLEX_AVG_POLY' : res['SEMLEX_POLY_INDEX'] / nb_words
            })
        # Indices on HTML
        res.update(reperage_images_liens_viki(data=html_brut))
        res.update(reperage_ponctuation(data=html_brut))
    except Exception as e:
        html += '<span style="background-color: red; color: white;">Error while calculating Indices</span>'
        raise e
    # Build Indices output
    html += '<h2 id="ind">Indices</h2><a href="#sum">Back to summary</a><br><br><div style="background-color: #EFEFEF; border: 1px solid grey;">'
    p = Presentation('templates/maquette2.html')
    p.populate(res, name='article')
    html += p.output_html_string(header=False)
    html += '</div>'
    # Build output footer
    html += """</div>
    </body>
    </html>
    """
else:
    html = """<!DOCTYPE html>
    <head>
        <title>Analyse article</title>
    </head>
    <body width="100%">
        <center>
            <form action="/index.py" method="post">
                <input type="text" name="name" placeholder="URL de l'article" />
                <input type="submit" name="send" value="Analyser">
            </form>
        </center>
    </body>
    </html>
    """

print(html)
