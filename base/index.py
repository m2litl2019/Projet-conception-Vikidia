import cgi 

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
import datetime

form = cgi.FieldStorage()
print("Content-type: text/html; charset=iso-8859-1\n")

if form.getvalue("name") is not None:
    # Get HTML
    url = form.getvalue("name")
    name = url.split('/')[-1]
    content = process_target('vikidia', url, None, display=False, output=True, strip=True, output_string=True)
    if content is None:
        content = '<span style="background-color: red; color: white;">Error while retrieving HTML</span>'
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
    html += content.replace('\u2032', '')
    html += '</div>'
    # Send to Talismane
    part = send(content)
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
        res.update(reperage_passive(part))
        res.update(reperage_pronoms(part))
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
elif False:
    try:  
        res.update(reperage_verbeconj_prorel_sub(WIKIPEDIA+"/"+article.tag))
        res.update(reperage_tps(WIKIPEDIA+"/"+article.tag))
        res.update(reperage_connecteurs_flesch(WIKIPEDIA+"/"+article.tag))
        res.update(reperage_definition(WIKIPEDIA+"/"+article.tag))
        lemmas = extract_lemmas(WIKIPEDIA+"/"+article.tag)
        res.update(compare_Manulex(lemmas))
        res.update(compute_polysemy_index(WIKIPEDIA+"/"+article.tag))
        res.update(reperage_images_liens_viki(article.tag[:-14],"wikipedia"))
        res.update(reperage_ponctuation(article.tag[:-14],"wikipedia"))
    except Exception:
        pass
    finally:
        p.populate(res, i, name=article.tag[:-4])
        html = p.output_html_string(header=False)
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
