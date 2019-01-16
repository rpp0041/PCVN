#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Needed libraries.
Selenium: we will use selenium to navegate through WOS web site
BibTexParser : we will use to read BibTex file
anecaUtils: set of functions to navigate in ACADEMIA
"""

from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import bibtexparser
from aneca_utils import *

""" Function that will login in Academa application and will upload all read information to it
 parameter : author name    (string) 
             pbar           (tkinter progressbar)
             user           (string)
             password       (string)
             
return : Nothing
"""


def aneca(author_input, pbar, user, pswd):

    """ Read data from BibTex file"""
    with open('BibFINAL.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)

    """ BibTex database for uncompleted publications"""
    db_salida = BibDatabase()
    # BibTex file writer object
    writer = BibTexWriter()
    """ update progress bar GUI"""
    pbar_inc = len(db.entries) / 100

    idx_article = list()
    no_idx_article = list()
    book = list()
    inproceedings = list()

    for i in db.entries:
        if i['ENTRYTYPE'] == 'book':
            book.append(i)
        elif i['ENTRYTYPE'] == 'article':
            if 'impactindex' in i.keys():
                # Article with quality index
                idx_article.append(i)
            else:
                # Article with NO quality index
                no_idx_article.append(i)
        elif i['ENTRYTYPE'] == 'inproceedings':
            inproceedings.append(i)

    se = login(user, pswd)
    if se is True:
        return True
    se2, new_url, other_url = redirect(se)
    se2, d, headers, final_url = acces_publication_area(se2, new_url, other_url)

    se2, d = add_no_idx(se2, d, headers, final_url, no_idx_article, author_input, db_salida, pbar, pbar_inc)
    se2, d = add_book(se2, d, headers, final_url, book, author_input, db_salida, pbar, pbar_inc)
    se2, d = add_idx(se2, d, headers, final_url, idx_article, author_input, db_salida, pbar, pbar_inc)
    se2, d = add_inprocedings(se2, d, headers, final_url, inproceedings, db_salida, pbar, pbar_inc)

    """ Write the uncompleted publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('uncompleted_publications.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db_salida))
