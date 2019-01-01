#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Needed libraries.
Selenium: we will use selenium to navegate through WOS web site
BibTexParser : we will use to read BibTex file
anecaUtils: set of functions to navigate in ACADEMIA
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import bibtexparser
from anecaUtils import *


def aneca(author_input, pbar, user, pswd):
    """ Options for Selenium driver """
    options = Options()
    options.headless = True

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    browser = webdriver.Firefox(options=options, firefox_profile=fp)

    """ Go to Academia application """
    go_to_academia(browser, user, pswd)
    """ Go to add publications Area """
    go_to_publications(browser)

    """ Read data from BibTex file"""
    with open('BibFINAL.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)

    """ BibTex database for uncompleted publications"""
    db_salida = BibDatabase()
    writer = BibTexWriter()
    progress_bar_inc = len(db.entries)/100
    """ Add every publication read from file"""
    for i in db.entries:
        if i['ENTRYTYPE'] == 'book':
            db_salida = fill_new_book(i, browser, author_input, db_salida)
            time.sleep(10)
        elif i['ENTRYTYPE'] == 'article':
            if 'ImpactIndex' in i.keys():
                db_salida = fill_new_index_article(
                    i, browser, author_input, db_salida)
                time.sleep(10)
            else:
                db_salida = fill_new_article(i, browser, author_input, db_salida)
                time.sleep(10)
        elif i['ENTRYTYPE'] == 'inproceedings':
            db_salida = fill_new_inproceedings(
                i, browser, author_input, db_salida)
            time.sleep(10)
        pbar['value'] += progress_bar_inc
        pbar.update()
    """ Write the uncompleted publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('uncompleted_publications.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
