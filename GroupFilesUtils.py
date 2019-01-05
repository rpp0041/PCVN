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
        time.sleep(6)
        """ See all data for every year from 2017-1998"""
        browser.find_element_by_link_text("All years").click()
        time.sleep(10)
    except IndexError:
        time.sleep(0.1)
    dic_impact, rank_dic, quartile_dic, category_dic = get_info(browser)
    browser.close()
    return dic_impact, rank_dic, quartile_dic, category_dic


""" Function that will Check if we have data for the journla given
if not will search and add it to the data structure and finnaly return
the data for a exactly year given:
parameter : impact_index_list (list(dic))
            journal_list     (list(str))
            journal         (str)
            year            (int)

return :    impactIndex     (float)
"""


def check_impact_index(impact_index_list, journal_list, rank_list, quartile_list, category_list, journal, year):
    journalower = journal.lower()
    # Actual year dont have impact index , so we get past year index
    if year == '2018':
        year = '2017'
    # if journal name is not on the list search impact index and add it
    if journalower not in journal_list:
        journal_list.append(journalower)
        try:
            impact_dict, rank_dic, quartile_dic, category = get_impact_index(journalower)
        except TypeError:
            return
        impact_index_list.append(impact_dict)
        rank_list.append(rank_dic)
        quartile_list.append(quartile_dic)
        category_list.append(category)
        return impact_dict.get(str(year)), rank_dic.get(str(year)), quartile_dic.get(str(year)), category
    # if it is on the list search on impacIndexList
    else:
        index = journal_list.index(journalower)
        impact_dict = impact_index_list[index]
        rank_dic = rank_list[index]
        quartile_dic = quartile_list[index]
        category = category_list[index]
        return impact_dict.get(str(year)), rank_dic.get(str(year)), quartile_dic.get(str(year)), category


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


def parse_wos(wos, impact_index_list, journal_list, rank_list, category_list, quartile_list, pbar):
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
            # Check impact index
            try:
                impact_index, rank, quartile, category = check_impact_index(impact_index_list, journal_list, rank_list,
                                                                            quartile_list, category_list, journal, year)
                pub['impactIndex'] = str(impact_index)
                pub['journalRank'] = str(rank)
                pub['journalQuartile'] = str(quartile)
                pub['journalCategory'] = str(category)
            except TypeError:
                pass
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


def get_info(browser):
    browser.find_element_by_link_text('Rank').click()
    time.sleep(0.5)
    """ Save results in a list """
    table=browser.find_element_by_id('gridview-1011-body').text
    table=table.split('\n')

    """ Parse list to dict to be returned """
    dic_impact = dict()
    """ the important rows are 0 & 2 , so we avoid the rest of rows 
    14 rows in total"""

    for i in range(0,len(table), 14):
        dic_impact[table[i]] = table[i+2]

    """ RANK & QUARTILE OF JOURNAL"""
    """ Extract data from rank table"""
    name_tab = browser.find_element_by_id('headercontainer-1038-innerCt').text
    name_tab = name_tab.split('\n')
    num_of_categories = int((len(name_tab) - 1) / 4)

    """ Extract category names """
    rank_table = browser.find_element_by_id('gridview-1039').text
    rank_table = rank_table.split('\n')

    """ Check table"""
    rank_table, name_tab = parse_table(rank_table, name_tab, num_of_categories)

    """ Remove years from table"""
    list_year = list()
    for i in range(0, len(rank_table), (num_of_categories * 3) + 1):
        list_year.append(rank_table[i])
    for i in list_year:
        rank_table.remove(i)

    """ fill dict """
    dic_rank = dict()
    dic_quartile = dict()
    cont_year = 0
    """ fill rank & quartile """
    for i in range(0, len(rank_table), num_of_categories * 3):
        rank = ''
        quartile = ''
        if num_of_categories > 1:
            for x in range(0, (num_of_categories - 1) * 3, 3):
                rank += str(rank_table[i]) + '\n'
                quartile += str(rank_table[i + 1]) + '\n'

            rank += str(rank_table[i + 3])
            quartile += str(rank_table[i + 4])
        else:
            rank += str(rank_table[i])
            quartile += str(rank_table[i + 1])

        dic_rank[list_year[cont_year]] = rank
        dic_quartile[list_year[cont_year]] = quartile
        cont_year += 1

    """ fill category"""
    name = ''
    if num_of_categories > 1:
        for i in range(1, len(name_tab) - 4, 4):
            name += str(name_tab[i]) + '\n'

        name += str(name_tab[i + 4])
    else:
        name += str(name_tab[1])
    return dic_impact, dic_rank, dic_quartile, name


def parse_table(rank_table, name_tab, num_of_categories):
    # remove white spaces in fields
    for i in range(0, len(rank_table)):
        rank_table[i] = rank_table[i].lstrip()
    """ when undefined appears in a row of the table percentile row  disappears, producing errors on code execution """
    i = 0
    while i < len(rank_table):
        if rank_table[i] == 'undefined':
            rank_table.insert(i + 1, '\\')
        i += 1
    """ difference of fields betwen actual 2017 (2018 data still not released)
    and previus year (2016)"""
    diff = rank_table.index('2016')-1
    """ num of standard fields for a normal rank table"""
    num_fields = (num_of_categories * 3) + 1
    """ num of fields to be remove"""
    num_to_remove = diff - num_fields

    if diff > num_fields:
        # cont of fields to remove per row
        cont = num_fields
        # new table
        table_parsed = list()
        """ parse rank table"""
        i = 0
        while i < len(rank_table):
            if cont == 0:  # cont is over
                i += num_to_remove  # skip extra fields
                cont = num_fields  # start again cont
            else:
                table_parsed.append(rank_table[i])  # add field to new table
                cont -= 1
            i += 1
        rank_table=table_parsed.copy()
        """ parse header table """
        num_header = (num_of_categories * 4) + 1
        for j in range(num_header, len(name_tab)):
            name_tab.pop()

    return rank_table, name_tab
