#!/usr/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from unicodedata import normalize
import time
import re

"""Function that return the impact index of a journal from 2017 to 1998 
parameter : string (Name of journal) 
return : dict (with impact index and year as Key)
         dict (with journal rank and year as Key)
         dict (with journal quartile and year as Key)
         dict (with journal category and year as Key)
"""


def get_impact_index(title):
    # set options of driver to be invisible for user (headless)
    options = Options()
    options.headless = True
    # set driver browser as Firefox
    fp = webdriver.FirefoxProfile()
    # initialize driver with options
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
    # wait for page to load
    time.sleep(5)

    """ Insert search"""
    browser.find_element_by_id('search-inputEl').send_keys(title)
    time.sleep(2)
    """ Click first journal option to search if there are no results 
    will return 0 """
    try:
        browser.find_elements_by_class_name('x-boundlist-item')[0].click()
    except IndexError:
        browser.quit()
        return 0
    # wait page to load
    time.sleep(5)

    # catch IndexError if there are no more than 1 window open
    try:
        """  close previous windows open """
        window_after = browser.window_handles[1]
        browser.quit()
        browser.switch_to.window(window_after)
        time.sleep(6)
        """ See all data for every year from 2017-1998"""
        browser.find_element_by_link_text("All years").click()
        time.sleep(10)
    except IndexError:
        time.sleep(0.1)
    try:
        dic_impact, rank_dic, quartile_dic, tertile_dict, category_dic = get_info(browser)
    except NoSuchElementException:
        browser.quit()
        return
    browser.quit()
    return dic_impact, rank_dic, quartile_dic, tertile_dict, category_dic


""" Function that will Check if we have data for the journla given
if not will search and add it to the data structure and finnaly return
the data for a exactly year given:
parameter : impact_index_list (list(dic))
            journal_list     (list(str))
            journal         (str)
            year            (int)

return :    impactIndex     (float)
"""


def check_impact_index(impact_index_list, journal_list, rank_list, quartile_list, tertile_list, category_list, journal,
                       year):
    # put journal name in lower case
    journalower = journal.lower()
    # Actual year dont have impact index , so we get past year index
    if year == '2018':
        year = '2017'
    # if journal name is not on the list search quality indexes and add it
    if journalower not in journal_list:
        # try get_impact_index and catch Type error , return None
        try:
            impact_dict, rank_dic, quartile_dic, tertile_dic, category = get_impact_index(journalower)
            # add journal name to the list
            journal_list.append(journalower)
        except (TypeError, NoSuchElementException) as e:
            return
        # add quality indexes (dic) to each list
        impact_index_list.append(impact_dict)
        rank_list.append(rank_dic)
        quartile_list.append(quartile_dic)
        tertile_list.append(tertile_dic)
        category_list.append(category)

        return impact_dict.get(str(year)), rank_dic.get(str(year)), quartile_dic.get(str(year)), tertile_dic.get(
            str(year)), category
    # if it is on the list search search on the list the correspond year
    else:
        # search journal position in list, will serve as index for the other lists
        index = journal_list.index(journalower)

        # search dicts in lists
        impact_dict = impact_index_list[index]
        rank_dic = rank_list[index]
        quartile_dic = quartile_list[index]
        tertile_dic = tertile_list[index]
        category = category_list[index]

        # return value for the correspond year
        return impact_dict.get(str(year)), rank_dic.get(str(year)), quartile_dic.get(str(year)), tertile_dic.get(
            str(year)), category


""" Function that if 2 given publications check if has ISSN attribute
and in case both have , check if are equal
parameter : publication (dict)
return : True/False
"""


def check_issn(pub1, pub2):
    # Check if issn field is in both publications
    if 'issn' in pub1 and 'issn' in pub2:
        # if it is and is equal return True , Else return False
        if pub1['issn'] == pub2['issn']:
            return True
    return False


""" Function that if 2 given publications check if  their titles are equal
parameter : publication (dict)
return : True/False
"""


def check_title(pub1, pub2):
    # parse titles trying to be as accurate in comparision as possible
    if 'title' in pub1 and 'title' in pub2:
        title1 = parse_string(pub1['title'])
        title2 = parse_string(pub2['title'])
        # return True if Equal, return false if not
        if title1 == title2:
            return True
    return False


""" Function that given 2 list of publications check if their are the same
in 2 steps first by ISSN (in case both have),second By Title
parameter: list of publications (list of dicts)
return: lists """


def remove_duplicates(list1, list2):
    # go trough al publications on list 1
    for pub in list1:
        # go trough al publications on list 2
        for pub2 in list2:
            # check if issn or title are equals, if they are update pub from list 1 and remove second one.
            if check_issn(pub, pub2):
                """ In case ISSN is the same,update keys from 1st pub"""
                pub2.update(pub)
                list1.remove(pub)
                break
            elif check_title(pub, pub2):
                """ In case title is the same,update keys from 1st pub"""
                pub2.update(pub)
                list1.remove(pub)
                break
    return list1, list2


""" Function that will parse WOS BibTex file for a correct format.
We need to remove extra '{}' characters , but some fields has not
this extra characters so we exclude them from parse proccess.
parameter: list of publications (list of dicts)
           impact_index_list      (list of dicts)
           journal_list          (list of str)
"""


def parse_wos(wos, impact_index_list, journal_list, rank_list, category_list, quartile_list, tertile_list, pbar):
    # progress bar GUI increment
    pbar_increment = 85 / len(wos)
    for pub in wos:
        # remove fields that not need to be parsed
        list_keys = list(pub.keys())
        list_keys.remove('author')
        list_keys.remove('ENTRYTYPE')
        list_keys.remove('ID')
        # removed extra brackets on each field
        for key in list_keys:
            pub[key] = pub[key].split('{')[1].split('}')[0]
        # if publication is an article , then we will search for quality indexes
        if pub['ENTRYTYPE'] == 'article':
            year = pub['year']
            journal = pub['journal']
            # Check quality indexes

            try:
                impact_index, rank, quartile, tertile, category = check_impact_index(impact_index_list, journal_list,
                                                                                     rank_list,
                                                                                     quartile_list, tertile_list,
                                                                                     category_list, journal, year)
                pub['impactIndex'] = str(impact_index)
                pub['journalRank'] = str(rank)
                pub['journalQuartile'] = str(quartile)
                pub['journalTertile'] = str(tertile)
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
because this will mean that during consulting progress 
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


""" Function that will get information about journal quality indexes , rank , quartile ,categories etc.
With a selenium browser with journal page loaded (in JCR), will look for its quality indexes and return several dicts
one for each index with information of all the possible years. 
"""


def get_info(browser):
    # click on rank field
    browser.find_element_by_link_text('Rank').click()
    time.sleep(0.5)
    """ Save results in a list """
    table = browser.find_element_by_id('gridview-1011-body').text
    table = table.split('\n')

    """ Parse list to dict to be returned """
    dic_impact = dict()
    """ the important rows are 0 & 2 , so we avoid the rest of rows 
    14 rows in total"""

    for i in range(0, len(table), 14):
        dic_impact[table[i]] = table[i + 2]

    """ RANK & QUARTILE OF JOURNAL"""
    """ Extract data from rank table"""
    name_tab = browser.find_element_by_id('headercontainer-1038-innerCt').text
    name_tab = name_tab.split('\n')
    # number of categories the journal is part of
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
    dic_tertile = dict()
    # counter index of the year
    cont_year = 0
    """ Go trough all the rows in the table to fill rank & quartile"""
    for i in range(0, len(rank_table), num_of_categories * 3):
        # strings to group all the information about rank & quartile
        rank = ''
        quartile = ''
        tertile = ''
        # if there are more than 1 categories add all ranks and quartile of each category in the string
        # we will add '\n' to separate each category
        # else add just the correspond (only 1)
        if num_of_categories > 1:
            # go trough all rank & quartile (- last one that will be added later)
            for x in range(0, (num_of_categories - 1) * 3, 3):
                # add rank & quartile
                rank += str(rank_table[i]) + '\n'
                quartile += str(rank_table[i + 1]) + '\n'
                tertile += str(calculate_tertile(rank_table[i])) + '\n'

            # add last rank & quartile without '\n'
            rank += str(rank_table[i + 3])
            quartile += str(rank_table[i + 4])
            tertile += str(calculate_tertile(rank_table[i + 3]))
        else:
            rank += str(rank_table[i])
            quartile += str(rank_table[i + 1])
            tertile += str(calculate_tertile(rank_table[i]))

        # add strings to each dict with year as key
        dic_rank[list_year[cont_year]] = rank
        dic_quartile[list_year[cont_year]] = quartile
        dic_tertile[list_year[cont_year]] = tertile
        # counter year +1
        cont_year += 1

    """ fill category"""
    # string to group all categories if needed
    name = ''
    # if there are more than 1 categories add all of them to the String
    # else add just the correspond (only 1)
    if num_of_categories > 1:
        # go trough all categories (- last one that will be added later)
        for i in range(1, len(name_tab) - 4, 4):
            name += str(name_tab[i]) + '\n'
        # add last category without '\n'
        name += str(name_tab[i + 4])
    else:
        name += str(name_tab[1])
    return dic_impact, dic_rank, dic_quartile, dic_tertile, name


""" Function that will parse the table with indexes quality in case it is not completed 
Ex: there are 3 categories but only 7 rows , there should be 9 rows (3 per category)"""


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
    try:
        diff = rank_table.index('2016') - 1
    except ValueError:
        return None
    """ num of standard fields for a normal rank table"""
    num_fields = (num_of_categories * 3) + 1
    """ num of fields to be remove"""
    num_to_remove = diff - num_fields

    if diff > num_fields:
        # cont of fields to remove per row
        cont = num_fields
        # new tablef
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
        rank_table = table_parsed.copy()
        """ parse header table """
        num_header = (num_of_categories * 4) + 1
        for j in range(num_header, len(name_tab)):
            name_tab.pop()

    return rank_table, name_tab


""" Function that will calculate the tertile of a journal, given the rank of this journal"""


def calculate_tertile(rank):
    try:
        posjournal = int(rank.split('/')[0])
        numjournal = int(rank.split('/')[1])
    except (ValueError, AttributeError):
        return 'None'

    return round(posjournal * 3 / (numjournal + 1) + .5)


""" Function that will parse number of cites of Scopus publications"""


def parse_scopus(scopus):
    for pub in scopus.entries:
        """ ex: cited by 4"""
        cites = pub['note'].split(' ')[2]
        cites = re.sub('[^0-9]', '', cites)
        pub['cites'] = cites
        del pub['note']

        if 'isbn' in pub.keys():
            isbn = pub['isbn'].split('; ')
            if len(isbn) > 1:
                pub['isbn'] = isbn[1]

    return scopus
