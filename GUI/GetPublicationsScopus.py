""" Needed libraries to extract and write the data
pyscopus : Is a non Official API to extract data from Scopus 
bibtexparser: Is a library that allow to work with BibTex format file """
from pyscopus import Scopus
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

""" Function that recived an int as a parameter , corresponding to the
current position of the publications, and will return the author´s
name in an apropiate BibTex format 
----------------------------------------------------------------------
author_pub[id] : list of ID (each id corresponds an author
query : str (correspond to Scopus query Style)

Returns : String (Author´s name in BibTex format)
----------------------------------------------------------------------
"""


def GetAU(id,author_pub,scopus): 
    string = ''
    lg = len(author_pub['author'][id])

    for i in range(0, lg-1):
        query = 'au-id(%s)' % author_pub['author'][id][i]
        a = scopus.search_author(query, 10)
        string += (a['name'][0])
        string += ' and '
    """ In the last one we don´t want have 'and' behind author´s name 
    so we convert ID in real name separtly"""
    query = 'au-id(%s)' % author_pub['author'][id][lg-1]
    a = scopus.search_author(query, 10)
    string += (a['name'][0])
    return string

def GetPublicationsScopus(author_id,pbar):
    """ Key gived by Elsevier to acces their api """
    key = 'a3ddc2b8df64bc16774266fb842c0365'
    scopus = Scopus(key)

    """ We ask the user to enter the author´s ID """
    #author_id = input('ID del Autor: ')

    """ int number indicates the number of publications to be retrieved
    (set by default in 10000) """
    author_pub = scopus.search_author_publication(author_id, 10000)
    """ Modifications on Internal data structure to fit with Bibtex Structure 
    ----------------------------------------------------------------------
    page_range : will be rename as pages
    authors : will be rename as atuhor
    scopus_id: will be rename as ID
    subtype_description : will be rename as ENTRYTYPE
    full_text: will be rename as url

    additionally some other keys will be removed to be added separately
    in write process
    """

    author_pub['pages'] = author_pub['page_range']
    author_pub.pop('page_range')

    author_pub['author'] = author_pub['authors']
    author_pub.pop('authors')

    author_pub['ID'] = author_pub['scopus_id']
    author_pub.pop('scopus_id')

    author_pub['ENTRYTYPE'] = author_pub['subtype_description']
    author_pub.pop('subtype_description')

    author_pub['url'] = author_pub['full_text']
    author_pub.pop('full_text')

    listOfKeys = list(author_pub.keys())
    listOfKeys.remove('author')
    listOfKeys.remove('citation_count')
    listOfKeys.remove('cover_date')
    listOfKeys.remove('publication_name')
    """
    ----------------------------------------------------------------------
    """

    db = BibDatabase()

    """ Number of Publications retrieved """
    numPub = len(author_pub['title'])
    progressbarInc=90/numPub
    writer = BibTexWriter()

    """ Go through all the publications creating a dict with all the 
    fields corresponding """
    for i in range(0, numPub):
        bib = dict()
        """ parse ID to real author name"""
        bib['author'] = GetAU(i,author_pub,scopus)
        """ parse number of cites to str"""
        bib['citation_count'] = str(author_pub['citation_count'][i])
        """ parse date to get only the year"""
        bib['year'] = author_pub['cover_date'][i].split('-')[0]
        """ Go through all the keys in the dict """
        for x in listOfKeys:
            if author_pub[x][i] is not None:
                """ parse affiliation field to get only the affiliation name"""
                if x is 'affiliation':
                    bib['affiliation'] = author_pub['affiliation'][i][0]['name']
                else:
                    """ In case aggregation_type is a journal 
                    we will add a new field with the title of the journal publication
                    Otherwhise we will parse ENTRYTYPE to fit BibTex standard ,
                    selecting only the first word of the whole field """
                    if x is 'aggregation_type':
                        if author_pub[x][i] == 'Journal':
                            bib['journal'] = author_pub['publication_name'][i]
                            author_pub['ENTRYTYPE'][i] = author_pub['ENTRYTYPE'][i].split(' ')[
                                0]
                        else:
                            author_pub['ENTRYTYPE'][i] = author_pub[x][i].split(' ')[
                                0]
                    else:
                        bib[x] = author_pub[x][i]

        """ update progress bar """    
        pbar['value'] += progressbarInc
        pbar.update()
        db.entries.append(bib)
    """ Write the extracted data stored in db (BibDatabase) and save it 
    in bibtexScopus.bib for later use """
    with open('bibtexScopus.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))