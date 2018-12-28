""" Needed libraries to extract and write the data
Selenium: we will use selenium to navegate through WOS web site
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import os

""" Function that will help in saving records process """


def SelectSaveOptions(browser):
    """ Select save in other format file"""
    browser.find_elements_by_class_name('select2-selection__arrow')[1].click()
    browser.find_elements_by_class_name('select2-results__option')[6].click()

    """Select register content """
    browser.find_element_by_id('select2-bib_fields-container').click()
    browser.find_elements_by_class_name('select2-results__option')[3].click()
    """Select file format """
    browser.find_element_by_id('select2-saveOptions-container').click()
    browser.find_elements_by_class_name('select2-results__option')[1].click()

def get_publications_wos(author,pbar):
    """ We ask the user to enter the author´s name """
    #author = input('Nombre del Autor :')
    """ Get current working directory (where we will save the files) """
    cwd = os.getcwd()
    """ Set options for webdriver
    to be invisible for the user (headless) 
    to never ask "saveToDisk" in bibTex files)
    finnaly initialize in WOS web site 
    """
    options = Options()
    options.headless = False
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", str(cwd))
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/x-bibtex")
    browser = webdriver.Firefox(options=options, firefox_profile=fp)
    browser.get('https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=F1QKecnLPApr37LVXSI&preferencesSaved=')

    """ update progress bar GUI"""
    pbar['value'] =20
    pbar.update()
    """Wait 5 sec to ensure web is loaded, after that check 
    if current url is login web site , if it is :
    log selectintg federation of Spain (FECYT) """
    time.sleep(5)
    actualUrl = browser.current_url
    logginUrl = 'https://login.webofknowledge.com/error/Error?Src=IP&Alias=WOK5&Error=IPError&Params=&PathInfo=%2F&RouterURL=https%3A%2F%2Fwww.webofknowledge.com%2F&Domain=.webofknowledge.com'
    if actualUrl == logginUrl:
        browser.find_element_by_class_name("select2-selection__rendered").click()
        browser.find_elements_by_class_name('select2-results__option')[15].click()
        browser.find_element_by_class_name('no-underline').click()

    """ Wait 5 sec to ensure web is loaded,after that insert author´s name"""
    time.sleep(5)
    elem = browser.find_element_by_id('value(input1)')
    elem.send_keys(author)

    """ update progress bar GUI"""
    pbar['value'] =40
    pbar.update()

    """ Select author in dropdown and Click search"""
    browser.find_element_by_id("select2-select1-container").click()
    browser.find_elements_by_class_name('select2-results__option')[2].click()
    browser.find_element_by_id('searchCell1').click()

    """Select *show 50 per page* """
    browser.find_element_by_id('select2-selectPageSize_bottom-container').click()
    browser.find_elements_by_class_name('select2-results__option')[2].click()

    # Save results
    pageCount = browser.find_element_by_id('pageCount.bottom')
    pageCount = int(pageCount.text)

    SelectSaveOptions(browser)
    """ update progress bar GUI"""
    pbar['value'] =60
    pbar.update()
    """ Check if there are more than 50 records (pageCount>1)
    if TRUE :we will select number of records range to save
    from 1 to (pageCount-1 )*50, then we got to the last page
    and save all the records from it and close dialog

    if FALSE : we just save the records of that single page
    """
    if pageCount > 1:
        """ Select records range"""
        browser.find_element_by_id('numberOfRecordsRange').click()
        markFrom = browser.find_element_by_id('markFrom')
        markFrom.send_keys(1)
        markTo = browser.find_element_by_id('markTo')
        numRegister = (pageCount-1)*50
        markTo.send_keys(numRegister)

        """ Save and close dialog  """
        browser.find_element_by_class_name('quickoutput-action').click()
        time.sleep(5)
        browser.find_element_by_class_name('quickoutput-cancel-action').click()
        """ Go to last page"""
        gotopage = browser.find_element_by_class_name('goToPageNumber-input')
        gotopage.send_keys(pageCount)
        gotopage.submit()
        time.sleep(5)

        SelectSaveOptions()
        """ Save and close dialog  """
        browser.find_element_by_class_name('quickoutput-action').click()
        time.sleep(4)
        browser.find_element_by_class_name('quickoutput-cancel-action').click()
        """ update progress bar GUI"""
        pbar['value'] =80
        pbar.update()
    else:
        """ Save and close dialog  """
        browser.find_element_by_class_name('quickoutput-action').click()
        time.sleep(4)
        browser.find_element_by_class_name('quickoutput-cancel-action').click()

    browser.close()
    pbar['value'] =100
    pbar.update()

