# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from GroupFilesUtils import *
import bibtexparser


def group_files(pbar):
    # Load BibTex files extract from Google Scholar, Scopus and WOS
    # in order to remove duplicate publications and to group them
    # in just one file so it will make easier to work with.

    # Load BibTex files extract from the websites

    # Load Google Scholar BibTex File
    with open('bibtexScopus.bib', encoding='utf-8') as bibfile:
        scopus = bibtexparser.load(bibfile)
    # Load Scopus BibTex File
    with open('bibtexScholar.bib', encoding='utf-8') as bibfile:
        scholar = bibtexparser.load(bibfile)
    # Load WOS BibTex File
    with open('savedrecs.bib', encoding='utf-8') as bibfile:
        wos = bibtexparser.load(bibfile)

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
    this will help us in the future comparison (otherwise it will be impossible)"""
    impact_index_list = list()
    journal_list = list()
    parse_wos(wos.entries, impact_index_list, journal_list, pbar)

    """ update progress bar GUI"""
    pbar['value'] = 95
    pbar.update()

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
    and parse volume field becouse in same cases we get 
    extra information that prouces errors in ACADEMIA
    """
    writer = BibTexWriter()
    db = BibDatabase()
    for i in scopus.entries:
        """ Rename cites"""
        i['cites'] = i['citation_count']
        i.pop('citation_count')
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
