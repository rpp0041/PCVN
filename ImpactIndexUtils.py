from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

"""Function that return the impact index of a journal from 2017 to 1998 
parameter : Name of journal 
return : dict with impact index and year"""


def GetImpactIndex(title):

    options = Options()
    options.headless = False
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
    except IndexError :
    	browser.close()
    	return 0

    time.sleep(5)
    """  close previous windows open """
    window_after = browser.window_handles[1]
    browser.close()
    browser.switch_to.window(window_after)
    time.sleep(5)
    """ See all data for every year from 2017-1998"""
    browser.find_element_by_link_text("All years").click()
    time.sleep(10)
    """ Save results in a list """
    table = browser.find_elements_by_class_name('x-grid-cell-inner')


    """ Parse list to dict to be returned """
    dic = dict()
    """ the are 2 extra rows with unusefull information 
    so we avoid them settin the length in -28.
    the important rows are 0 & 2 , so we avoid the rest of rows 
    14 rows in total"""
    ln=len(table)-28
    for i in range(0, ln, 14):
        dic[table[i].text] = table[i+2].text

    browser.close()

    return dic

""" Function that will Check if we have data for the journla given
if not will search and add it to the data structure and finnaly return
the data for a exactly year given:
parameter : ImpactIndexList (list(dic))
			JournalList 	(list(str))
			journal 		(str)
			year 			(int)

return : 	impactIndex 	(float)
"""
def CheckImpactIndex(ImpactIndexList, JournalList, journal, year):
    journalower = journal.lower()
    # Actual year dont have impact index , so we get past year index
    if year=='2018':
    	year='2017'
    # if journal name is not on the list search impact index and add it
    if journalower not in JournalList:
        JournalList.append(journalower)
        impactDict = GetImpactIndex(journalower)
        if impactDict==0:
        	return 0
        ImpactIndexList.append(impactDict)

        return impactDict.get(str(year))
    # if it is on the list search on impacIndexList
    else:
        index = JournalList.index(journalower)
        impactDict = ImpactIndexList[index]

        return impactDict.get(str(year))

