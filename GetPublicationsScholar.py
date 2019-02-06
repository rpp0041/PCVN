""" Needed libraries to extract and write the data
Scholarly : Is a non Official API to extract data from Google Scholar 
bibtexparser: Is a library that allow to work with BibTex format file """
import scholarly
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

""" Function that will return Abstract field parsed, without some
html tags that in same cases the API return
input : string
return : string 
"""


def parse_abstract(abstract):
    if type(abstract) not in [str]:
        raise TypeError('Abstract must be an str')
    # split in "gsh_csp" html tags to be removed
    abstract = abstract.split('class="gsh_csp">')
    # if len of abstract list split is less that 2, indicates that there are no "gsh_csp" tags
    if len(abstract) < 2:
        # split in "gsh_vcd_descr" html tags to be removed
        abstract = abstract[0].split('class="gsh_small">')
        # if len of abstract list split is less that 2, indicates that there are no "gsh_small" tags
        if len(abstract) < 2:
            abstract = abstract[0].split('"gsc_vcd_descr">')
            # if len of abstract list split is less that 2, indicates that there are no "gsh_vcd_descr" tags
            if len(abstract) < 2:
                abstract = abstract[0]
            else:
                abstract = abstract[1]
        else:

            abstract = abstract[1]
    else:
        abstract = abstract[1]
    # Remove "</div>" tag
    abstract = abstract.split('</div>')[0]
    return abstract


""" Function that will search for publications made by the author given as a parameter an will save the results in a 
BibTex file
input : author (string)
        pbar   (tkinter progressbar) 
        
return : BibTex file
"""


def get_publications_scholar(author_input, pbar, label_var, max):
    """  Call to scholarly functions that will search for the author given
    as a parameter and will return an iterable object with all the 
    publications found for the author given"""
    search_query = scholarly.search_author(author_input)
    author = next(search_query).fill()
    # Iterable object that contains all user publications
    author_pub = author.publications
    # BibTex database for write data to BibTex File
    db = BibDatabase()
    # Counter that indicates ID in BibDatabase
    cont = 0
    if max == 10000:
        max = len(author_pub)
    """ update progress bar GUI"""
    progress_bar_inc = 100 / max
    # BibTex writer object
    writer = BibTexWriter()

    """ Go thought all the author´s publications , complete all the fields
    and parse some in order to fit BibTexWriter"""
    for pub in author_pub:
        # Set max of publications
        if cont >= max:
            break
        # fill all fields possible of that publication
        pub.fill()
        """ Need modifications for BibTextWriter 
        if has journal field , it indicates that it is an articule
        otherwise it is a book"""
        if 'journal' in pub.bib.keys():
            pub.bib['ENTRYTYPE'] = 'article'
        else:
            pub.bib['ENTRYTYPE'] = 'book'
        # set counter as Pub ID
        pub.bib['ID'] = str(cont)
        # parse abstract field
        if 'abstract' in pub.bib.keys():
            # Parse abstract field to string
            abstract = str(pub.bib['abstract'])
            abstract = parse_abstract(abstract)
            pub.bib['abstract'] = abstract
        # parse year to string
        if 'year' in pub.bib.keys():
            pub.bib['year'] = str(pub.bib['year'])
        # set number of Cites , it has no attribute "citedBy" it has NO cites so it set as 0
        if hasattr(pub, 'citedby'):
            pub.bib['cites'] = str(pub.citedby)
        else:
            pub.bib['cites'] = '0'
        # add publication to database
        db.entries.append(pub.bib)
        cont += 1
        """ update progress bar GUI"""
        pbar['value'] += progress_bar_inc
        pbar.update()
        label_var.set('Número de publicaciones obtenidas:\n'+str(cont)+'/'+str(max))
    """ Write the extracted data stored in db (BibDatabase) and save it 
    in bibtexScholar.bib for later use """
    with open('bibtexScholar.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
