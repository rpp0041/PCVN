#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GroupFilesUtils import parse_string
from selenium.common.exceptions import NoSuchElementException
import time

""" Function that will log user in to Aneca Academia Application"""


def login(browser, user, pswd):
    """ Insert user"""
    log_in = browser.find_element_by_id('login')
    log_in.send_keys(user)
    """ Insert password"""
    clave = browser.find_element_by_id('clave')
    clave.send_keys(pswd)
    """ Send Information"""
    browser.find_element_by_id('boton_entrar').click()
    return browser


""" Function that will get selenium driver to Academia application 
asking the user to log in with the credentials"""


def go_to_academia(browser, user, pswd):
    """ go to ANECA web site"""
    browser.get(
        'https://sede.educacion.gob.es/sede/login/inicio.jjsp;jsessionid=7D33705756C3CC4DC0C46E17B7DEA3CB')
    """ search for Academia """
    academia = browser.find_element_by_id(
        'buscadorConvocatoriasForm.descripcion.descripcion.desc')
    academia.send_keys('academia')
    browser.find_element_by_id(
        'buscarConvocatoriasInicio_boton_consulta_convocatoria').click()
    browser.find_element_by_id('listaConvocatoriaForm0').click()

    """ Check if the user & password given are correct 
    if not ask for it again """
    login(browser, user, pswd)
    try:
        browser.find_element_by_id('infoError')
        return True
    except NoSuchElementException:
        print('LogIn Correcto')

    """ Access to Academia 3.0 application  and close previous windows open
    in the future we will work with only with this window """
    browser.find_element_by_id('acciones').click()
    window_after = browser.window_handles[1]
    browser.close()
    browser.switch_to.window(window_after)
    time.sleep(8)


""" Function that will drive Selenium to Academia add Publication Area"""


def go_to_publications(browser):
    """ Acces to add publications area"""
    browser.find_elements_by_class_name('has-submenu')[2].click()
    browser.find_elements_by_class_name('has-submenu')[3].click()
    time.sleep(0.5)
    browser.find_element_by_link_text(
        'Calidad y difusión de los resultados de la actividad investigadora').click()

    """ Accept Coockie Polycy"""
    browser.find_element_by_link_text('Acepto').click()


""" Function tha will fill a new Book publication """


def fill_new_book(pub, browser, author_input, db):
    """Open new pub form """
    browser.find_element_by_id('nuevLibroCapituloId').click()
    time.sleep(1)
    """ fill author *NECESSARY FIELD* """
    au = browser.find_element_by_id('autoresFilter')
    add_au = browser.find_element_by_xpath('//*[@title="Añadir"]')
    if 'author' in pub:
        for author in pub['author'].split(' and '):
            au.send_keys(author)
            add_au.click()
        """ fill author position"""
        pos = author_position(pub['author'], author_input)
        browser.find_element_by_id('posicionSolicitanteTextId').send_keys(pos)
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill Title *NECESSARY FIELD* """
    if 'title' in pub:
        browser.find_element_by_id('tituloLibroTextId').send_keys(pub['title'])
    else:
        db = save_pub(db, browser, pub)
        return db
    """ fill volume """
    if 'volume' in pub:
        browser.find_element_by_id('volumenTextId').send_keys(pub['volume'])
    """fill pages"""
    if 'pages' in pub:
        pagefrom = browser.find_element_by_id('pagDesdeTextId')
        pagelast = browser.find_element_by_id('pagHastaTextId')
        pages = pub['pages'].split('-')
        pagefrom.send_keys(pages[0])
        pagelast.send_keys(pages[1])
    """ fill number of cites """
    browser.find_element_by_id('numeroCitasTextAreaId').send_keys(pub['cites'])

    """Check if has YEAR & fill the field"""
    if 'year' in pub:
        browser.find_element_by_id(
            'annioPublicacionTextId').send_keys(pub['year'])
    """ Check if has ISBN & fill the field"""
    if 'isbn' in pub:
        browser.find_element_by_id('isbnTextId').send_keys(pub['isbn'])
    """ Check if has publisher & fill the field """
    if 'publisher' in pub:
        browser.find_element_by_id(
            'editorialTextId').send_keys(pub['publisher'])

    # TODO
    browser.find_element_by_class_name('col-sm-7').click()
    browser.find_element_by_xpath('//*[@data-value="2"]').click()

    """save"""
    browser.find_element_by_id('saveBtn').click()

    return db


""" Function tha will fill a new not indexed
Article publication """


def fill_new_article(pub, browser, author_input, db):
    """Open new pub form """
    browser.find_element_by_id('nuevaPublicacionNoIdxId').click()
    time.sleep(1)
    """ fill author *NECESSARY FIELD* """
    au = browser.find_element_by_id('autoresFilter')
    add_au = browser.find_element_by_xpath('//*[@title="Añadir"]')
    if 'author' in pub:
        for author in pub['author'].split(' and '):
            au.send_keys(author)
            add_au.click()
        """ fill author position"""
        pos = author_position(pub['author'], author_input)
        browser.find_element_by_id('posicionSolicitanteTextId').send_keys(pos)
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill Title *NECESSARY FIELD * """
    if 'title' in pub:
        browser.find_element_by_id('tituloTextId').send_keys(pub['title'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill journal *NECESSARY FIELD* """
    if 'journal' in pub:
        browser.find_element_by_id(
            'nombreRevistaTextId').send_keys(pub['journal'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill volume *NECESSARY FIELD* """
    if 'volume' in pub:
        browser.find_element_by_id('volumenTextId').send_keys(pub['volume'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """fill pages"""
    if 'pages' in pub:
        pagefrom = browser.find_element_by_id('pagDesdeTextId')
        pagelast = browser.find_element_by_id('pagHastaTextId')
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            pagefrom.send_keys(pages[0])
            pagelast.send_keys(pages[1])
        else:
            pagefrom.send_keys(0)
            pagelast.send_keys(pages[0])

    """ fill year *NECESSARY FIELD* """
    if 'year' in pub:
        browser.find_element_by_id(
            'annioPublicacionTextId').send_keys(pub['year'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ Check if has ISBN & fill the field"""
    if 'issn' in pub:
        browser.find_element_by_id('issnTextId').send_keys(pub['issn'])

    """ Check if has D.O.I & fill the field """
    if 'doi' in pub:
        browser.find_element_by_id('doiTextId').send_keys(pub['doi'])

    # TODO
    browser.find_element_by_class_name('col-sm-5').click()
    browser.find_element_by_xpath('//*[@data-value="2"]').click()

    """save"""
    browser.find_element_by_id('saveBtn').click()

    return db


""" Function tha will fill a new Inprocedings publication """


def fill_new_inproceedings(pub, browser, author_input, db):
    """Open new pub form """
    browser.find_element_by_id('nuevoCongreso').click()
    time.sleep(1)

    """ fill author"""
    if 'author' in pub:

        au = browser.find_element_by_id('autoresFilter')
        add_au = browser.find_element_by_xpath('//*[@title="Añadir"]')
        for author in pub['author'].split(' and '):
            au.send_keys(author)
            add_au.click()
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill Type """
    browser.find_element_by_class_name('col-sm-4').click()
    browser.find_element_by_xpath('//*[@data-value="1"]').click()
    """ fill Title"""
    browser.find_element_by_id('tituloTextId').send_keys(pub['title'])

    """ fill Name of the congress"""
    if 'note' in pub:
        browser.find_element_by_id('denominacionTextId').send_keys(pub['note'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill Organizer """
    if 'organization' in pub:
        browser.find_element_by_id(
            'entidadOrganizadoraTextId').send_keys(pub['organization'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill place of congress """
    if 'address' in pub:
        browser.find_element_by_id('lugarTextId').send_keys(pub['address'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill date"""
    if 'da' in pub:
        browser.find_element_by_id('fDesdeTextId').send_keys(pub['da'])
        browser.find_element_by_id('fHastaTextId').send_keys(pub['da'])
    else:
        db = save_pub(db, browser, pub)
        return db
    """ fill volume """
    if 'volume' in pub:
        browser.find_element_by_id(
            'volumenTextId').send_keys(pub['volume'])
    """fill pages"""
    if 'pages' in pub:
        pagefrom = browser.find_element_by_id('pagDesdeTextId')
        pagelast = browser.find_element_by_id('pagHastaTextId')
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            pagefrom.send_keys(pages[0])
            pagelast.send_keys(pages[1])
        else:
            pagefrom.send_keys(0)
            pagelast.send_keys(pages[0])

    """ Check if has ISSN & fill the field"""
    if 'issn' in pub:
        browser.find_element_by_id('issnisbnTextId').send_keys(pub['issn'])
    elif 'isbn' in pub:
        browser.find_element_by_id('issnisbnTextId').send_keys(pub['isbn'])

    """save"""
    browser.find_element_by_id('saveBtn').click()
    return db


""" Function tha will fill a new Indexed Article publication """


def fill_new_index_article(pub, browser, author_input, db):
    """Open new pub form """
    browser.find_element_by_id('nuevaPublicacionIdxId').click()
    time.sleep(1)
    """ fill author"""
    if 'author' in pub:
        au = browser.find_element_by_id('autoresFilter')
        add_au = browser.find_element_by_xpath('//*[@title="Añadir"]')
        for author in pub['author'].split(' and '):
            au.send_keys(author)
            add_au.click()
        """ fill author position"""
        pos = author_position(pub['author'], author_input)
        browser.find_element_by_id('posicionSolicitanteTextId').send_keys(pos)

    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill Title"""
    if 'title' in pub:
        browser.find_element_by_id('tituloTextId').send_keys(pub['title'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill journal """
    if 'journal' in pub:
        browser.find_element_by_id(
            'nombreRevistaTextId').send_keys(pub['journal'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """ fill volume """
    if 'volume' in pub:
        browser.find_element_by_id('volumenTextId').send_keys(pub['volume'])
    else:
        db = save_pub(db, browser, pub)
        return db

    """fill pages"""
    if 'pages' in pub:
        pagefrom = browser.find_element_by_id('pagDesdeTextId')
        pagelast = browser.find_element_by_id('pagHastaTextId')
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            pagefrom.send_keys(pages[0])
            pagelast.send_keys(pages[1])
        else:
            pagefrom.send_keys(0)
            pagelast.send_keys(pages[0])

    """Check if has YEAR & fill the field"""
    if 'year' in pub:
        browser.find_element_by_id(
            'annioPublicacionTextId').send_keys(pub['year'])
        browser.find_element_by_id('annioCalidadTextId').send_keys(pub['year'])
    else:
        db = save_pub(db, browser, pub)
        return db
    """ Check if has ISSN & fill the field"""
    if 'issn' in pub:
        browser.find_element_by_id('issnTextId').send_keys(pub['issn'])

    """ Check if has D.O.I & fill the field """
    if 'doi' in pub:
        browser.find_element_by_id('doiTextId').send_keys(pub['doi'])

    """ Fill Index Data Base """
    browser.find_element_by_id('baseDatosTextId').send_keys('Web of Science')
    """ Fill ImpactIndex """
    browser.find_element_by_id(
        'indiceImpactoTextId').send_keys(pub['impactindex'])

    """ Fill journal rank position """
    position = pub['journalrank'].split('\n')
    category = pub['journalcategory'].split('\n')
    quartile = pub['journalquartile'].split('\n')

    flag_index = False
    for x in range(0, len(position)):
        if fill_journal(browser, position, category, quartile) is True:
            position.pop(0)
            category.pop(0)
            quartile.pop(0)
        else:
            flag_index = True
            break

    if not flag_index:
        db = save_pub(db, browser, pub)
        return db

    """ Fill JCR cites"""
    browser.find_element_by_id('citasJcrTextId').send_keys(pub['cites'])

    # TODO
    browser.find_element_by_class_name('col-sm-5').click()
    browser.find_element_by_xpath('//*[@data-value="2"]').click()

    """save"""
    browser.find_element_by_id('saveBtn').click()
    return db


""" Function that will return the position of an author in a string 
parameter : String
return : int    
"""


def author_position(auth, author_input):
    cont = 1
    """ Parse author name (remove non alphabetic characters)"""
    au2 = parse_string(author_input)
    """ Split author strings in to substring to be compared"""
    for author in auth.split(' and '):
        """ parse sub string """
        au1 = parse_string(author)
        if au1 == au2:
            return cont
        cont += 1
    return 1


""" Function that will save given publication to be written in a BibTex File , the publications to be saved are those 
that are not completed (there are missing fields)"""


def save_pub(db, browser, pub):
    """ Add pub to db """
    db.entries.append(pub)
    """ Cancel publication"""
    browser.find_element_by_class_name('close').click()
    return db


def fill_journal(browser, position, category, quartile):
    if position[0] != 'None':
        pos1 = position[0].split('/')
        browser.find_element_by_id('posRevistaTextId').send_keys(pos1[0])

        """ Fill number of journal rank max"""
        browser.find_element_by_id('posRevistaMaxTextId').send_keys(pos1[1])

        """ Fill Category """
        browser.find_element_by_id('categoriaTextId').send_keys(category[0])

        """Fill quartile """
        browser.find_element_by_id('cuartilComboId').send_keys(quartile[0][1])

        """ Fill Other information """
        if len(position) > 1:
            other_information = ''
            for x in range(1, len(position)):
                other_information += 'rank' + position[x]
                other_information += 'quartile' + quartile[x]
                other_information += 'Category' + category[x] + ' '
            browser.find_element_by_id('otrosIndiciosTextAreaId').send_keys(other_information)
    else:
        return True
