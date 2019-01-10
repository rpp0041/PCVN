#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Needed libraries.
Selenium: we will use selenium to navegate through WOS web site
BibTexParser : we will use to read BibTex file
anecaUtils: set of functions to navigate in ACADEMIA
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import bibtexparser
from anecaUtils import *

""" Function that will login in Academa application and will upload all read information to it
 parameter : author name    (string) 
             pbar           (tkinter progressbar)
             user           (string)
             password       (string)
             
return : Nothing
"""


def aneca(author_input, pbar, user, pswd):
    """ Options for Selenium driver """
    options = Options()
    # set options of driver to be invisible for user (headless)
    options.headless = True
    # set driver browser as Firefox
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    # initialize driver with options
    browser = webdriver.Firefox(options=options, firefox_profile=fp)

    """ Go to Academia application, if login is not ok , function will return True so GUI can ask for login again"""
    if go_to_academia(browser, user, pswd):
        browser.close()
        return True

    """ Go to add publications Area """
    go_to_publications(browser)

    """ Read data from BibTex file"""
    with open('BibFINAL.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)

    """ BibTex database for uncompleted publications"""
    db_salida = BibDatabase()
    # BibTex file writer object
    writer = BibTexWriter()
    """ update progress bar GUI"""
    progress_bar_inc = len(db.entries) / 100

    """ Add every publication read from file"""
    for i in db.entries:
        if i['ENTRYTYPE'] == 'book':
            db_salida = fill_new_book(i, browser, author_input, db_salida)
            """ Wait publication to ve saved"""
            element = WebDriverWait(browser, 20).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "#nuevaPublicacionIdxId")))
        elif i['ENTRYTYPE'] == 'article':
            if 'impactindex' in i.keys():
                db_salida = fill_new_index_article(
                    i, browser, author_input, db_salida)
                """ Wait publication to ve saved"""
                element = WebDriverWait(browser, 20).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, "#nuevLibroCapituloId")))
                time.sleep(1)
            else:
                db_salida = fill_new_article(i, browser, author_input, db_salida)
                """ Wait publication to ve saved"""
                element = WebDriverWait(browser, 20).until(
                    ec.element_to_be_clickable((By.CSS_SELECTOR, "#nuevaConferenciaSeminarioId")))
        elif i['ENTRYTYPE'] == 'inproceedings':
            db_salida = fill_new_inproceedings(
                i, browser, db_salida)
            """ Wait publication to ve saved"""
            element = WebDriverWait(browser, 20).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, "#nuevaPublicacionIdxId")))
        pbar['value'] += progress_bar_inc
        pbar.update()
    browser.close()
    """ Write the uncompleted publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('uncompleted_publications.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
