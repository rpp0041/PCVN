from pyscopus import Scopus # Import library that will help us in the search
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def GetAU(id): # Function that will parse author id into real name.
    string=''
    lg=len(author_pub['author'][id])
    for i in range(0,lg-1):
        query = 'au-id(%s)'%author_pub['author'][id][i]
        a=scopus.search_author(query,10)
        string+=(a['name'][0])
        string+=' and '
    query = 'au-id(%s)'%author_pub['author'][id][lg-1]
    a=scopus.search_author(query,10)
    string+=(a['name'][0])
    return string
   
key ='a3ddc2b8df64bc16774266fb842c0365' # Key gived by Elsevier to acces their api 
scopus = Scopus(key)

author_id= input('ID del Autor: ')   # We ask the user to enter the author´s ID

author_pub= scopus.search_author_publication(author_id,10000) # int number indicates the number of publications to be retrieved (set by default in 10000)
															  # (pending of improve)


############################################################################
# Modifications on Internal data structure to fit with Bibtex Structure
author_pub['pages']=author_pub['page_range']
author_pub.pop('page_range')

author_pub['author']=author_pub['authors']
author_pub.pop('authors')

author_pub['ID']=author_pub['scopus_id']
author_pub.pop('scopus_id')

author_pub['ENTRYTYPE']=author_pub['subtype_description']
author_pub.pop('subtype_description')

author_pub['url']=author_pub['full_text']
author_pub.pop('full_text')

listOfKeys=list(author_pub.keys())
listOfKeys.remove('author')
listOfKeys.remove('citation_count')
listOfKeys.remove('cover_date')
listOfKeys.remove('publication_name')
############################################################################

db = BibDatabase()
numPub=len(author_pub['title']) # Number of Publications retrieved
writer = BibTexWriter()


for i in range(0,numPub):
    bib=dict()
    bib['author']=GetAU(i)
    bib['citation_count']=str(author_pub['citation_count'][i])
    bib['cover_date']= author_pub['cover_date'][i].split('-')[0]
    for x in listOfKeys:
        if author_pub[x][i] is not None:
            if x is 'affiliation':
                bib['affiliation']=author_pub['affiliation'][i][0]['name']
            else:
                if x is 'aggregation_type':
                    if author_pub[x][i]== 'Journal':
                        bib['journal']=author_pub['publication_name'][i]
                        author_pub['ENTRYTYPE'][i]=author_pub['ENTRYTYPE'][i].split(' ')[0]
                    else:
                        author_pub['ENTRYTYPE'][i]=author_pub[x][i].split(' ')[0]
                else:
                    bib[x]=author_pub[x][i]
    db.entries=[bib]

    with open('bibtexScopus.bib', 'a' , encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))