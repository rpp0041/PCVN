from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
""" Function than will return the biggest number of 3 given """


def Bigger(num1, num2, num3):
    if num1 > num2:
        if num1 > num3:
            return num1
        else:
            return num3
    else:
        if num2 > num3:
            return num2
        else:
            return num3

# Load BibTex files extract from Google Scholar, Scopus and WOS
# in order to remove duplicate publications and to group them in just one file
# so it will make easier to work with.


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
lenScopus = len(Scopus.entries)
lenScholar = len(Scholar.entries)
lenWos = len(WOS.entries)
lenMax = Bigger(lenScholar, lenScopus, lenWos)

#####################################################################


# Extract all the publications titles to be compared and determinate
# if there are duplicates or not, if we find a publication duplicated
# we will group them combinating the different keys of dicts

listScopus = list()
listScholar = list()
listWos = list()

for i in range(0, lenMax):
    if i < lenScopus:
        listScopus.append(Scopus.entries[i]['title'])
    if i < lenScholar:
        listScholar.append(Scholar.entries[i]['title'])
    if i < lenWos:
        listWos.append(WOS.entries[i]['title'])

cont = 0  # Indicates the current position in listScopus
# Go trought all titles retrieved by Scopus
for title in listScopus:
    if title in listScholar:
        """ If the title is in Google Scholar list then we will obtain
        the currrent position in the list, so we can delete it from 
        the list and also from the dict, we update the keys of Scopus
        with the different ones from Google Scholar"""
        index = listScholar.index(title)
        Scopus.entries[cont].update(Scholar.entries[index])
        Scholar.entries.pop(index)
        listScholar.pop(index)
    if title in listWos:
        """ If the title is in Web of Science list then we will obtain
        the currrent position in the list, so we can delete it from 
        the list and also from the dict, we update the keys of Scopus
        with the different ones from WOS"""
        index = listWos.index(title)
        Scopus.entries[cont].update(WOS.entries[index])
        WOS.entries.pop(index)
        listWos.pop(index)
    cont += 1

cont = 0  # Indicates the current position in  listWosfor title in listWos:
# Go trought all titles retrieved by Web Of Science
for title in listWos:
    if title in listScholar:
        """ If the title is in Google Scholar list then we will obtain
        the currrent position in the list, so we can delete it from 
        the list and also from the dict, we update the keys of WOS
        with the different ones from Google Scholar"""
        index = listScholar.index(title)
        WOS.entries[cont].update(Scholar.entries[index])
        Scholar.entries.pop(index)
        listScholar.pop(index)
    cont += 1

#####################################################################

""" Write the dictionaries modified in a new BibTex file 
 at this point we will not have duplicate publications
  """
writer = BibTexWriter()
db = BibDatabase()
for i in Scopus.entries:
    db.entries.append(i)
for i in Scholar.entries:
    db.entries.append(i)
for i in WOS.entries:
    db.entries.append(i)
with open('BibFINAL.bib', 'a', encoding='utf-8') as bibfile:
    bibfile.write(writer.write(db))
