import bs4
import bs4.element
import os

#tags = []

for filename in os.listdir('vikibest_html'):
    f = open('vikibest_html' + os.sep + filename, mode='rb')
    soup = bs4.BeautifulSoup(f, 'html.parser')
    part = soup.find("div", {"id" : "mw-content-text"})
    for table in part.findAll("table"):
        table.decompose()
    for child in part.children:
        #if isinstance(child, bs4.element.Tag):
        #    if child.name not in tags:
        #        tags.append(child.name)
        if isinstance(child, bs4.Comment):
            child.extract()
    print(part)
    f.close()
    #print(tags)
    #break
