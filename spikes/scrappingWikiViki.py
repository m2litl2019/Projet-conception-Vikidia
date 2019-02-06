#Ne fonctionne pas pour certains articles Wikipédia possédant des sous-titres comme des propositions d'articles homonymes => https://fr.wikipedia.org/wiki/Maus 

#------------------------------------------------------------
# Import
#------------------------------------------------------------

import urllib.request
import sys
from bs4 import BeautifulSoup, Comment

#------------------------------------------------------------
# Switches
#------------------------------------------------------------

WRITE_TARGET_LIST_TO_DISK = False
LOAD_TARGET_LIST_FROM_DISK = True

#------------------------------------------------------------
# Make a list of targets
#------------------------------------------------------------

urls = [] # all targets to scrap
def list_targets(seed="/w/index.php?title=Sp%C3%A9cial:Toutes_les_pages", info=False):
    old_size = len(urls)
    if info:
        print('Len =', old_size, 'Going to :', "https://fr.vikidia.org" + seed + "&hideredirects=1")
    req = urllib.request.Request(
        "https://fr.vikidia.org" + seed + "&hideredirects=1",
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    response = urllib.request.urlopen(req)
    
    soup = BeautifulSoup(response.read(), 'html.parser')
    next_target = None
    try:
        part = soup.findAll("a", {"title" : 'Spécial:Toutes les pages'})
        if len(part) == 1:
            next_target = part["href"]
        else:
            next_target = part[1]["href"]
        print(next_target)
    except:
        print("No next")
    
    for link in soup.findAll('a'):
        if link.has_attr("href") and link["href"].startswith("/wiki/") \
           and not link["href"].startswith("/wiki/Vikidia:") \
           and not link["href"].startswith("/wiki/Sp%C3%A9cial:") \
           and not link["href"].startswith("/wiki/Portail:") \
           and not link["href"].startswith("/wiki/Aide:"):
            url = link["href"]
            if url not in urls:
                urls.append(url)
    if next_target is not None and old_size != len(urls):
        list_targets(next_target)

#------------------------------------------------------------
# Scrap targets
#------------------------------------------------------------

failed_vikidia = 0
failed_wikipedia = 0
def process_target_both(name, output):
    global failed_vikidia
    global failed_wikipedia
    try:
        process_target(name, "https://fr.vikidia.org/wiki/"+ name, 'vikidia', output=output)
    except:
        print('Impossible to get', name, 'for vikidia.')
        failed_vikidia += 1
    try:
        process_target(name, "https://fr.wikipedia.org/wiki/" + name, 'wikipedia', output=output)
    except:
        print('Impossible to get', name, 'for wikipedia.')
        failed_wikipedia += 1

def process_target(target, url, suffix, display=False, output=False):

    req = urllib.request.Request(
        url,
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    response = urllib.request.urlopen(req)
    #print(f.read().decode('utf-8'))

    #response = urllib.request.urlopen(url)
    html_doc = response.read()
    #print(html_doc)

    soup = BeautifulSoup(html_doc, 'html.parser')
    part = soup.find("div", {"id" : "mw-content-text"}) 

    #for div in part.findAll("div"): 
    #    div.decompose()

    for center in part.findAll("center"):
        center.decompose()

    for table in part.findAll("table"):
        table.decompose()

    for child in part.children:
        if isinstance(child, Comment):
            child.extract()

    def replace_by_text(part, tag):
        for child in part.findAll(tag):
            child.insert_before(child.text)
            child.decompose()
        return part

    replace_by_text(part, "a")
    replace_by_text(part, "b")
    replace_by_text(part, "i")
    replace_by_text(part, "strong")
    replace_by_text(part, "em")
    replace_by_text(part, "u")

    text = ''
    for child in part.findAll("p"):
        text += child.text

    if display:
        print(text)
    if output:
        if suffix == 'wikipedia': # if "https://fr.wikipedia.org" in url:
            f = open('wikipedia/' + target + '_' + suffix + '.txt', mode='w', encoding='utf8')
        else:
            f = open('vikidia/' + target + '_' + suffix + '.txt', mode='w', encoding='utf8')
        #f = open(target + '_' + suffix + '.txt', mode='w', encoding='utf8')
        f.write(text)
        f.close()

if __name__ == '__main__':
    if WRITE_TARGET_LIST_TO_DISK:
        f = open('targets.txt', encoding='utf8', mode='w')
        for t in urls: # 52127
            f.write(t + "\n")
        f.close()
    elif LOAD_TARGET_LIST_FROM_DISK:
        urls = open('targets.txt', encoding='utf8', mode='r').readlines()
    else:
        raise Exception("A target list has not been defined. Scrap it from the web or provide a file named targets.txt.")
    
    #target = "AZERTY"
    #process_target_both(target, output=True)
    #article = ["Belgique"]
    #article=["%C3%89checs","%C3%89l%C3%A9phant","Australie","Belgique ","Boulangerie","Caracal","Catherine_II_de_Russie","Ch%C3%A8vre","Chat","Cheval","Chien","Com%C3%A8te","D%C3%B4me_du_Rocher","Geyser","Homme_au_masque_de_fer","Ich_bin_ein_Berliner","Kurdistan","Indira_Gandhi","Kylian_Mbapp%C3%A9","L%C3%A9gionelle","L%C3%A9onard_de_Vinci","La_Ferme_des_animaux","Le_Lotus_bleu","Lille","Lyon","Marl%C3%A8ne_Dietrich","Massif_central","Mode_(habillement)","Monstre_de_Gila","Mosqu%C3%A9e","Napol%C3%A9on_Ier","Navette_spatiale_Bourane","Op%C3%A9ra_Garnier","Otto_Dix","Paris","Poivre","Portugal","Pyr%C3%A9n%C3%A9es","Rome","Rubik%27s_Cube","Saturn_V","Tyrannosaurus_rex","Vienne_(Is%C3%A8re)","Volcan"]
    #for target in article:
    restart_at = 'Tripoli_(Lybie)' #'TF1_games' #'BZRK'
    for vikidia in urls:
        target = vikidia.replace('/wiki/', '').strip()
        if restart_at is not None:
            if target == restart_at: restart_at = None
            else: continue
        process_target_both(target, output=True)
    print('Wikipedia failed:', failed_wikipedia)
    print('Vikidia failed:', failed_vikidia)
