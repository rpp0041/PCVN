from selenium import webdriver
import time
author= input('Nombre del Autor :')

browser = webdriver.Firefox()

browser.get('https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=F1QKecnLPApr37LVXSI&preferencesSaved=')
time.sleep(5)
actualUrl=browser.current_url
logginUrl= 'https://login.webofknowledge.com/error/Error?Src=IP&Alias=WOK5&Error=IPError&Params=&PathInfo=%2F&RouterURL=https%3A%2F%2Fwww.webofknowledge.com%2F&Domain=.webofknowledge.com'
if actualUrl == logginUrl:
    browser.find_element_by_class_name("select2-selection__rendered").click()
    browser.find_elements_by_class_name('select2-results__option')[15].click()
    browser.find_element_by_class_name('no-underline').click()
    
time.sleep(5)
elem =  browser.find_element_by_id('value(input1)')
elem.send_keys(author)

browser.find_element_by_id("select2-select1-container").click()
browser.find_elements_by_class_name('select2-results__option')[2].click()
browser.find_element_by_id('searchCell1').click()

