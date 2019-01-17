from bibtexparser.bibdatabase import BibDatabase
import bibtexparser
from tkinter import ttk
from tkinter import *
from aneca_utils import *
from login import *

se = login(user, pswd)
se2, new_url, other_url = redirect(se)
se2, d, headers, final_url = acces_publication_area(se2, new_url, other_url)
db_salida = BibDatabase()
window = Tk()
pbar = ttk.Progressbar(window, mode='determinate', length=100)
""" Read data from BibTex file"""
with open('bib_test.bib', encoding='utf-8') as bibfile:
    db = bibtexparser.load(bibfile)
no_idx_article = list()
no_idx_article_false = list()
idx_article = list()
idx_article_false = list()
book = list()
book_false = list()
inproceedings = list()
inproceedings_false = list()
no_idx_article.append(db.entries[0])
no_idx_article_false.append(db.entries[1])
idx_article.append(db.entries[2])
idx_article_false.append(db.entries[3])
book.append(db.entries[4])
book_false.append(db.entries[5])
inproceedings.append(db.entries[6])
inproceedings_false.append(db.entries[7])
