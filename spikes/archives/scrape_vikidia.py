from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, Comment
import copy
import re
import datetime
import random


""" constitution du corpus : articles a simplifier, super articles et de l'aléatoire """

random.seed(datetime.datetime.now())
def getLinks(articleUrl,write=""):

	req = Request("https://fr.vikidia.org" + articleUrl, headers={"User-Agent":'Mozilla/5.0'})
	webpage = urlopen(req)
	bsObj = BeautifulSoup(webpage,"lxml")
	if write != "": 
		print("<article title=\"" + articleUrl + '" type=\"' + str(write) +'">')
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
		print("</article>")
		
	# webpage = urlopen(req)
	# bsObj = BeautifulSoup(webpage,"lxml")
	links = bsObj.find("div", {"id" : "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

	return links

#html = urlopen("https://fr.vikidia.org/wiki/Arbre")


if __name__ =="__main__":
	print("<corpus>")
	pages = set()
	links = getLinks("/wiki/Vikidia:Super_article/Promus","")
	for link in links:
		getLinks(link,"super")
    
  
    
    # i = 0
    # links = getLinks("/wiki/Arbre")
    # pages.add("/wiki/Arbre")
    # while len(links) > 0 and i < 2000:
        # newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        # if newArticle not in pages:
            # pages.add(newArticle)
            # links = getLinks(newArticle)
            # i += 1
	print("</corpus>")
	
