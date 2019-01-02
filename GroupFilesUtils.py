#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from unicodedata import normalize
import time
import re


"""Function that return the impact index of a journal from 2017 to 1998 
parameter : Name of journal 
return : dict with impact index and year"""


def get_impact_index(title):

    options = Options()
    options.headless = True
    fp = webdriver.FirefoxProfile()
    browser = webdriver.Firefox(options=options, firefox_profile=fp)
    """ Go to incites web site """
    browser.get(
        ' https://jcr.incites.thomsonreuters.com/JCRJournalHomeAction.action')

    """ Select FECYT as acces mode """
    browser.find_element_by_xpath(
        "//div//select[@name='select2']//option[text()='Federation of Spain by FECYT']").click()
    """ Click go Button """
    browser.find_element_by_xpath(
        '//div//a[@href="javascript:shibbolethRedirect(document.forms[1].select2);"]').click()

    time.sleep(5)
    """ Insert search"""
    browser.find_element_by_id('search-inputEl').send_keys(title)
    time.sleep(2)
    """ Click first journal option to search if there are no results 
    will return 0 """
    try:
        browser.find_elements_by_class_name('x-boundlist-item')[0].click()
    except IndexError:
        browser.close()
        return 0

    time.sleep(5)
    try:
        """  close previous windows open """
        window_after = browser.window_handles[1]
        browser.close()
        browser.switch_to.window(window_after)
        time.sleep(5)
        """ See all data for every year from 2017-1998"""
        browser.find_element_by_link_text("All years").click()
        time.sleep(10)
    except IndexError:
        time.sleep(0.1)
    """ Save results in a list """
    table = browser.find_elements_by_class_name('x-grid-cell-inner')

    """ Parse list to dict to be returned """
    dic = dict()
    """ the are 2 extra rows with unusefull information 
    so we avoid them settin the length in -28.
    the important rows are 0 & 2 , so we avoid the rest of rows 
    14 rows in total"""
    ln = len(table)-28
    for i in range(0, ln, 14):
        dic[table[i].text] = table[i+2].text

    browser.close()

    return dic


""" Function that will Check if we have data for the journla given
if not will search and add it to the data structure and finnaly return
the data for a exactly year given:
parameter : impact_index_list (list(dic))
            journal_list     (list(str))
            journal         (str)
            year            (int)

return :    impactIndex     (float)
"""


def check_impact_index(impact_index_list, journal_list, journal, year):
    journalower = journal.lower()
    # Actual year dont have impact index , so we get past year index
    if year == '2018':
        year = '2017'
    # if journal name is not on the list search impact index and add it
    if journalower not in journal_list:
        journal_list.append(journalower)
        impact_dict = get_impact_index(journalower)
        if impact_dict == 0:
            return 0
        impact_index_list.append(impact_dict)

        return impact_dict.get(str(year))
    # if it is on the list search on impacIndexList
    else:
        index = journal_list.index(journalower)
        impact_dict = impact_index_list[index]

        return impact_dict.get(str(year))


""" Function that if 2 given publications check if hass issn attribute
and in case both have , check if are equal
parameter : publication (dict)
return : True/False
"""


def check_issn(pub1, pub2):
    if 'issn' in pub1 and 'issn' in pub2:
        if pub1['issn'] == pub2['issn']:
            return True
    return False


""" Function that if 2 given publications check if  their titles are equal
parameter : publication (dict)
return : True/False
"""


def check_title(pub1, pub2):
    title1 = parse_string(pub1['title'])
    title2 = parse_string(pub2['title'])
    if title1 == title2:
        return True
    return False


""" Function that given 2 list of publications check if their are the same
in 2 steps first by ISSN (in case both have),second By Title
parameter: list of publications (list of dicts)
return: lists """


def remove_duplicates(list1, list2):
    for pub in list1:
        for pub2 in list2:
            if check_issn(pub, pub2):
                """ In case ISSN is the same,update keys from 1st pub"""
                pub.update(pub2)
                list2.remove(pub2)
            elif check_title(pub, pub2):
                """ In case title is the same,update keys from 1st pub"""
                pub.update(pub2)
                list2.remove(pub2)
    return list1, list2


""" Function that will parse WOS BibTex file for a correct format.
We need to remove extra '{}' characters , but some fields has not
this extra characters so we exclude them from parse proccess.
parameter: list of publications (list of dicts)
           impact_index_list      (list of dicts)
           journal_list          (list of str)
"""


def parse_wos(wos, impact_index_list, journal_list, pbar):
    pbar_increment = 85/len(wos)
    for pub in wos:
        list_keys = list(pub.keys())
        list_keys.remove('author')
        list_keys.remove('ENTRYTYPE')
        list_keys.remove('ID')
        for key in list_keys:
            pub[key] = pub[key].split('{')[1].split('}')[0]
        if pub['ENTRYTYPE'] == 'article':
            year = pub['year']
            journal = pub['journal']
            pub['impactIndex'] = str(check_impact_index(
                impact_index_list, journal_list, journal, year))
        """ update progress bar GUI"""
        pbar['value'] += pbar_increment
        pbar.update()


""" Function that will parse Volume field to remove extra information
that produces errors in ANECA application
parameter : publication (dict)
return: publication(dict) """


def parse_volume(pub):
    if 'volume' in pub.keys():
        pub['volume'] = pub['volume'].split(' ')[0]
    return pub


""" Function that will remove impactIndex key if equals 0
becouse this will mean that during consulting progress 
,there are not results found for this journal name
parameter : publication (dict)
return: publication(dict) """


def parse_impact_index(pub):
    if 'impactIndex' in pub.keys():
        if pub['impactIndex'] == '0':
            pub.pop('impactIndex')
    return pub


""" Function that will parse the given string to remove 
non alphabetic characters (spaces ,accented vowels , "-","_" etc )
parameter : string
return :    string 
"""


def parse_string(s):
    # -> NFD y eliminar diacríticos
    s = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1",
        normalize("NFD", s), 0, re.I
    )
    # -> NFC
    s = normalize('NFC', s)
    # remove non alphabetic characters
    regex = re.compile('[^a-zA-Z]')
    s = regex.sub('', s)
    return s.lower()
