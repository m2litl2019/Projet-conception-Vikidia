from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
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
    print(str(bsObj.find("div", {"id": "bodyContent"})))
    #print(bsObj.find("div", {"id": "bodyContent"}).get_text()) ## pour n'avoir que le texte
    print("</article>")
    return bsObj.find("div", {"id" : "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
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
