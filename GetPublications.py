import scholarly # Non official Api for Google Scholar
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def ParseAbstract(i):
    abstract=str(i.bib['abstract'])
    abstract=abstract.split('class="gsh_csp">')
    if len(abstract)<2:
        abstract=abstract[0].split('class="gsh_small">')
        if len(abstract)<2:
            abstract=abstract[0].split('"gsc_vcd_descr">')[1]
        else:
            abstract=abstract[1]
    else:
        abstract=abstract[1]
    abstract=abstract.split('</div>')[0]
    return abstract


authorInput= input('Nombre del Autor: ')

search_query = scholarly.search_author(authorInput)
author = next(search_query).fill()
author_pub = author.publications

db = BibDatabase()

cont =0
writer = BibTexWriter()
for i in author_pub:
    i.fill()
    ## Need modifications for BibTextWriter 
    if 'journal' in i.bib.keys():
        i.bib['ENTRYTYPE']='article'
    else: 
        i.bib['ENTRYTYPE']='book'
    i.bib['ID']=str(cont)
    if 'abstract' in i.bib.keys():
        abstract=ParseAbstract(i)
        i.bib['abstract']=abstract
    if 'year' in i.bib.keys():
        i.bib['year']=str(i.bib['year'])
    db.entries=[i.bib]
    cont+=1
    with open('bibtex.bib', 'a' , encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
    