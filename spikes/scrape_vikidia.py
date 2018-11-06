from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Comment
import copy
import re
import datetime
import random

""" recupere 1000 articles aleatoirement de vikidia et retourne TOUT ce qu'il trouve au format html (option texte seulement mise 
en commentaire meme si elle renvoie des parties du texte pas pertinentes)"""

random.seed(datetime.datetime.now())
def getLinks(articleUrl):

    req = Request("https://fr.vikidia.org" + articleUrl, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    bsObj = BeautifulSoup(webpage,"lxml")
    print("<article title="+articleUrl+'" format=\"html\">')
    #print(str(bsObj.find("div", {"id": "bodyContent"})))
    #print(bsObj.find("div", {"id": "bodyContent"}).get_text()) ## pour n'avoir que le texte
    #print("</article>")

    part = bsObj.find("div", {"id" : "mw-content-text"})

    for div in part.findAll("div"): 
        div.decompose()

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

    print(text)

    webpage = urlopen(req)
    bsObj = BeautifulSoup(webpage,"lxml")
    links = bsObj.find("div", {"id" : "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
    
    return links

#html = urlopen("https://fr.vikidia.org/wiki/Arbre")


if __name__ =="__main__":
    print("<corpus>")
    links = getLinks("/wiki/Arbre")
    pages = set("/wiki/Arbre")
    i = 0
    while len(links) > 0 and i < 1000:
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        if newArticle not in pages:
            pages. add(newArticle)
            links = getLinks(newArticle)
            i += 1

    print("</corpus>")
