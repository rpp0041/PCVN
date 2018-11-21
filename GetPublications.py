import scholarly # Non official Api for Google Scholar
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

authorInput= input('Nombre del Autor: ')

search_query = scholarly.search_author(authorInput)
author = next(search_query).fill()
author_pub = author.publications

db = BibDatabase()

cont =0
writer = BibTexWriter()
for i in author_pub	:
	i.fill()

for i in author_pub:
	## Need modifications for BibTextWriter 
    if 'journal' in i.bib.keys():
        i.bib['ENTRYTYPE']='article'
    else: 
        i.bib['ENTRYTYPE']='book'
    i.bib['ID']=str(cont)
    if 'abstract' in i.bib.keys():
        i.bib['abstract']=str(i.bib['abstract'])
    if 'year' in i.bib.keys():
        i.bib['year']=str(i.bib['year'])
    db.entries=[i.bib]
    cont+=1
    with open('bibtex.bib', 'a' , encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))