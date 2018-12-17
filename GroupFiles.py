from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
""" Function that if 2 given publications check if hass issn attribute
and in case both have , check if are equal
parameter : publication (dict)
return : True/False
"""


def checkISSN(pub1, pub2):
    if 'issn' in pub1 and 'issn' in pub2:
        if pub1['issn'] == pub2['issn']:
            return True
    return False


""" Function that if 2 given publications check if  their titles are equal
parameter : publication (dict)
return : True/False
"""


def checkTitle(pub1, pub2):
    if pub1['title'].lower() == pub2['title'].lower():
        return True
    return False


""" Function that given 2 list of publications check if their are the same
in 2 steps first by ISSN (in case both have),second By Title
parameter: list of publications (list of dicts)
return: lists """


def RemoveDupliates(list1, list2):
    for pub in list1:
        for pub2 in list2:
            if checkISSN(pub, pub2):
                """ In case ISSN is the same,update keys from 1st pub"""
                pub.update(pub2)
                list2.remove(pub2)
            elif checkTitle(pub, pub2):
                """ In case title is the same,update keys from 1st pub"""
                pub.update(pub2)
                list2.remove(pub2)
    return list1, list2



""" Function that will parse WOS BibTex file for a correct format.
We need to remove extra '{}' characters , but some fields has not
this extra characters so we exclude them from parse proccess.
parameter: list of publications (list of dicts)"""


def ParseWOS(wos):
    for pub in wos:
        listKeys = list(pub.keys())
        listKeys.remove('author')
        listKeys.remove('ENTRYTYPE')
        listKeys.remove('ID')
        for key in listKeys:
            pub[key] = pub[key].split('{')[1].split('}')[0]


""" Function that will parse Volume field to remove extra information
that produces errors in ANECA application
parameter : publication (dict)
return: publication(dict) """


def ParseVolume(pub):
    if 'volume' in pub.keys():
        pub['volume'] = pub['volume'].split(' ')[0]
    return pub
# Load BibTex files extract from Google Scholar, Scopus and WOS
# in order to remove duplicate publications and to group them in just one file
# so it will make easier to work with.


# Load BibTex files extract from the websites

# Load Google Scholar BibTex File
with open('bibtexScopus.bib', encoding='utf-8') as bibfile:
    Scopus = bibtexparser.load(bibfile)
# Load Scopus BibTex File
with open('bibtexScholar.bib', encoding='utf-8') as bibfile:
    Scholar = bibtexparser.load(bibfile)
# Load WOS BibTex File
with open('savedrecs.bib', encoding='utf-8') as bibfile:
    WOS = bibtexparser.load(bibfile)

""" If WOS had returned more than 50 publications, we will have 2 files,
so we try to read & add to WOS bibtexparser structure to work as if only
one exists """
try:
    with open('savedrecs(1).bib', encoding='utf-8') as bibfile:
        WOS2 = bibtexparser.load(bibfile)
    for x in WOS2.entries:
        WOS.entries.append(x)
except:
    pass

""" Parse WOS db in order to get same format for every bibTex db 
this will help us in the future comparison (otherwise it will be impossible)"""
ParseWOS(WOS.entries)

#####################################################################

""" Remove Duplicates from the BibTex Files"""
WOS.entries, Scopus.entries = RemoveDupliates(WOS.entries, Scopus.entries)
WOS.entries, Scholar.entries = RemoveDupliates(WOS.entries, Scholar.entries)
Scopus.entries, Scholar.entries = RemoveDupliates(
    Scopus.entries, Scholar.entries)


""" Write the dictionaries modified in a new BibTex file 
 at this point we will not have duplicate publications,
 also modify some field´s name to fit BibTex Standard (cites)
 and parse volume field becouse in same cases we get 
 extra information that produces errors in ACADEMIA
"""
writer = BibTexWriter()
db = BibDatabase()
for i in Scopus.entries:
    """ Rename cites"""
    i['cites'] = i['citation_count']
    i.pop('citation_count')
    """ Parse Volume """
    i = ParseVolume(i)
    """ Add pub to write BibTex db """
    db.entries.append(i)
for i in Scholar.entries:
    """ Parse Volume """
    i = ParseVolume(i)
    """ Add pub to write BibTex db """
    db.entries.append(i)
for i in WOS.entries:
    """ Rename cites """
    i['cites'] = i['number-of-cited-references']
    i.pop('number-of-cited-references')
    """ Parse Volume """
    i = ParseVolume(i)
    """ Add pub to write BibTex db """
    db.entries.append(i)
""" Write db to BibTex file """
with open('BibFINAL.bib', 'w', encoding='utf-8') as bibfile:
    bibfile.write(writer.write(db))

