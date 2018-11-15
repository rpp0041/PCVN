from selenium import webdriver
author= input('Nombre del Autor :')

browser = webdriver.Firefox()

browser.get('https://apps.webofknowledge.com/UA_GeneralSearch_input.do?product=UA&search_mode=GeneralSearch&SID=F1QKecnLPApr37LVXSI&preferencesSaved=')

elem =  browser.find_element_by_id('value(input1)')
elem.send_keys(author)

browser.find_element_by_id("select2-select1-container").click()
browser.find_elements_by_class_name('select2-results__option')[2].click()
browser.find_element_by_id('searchCell1').click()

