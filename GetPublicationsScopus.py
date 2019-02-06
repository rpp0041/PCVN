from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import os


def get_publications_scopus(author_id, pbar):
    """ Options for Selenium driver """
    # Set driver to be invisible
    options = Options()
    options.headless = True
    cwd = os.getcwd()
    # set driver browser to be Firefox
    fp = webdriver.FirefoxProfile()
    # Set directory where save documents (actual working dir)
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", str(cwd))
    # Never ask save to disk
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-bibtex")
    browser = webdriver.Firefox(options=options, firefox_profile=fp)

    """ go to scopus web page"""
    browser.get('https://www.scopus.com/search/form.uri?display=basic')
    time.sleep(5)  # wait page to load
    """ update progress bar GUI"""
    pbar['value'] = 20
    pbar.update()

    """ close po up"""
    browser.find_element_by_id('_pendo-close-guide_').click()

    """ advnaced search"""
    browser.find_element_by_partial_link_text('Advanced').click()
    query = 'au-id(%s)' % author_id
    browser.find_element_by_id('searchfield').send_keys(query)
    browser.find_element_by_id('advSearch').click()
    time.sleep(3)
    """ Check if there are results for author input"""
    try:
        browser.find_element_by_class_name('alert alert-danger')
        return True
    except NoSuchElementException:
        pass

    """ update progress bar GUI"""
    pbar['value'] = 30
    pbar.update()
    """ Select 200 per page"""
    browser.find_element_by_id('resultsPerPage-button').send_keys(200)
    time.sleep(4)   # wait for page to actualize records

    """ update progress bar GUI"""
    pbar['value'] = 50
    pbar.update()

    """ Selecet all publications to be exported"""
    browser.find_element_by_id('selectAllCheck').click()
    time.sleep(1)

    """ Click Export button"""
    element = WebDriverWait(browser, 20).until(
        ec.element_to_be_clickable((By.ID, "export_results")))
    browser.find_element_by_id('export_results').click()

    """ update progress bar GUI"""
    pbar['value'] = 70
    pbar.update()

    """ Select BibTex format file"""
    browser.find_elements_by_class_name('radio-label')[4].click()

    """ Add bibliographical information"""
    browser.find_element_by_xpath(
        ".//*[contains(text(), 'Bibliographical information')]"
    ).click()

    """ Click export"""
    browser.find_element_by_id('exportTrigger').click()

    """ update progress bar GUI"""
    pbar['value'] = 90
    pbar.update()
    """ Wait for download to complete & close selenium Driver"""
    time.sleep(5)
    browser.close()

    """ update progress bar GUI"""
    pbar['value'] = 100
    pbar.update()
