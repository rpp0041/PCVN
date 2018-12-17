""" Needed libraries.
Selenium: we will use selenium to navegate through WOS web site
Time : we will use it for add delay to code execution
BibTexParser : we will use to read BibTex file
anecaUtils: set of functions to navigate in ACADEMIA
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import bibtexparser
from anecaUtils import *

""" Options for Selenium driver """
options = Options()
options.headless = True

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
browser = webdriver.Firefox(firefox_profile=fp)

""" Go to Academia application """
GoToAcademia(browser)
""" Go to add publications Area """
GoToPublications(browser)

""" Read data from BibTex file"""
with open('BibFINAL.bib', encoding='utf-8') as bibfile:
    db = bibtexparser.load(bibfile)

""" Add every publication readed from file"""
for i in db.entries:
    if i['ENTRYTYPE']=='book':
        fillNewBook(i,browser)
        time.sleep(7)
    elif i['ENTRYTYPE']=='article':
        fillNewArticle(i,browser)
        time.sleep(10)
    elif i['ENTRYTYPE']=='inproceedings':
        fillNewArticle(i,browser)
        time.sleep(7)