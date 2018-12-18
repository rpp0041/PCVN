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
    """ Click search button"""
    browser.find_element_by_xpath(
        '//div//span[@class="fas fa-search header-search-submit"]').click()

    time.sleep(5)
    """  close previous windows open """
    window_after = browser.window_handles[1]
    browser.close()
    browser.switch_to.window(window_after)
    time.sleep(3)
    """ See all data for every year from 2017-1998"""
    browser.find_element_by_link_text("All years").click()
    time.sleep(10)
    """ Save results in a list """
    table = browser.find_elements_by_class_name('x-grid-cell-inner')

    """ Parse list to dict to be returned """
    dic = dict()

    for i in range(0, 280, 14):
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
	""" if journal not in list add it and search for data"""
    if journal not in JournalList:
        JournalList.append(journal)
        impactDict= GetImpactIndex(journal)
        ImpactIndexList.append(impactDict)
        
        return impactDict.get(str(year))
    """ if it is: look for it´s position
     return dict value for this year """
    else:
        index=JournalList.index(journal)
        impactDict=ImpactIndexList[index]
        
        return impactDict.get(str(year))
