""" Needed libraries to extract and write the data
Scholarly : Is a non Official API to extract data from Google Scholar 
bibtexparser: Is a library that allow to work with BibTex format file """
import scholarly
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

""" Function that will return Abstract field parsed, without some
html tags that in same cases the API return"""


def parse_abstract(i):
    abstract = str(i.bib['abstract'])
    abstract = abstract.split('class="gsh_csp">')
    if len(abstract) < 2:
        abstract = abstract[0].split('class="gsh_small">')
        if len(abstract) < 2:
            abstract = abstract[0].split('"gsc_vcd_descr">')[1]
        else:
            abstract = abstract[1]
    else:
        abstract = abstract[1]
    abstract = abstract.split('</div>')[0]
    return abstract


def get_publications_scholar(author_input, pbar):
    """ Ask the user to input the name of the author to search for"""

    """  Call to scholarly functions that will search for the author given 
    as a parameter and will return an iterable object with all the 
    publications found for the author given"""
    search_query = scholarly.search_author(author_input)
    author = next(search_query).fill()
    author_pub = author.publications

    db = BibDatabase()

    cont = 0
    progress_bar_inc = 100 / len(author_pub)
    writer = BibTexWriter()
    """ Go trought all the author´s publications , complete all the fields
    and parse some in order to fit BibTexWriter"""
    for i in author_pub:
        i.fill()
        """ Need modifications for BibTextWriter """
        if 'journal' in i.bib.keys():
            i.bib['ENTRYTYPE'] = 'article'
        else:
            i.bib['ENTRYTYPE'] = 'book'
        i.bib['ID'] = str(cont)
        if 'abstract' in i.bib.keys():
            abstract = parse_abstract(i)
            i.bib['abstract'] = abstract
        if 'year' in i.bib.keys():
            i.bib['year'] = str(i.bib['year'])
        if hasattr(i, 'citedby'):
            i.bib['cites'] = str(i.citedby)
        else:
            i.bib['cites'] = '0'
        db.entries.append(i.bib)
        cont += 1
        pbar['value'] += progress_bar_inc
        pbar.update()

    """ Write the extracted data stored in db (BibDatabase) and save it 
    in bibtexScholar.bib for later use """
    with open('bibtexScholar.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
