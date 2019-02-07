import urllib.request

name = 'Naumachie' #None

if name is None:
    name = input('Enter the name of the page (without http):')

url = "https://fr.vikidia.org/wiki/" + name

response = urllib.request.urlopen(url)
html_doc = response.read()

from bs4 import BeautifulSoup, Comment
soup = BeautifulSoup(html_doc, 'html.parser')
part = soup.find("div", {"id" : "mw-content-text"})

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
