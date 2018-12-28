""" Needed libraries.
Selenium: we will use selenium to navegate through WOS web site
Time : we will use it for add delay to code execution
BibTexParser : we will use to read BibTex file
anecaUtils: set of functions to navigate in ACADEMIA
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import time
import bibtexparser
from anecaUtils import *


def aneca(authorInput, pbar, user, pswd):
    """ Options for Selenium driver """
    options = Options()
    options.headless = False

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    browser = webdriver.Firefox(firefox_profile=fp)

    """ Go to Academia application """
    GoToAcademia(browser, user, pswd)
    """ Go to add publications Area """
    GoToPublications(browser)

    """ Read data from BibTex file"""
    with open('BibFINAL.bib', encoding='utf-8') as bibfile:
        db = bibtexparser.load(bibfile)

    """ BibTex database for uncompleted publications"""
    db_salida = BibDatabase()
    progressbarInc = len(db.entries)/100
    """ Add every publication readed from file"""
    for i in db.entries:
        if i['ENTRYTYPE'] == 'book':
            db_salida = fillNewBook(i, browser, authorInput, db_salida)
            time.sleep(10)
        elif i['ENTRYTYPE'] == 'article':
            if 'ImpactIndex' in i.keys():
                db_salida = fillNewIndexArticle(
                    i, browser, authorInput, db_salida)
                time.sleep(10)
            else:
                db_salida = fillNewArticle(i, browser, authorInput, db_salida)
                time.sleep(10)
        elif i['ENTRYTYPE'] == 'inproceedings':
            db_salida = fillNewInproceedings(
                i, browser, authorInput, db_salida)
            time.sleep(10)
        pbar['value'] += progressbarInc
        pbar.update()
    """ Write the uncompleted publication stored in db (BibDatabase) and save it 
    in BibTex file """
    with open('uncompleted_publications.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))
