# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from GroupFilesUtils import *
import bibtexparser
import pickle

"""" Function that will group all BibTex files return by the others functions in a single BibTex file removing in the 
process duplicates , parsing at the same time necessary fields and adding new ones (impactIndex , JournalRank etc) 
input : pbar (tkinter progress bar)
return : BibTex file
"""


def group_files(pbar):

    # Load BibTex files extract from the websites

    # Load Scopus BibTex File
    with open('scopus.bib', encoding='utf-8') as bibfile:
        scopus = bibtexparser.load(bibfile)
    # Load Google Scholar BibTex File
    with open('bibtexScholar.bib', encoding='utf-8') as bibfile:
        scholar = bibtexparser.load(bibfile)
    # Load WOS BibTex File
    with open('savedrecs.bib', encoding='utf-8') as bibfile:
        wos = bibtexparser.load(bibfile)
    # In case there are mora than 50 publications for this author in Web of science , function will generate 2 fields
    # so we try to read it, in case it do not exists FileNotFoundError , we do nothing
    try:
        with open('savedrecs(1).bib', encoding='utf-8') as bibfile:
            wos2 = bibtexparser.load(bibfile)
        for x in wos2.entries:
            wos.entries.append(x)
    except FileNotFoundError:
        pass

    """ update progress bar GUI"""
    pbar['value'] = 10
    pbar.update()

    """ Parse WOS db in order to get same format for every bibTex db 
    this will help us in the future comparison (otherwise it will be impossible)
    also look for quality indexes in JCR cites """
    try:
        with open('test.pkl', 'rb') as input:
            impact_index_list = pickle.load(input)
            rank_list = pickle.load(input)
            quartile_list = pickle.load(input)
            tertile_list = pickle.load(input)
            category_list = pickle.load(input)
            journal_list = pickle.load(input)
    except:
        impact_index_list = list()
        rank_list = list()
        quartile_list = list()
        tertile_list = list()
        category_list = list()
        journal_list = list()
    parse_wos(wos.entries, impact_index_list, journal_list, rank_list, category_list, quartile_list, tertile_list, pbar)
    scopus = parse_scopus(scopus)

    """ update progress bar GUI"""
    pbar['value'] = 95
    pbar.update()

    with open('test.pkl', 'wb') as output:
        pickle.dump(impact_index_list, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(rank_list, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(quartile_list, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(tertile_list, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(category_list, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(journal_list, output, pickle.HIGHEST_PROTOCOL)
    #####################################################################

    """ Remove Duplicates from the BibTex Files"""
    wos.entries, scopus.entries = remove_duplicates(wos.entries, scopus.entries)
    wos.entries, scholar.entries = remove_duplicates(
        wos.entries, scholar.entries)
    scopus.entries, scholar.entries = remove_duplicates(
        scopus.entries, scholar.entries)

    """ Write the dictionaries modified in a new BibTex file 
    at this point we will not have duplicate publications,
    also modify some field´s name to fit BibTex Standard (cites)
    and parse volume field because in same cases we get 
    extra information that produces errors in ACADEMIA
    """
    writer = BibTexWriter()
    db = BibDatabase()
    for i in scopus.entries:
        """ Parse Volume """
        i = parse_volume(i)
        """ Add pub to write BibTex db """
        db.entries.append(i)
    for i in scholar.entries:
        """ Parse Volume """
        i = parse_volume(i)
        """ Add pub to write BibTex db """
        db.entries.append(i)
    for i in wos.entries:
        """ Rename cites """
        i['cites'] = i['number-of-cited-references']
        i.pop('number-of-cited-references')
        """ Parse Volume """
        i = parse_volume(i)
        """ Parse ImpactIndex"""
        i = parse_impact_index(i)
        """ Add pub to write BibTex db """
        db.entries.append(i)
    """ Write db to BibTex file """
    with open('BibFINAL.bib', 'w', encoding='utf-8') as bibfile:
        bibfile.write(writer.write(db))

    """ update progress bar GUI"""
    pbar['value'] = 100
    pbar.update()
