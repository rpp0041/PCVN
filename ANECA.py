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


def aneca(author_input, pbar, user, pswd, num_var, total, failed):

    """ Read data from BibTex file"""
    with open('todas.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)

    """ BibTex database for uncompleted publications"""
    db_salida = BibDatabase()
    """ BibTex database for completed publications"""
    db_completa = BibDatabase()
    # BibTex file writer object
    writer = BibTexWriter()
    """ update progress bar GUI"""
    pbar_inc = 100/len(db.entries)

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
        total = failed = True
        return total, failed
    se2, new_url, partial_url = redirect(se)
    se2, get_response, headers, final_url = acces_publication_area(se2, new_url, partial_url)

    se2, get_response = add_no_idx(se2, get_response, headers, final_url, no_idx_article, author_input, db_salida, db_completa, pbar, pbar_inc, num_var)
    se2, get_response = add_book(se2, get_response, headers, final_url, book, author_input, db_salida, db_completa, pbar, pbar_inc, num_var)
    se2, get_response = add_idx(se2, get_response, headers, final_url, idx_article, author_input, db_salida, db_completa, pbar, pbar_inc, num_var)
    se2, get_response = add_inprocedings(se2, get_response, headers, final_url, inproceedings, db_salida, db_completa, pbar, pbar_inc, num_var)

    """ Write the uncompleted publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('pendientes.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db_salida))

    """ Write the completed publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('subidas.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db_completa))
    total = len(db.entries)
    failed = len(db_salida.entries)

    return total, failed
