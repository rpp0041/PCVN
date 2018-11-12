import scholarly # Non official Api for Google Scholar
import codecs

authorInput= input('Nombre del Autor: ')

search_query = scholarly.search_author('Cesar Garcia-Osorio')
author = next(search_query).fill()
author_pub = author.publications

pubs={}							# Dict where we have Title´s publication and number of cites
for i in author_pub:
    title=i.bib['title']
    if hasattr(i,'citedby'):    # Check it has or not citations , in case it has, it will be add to the list
        citations=i.citedby
    else:
        citations=0
    pubs[title]=citations

# Write information retrieved to txt file
file=codecs.open('testfile.txt','w',"utf8")
for i in pubs.items():
    file.write(i[0]+' , '+str(i[1]))
file.close()