import getpass
import time
""" Function that will log user in to Aneca Academia Aplication"""


def login(browser):
    """ Insert user"""
    user = input('Introduzca el Usuarion (DNI/NIE)')
    login = browser.find_element_by_id('login')
    login.send_keys(user)
    """ Insert password"""
    pswd = getpass.getpass('Contraseña:')
    clave = browser.find_element_by_id('clave')
    clave.send_keys(pswd)
    """ Send Information"""
    browser.find_element_by_id('boton_entrar').click()
    return browser


def autologin(browser):
    """ Insert user"""
    user = '71291761H'
    login = browser.find_element_by_id('login')
    login.send_keys(user)
    """ Insert password"""
    pswd = '00a3f21d53'
    clave = browser.find_element_by_id('clave')
    clave.send_keys(pswd)
    """ Send Information"""
    browser.find_element_by_id('boton_entrar').click()
    return browser
""" Function that will get selenium driver to Academia application 
asking the user to log in with the credentials"""

def GoToAcademia(browser):
    """ go to ANECA web site"""
    browser.get(
        'https://sede.educacion.gob.es/sede/login/inicio.jjsp;jsessionid=7D33705756C3CC4DC0C46E17B7DEA3CB')
    """ search for Academia """
    Academia = browser.find_element_by_id(
        'buscadorConvocatoriasForm.descripcion.descripcion.desc')
    Academia.send_keys('academia')
    browser.find_element_by_id(
        'buscarConvocatoriasInicio_boton_consulta_convocatoria').click()
    browser.find_element_by_id('listaConvocatoriaForm0').click()

    """ Check if the user & password given are correct 
    if not ask for it again """
    while True:
        # login()
        autologin(browser)
        try:
            browser.find_element_by_id('infoError')
            print('Información introducida erronea pruebe de nuevo')
        except:
            print('LogIn Correcto')
            break
    """ Access to Academia 3.0 application  and close previous windows open
    in the future we will work with only with this window """
    browser.find_element_by_id('acciones').click()
    window_after = browser.window_handles[1]
    browser.close()
    browser.switch_to.window(window_after)
    time.sleep(7)

    return browser


def GoToPublications(browser):
    """ Acces to add publications area"""
    browser.find_elements_by_class_name('has-submenu')[2].click()
    browser.find_elements_by_class_name('has-submenu')[3].click()
    time.sleep(0.5)
    browser.find_element_by_link_text(
        'Calidad y difusión de los resultados de la actividad investigadora').click()

    """ Accept Coockie Polycy"""
    browser.find_element_by_link_text('Acepto').click()


def fillNewBook(pub, browser):
    """Open new pub form """
    browser.find_element_by_id('nuevLibroCapituloId').click()
    time.sleep(1)
    """ fill author"""
    au = browser.find_element_by_id('autoresFilter')
    addAU = browser.find_element_by_xpath('//*[@title="Añadir"]')
    for author in pub['author'].split(' and '):
        au.send_keys(author)
        addAU.click()
    """ fill Title"""
    browser.find_element_by_id('tituloLibroTextId').send_keys(pub['title'])
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
    browser.find_element_by_id('posicionSolicitanteTextId').send_keys(1)
    browser.find_element_by_class_name('col-sm-7').click()
    browser.find_element_by_xpath('//*[@data-value="2"]').click()

    """save"""
    browser.find_element_by_id('saveBtn').click()


def fillNewArticle(pub, browser):
    """Open new pub form """
    browser.find_element_by_id('nuevaPublicacionNoIdxId').click()
    time.sleep(1)
    """ fill author"""
    au = browser.find_element_by_id('autoresFilter')
    addAU = browser.find_element_by_xpath('//*[@title="Añadir"]')
    for author in pub['author'].split(' and '):
        au.send_keys(author)
        addAU.click()
    """ fill Title"""
    browser.find_element_by_id('tituloTextId').send_keys(pub['title'])
    """ fill journal """
    browser.find_element_by_id('nombreRevistaTextId').send_keys(pub['journal'])
    """ fill volume """
    if 'volume' in pub:
        browser.find_element_by_id('volumenTextId').send_keys(pub['volume'])
    else:
        browser.find_element_by_id('volumenTextId').send_keys(0) #TODO
    """fill pages"""
    if 'pages' in pub:
        pagefrom = browser.find_element_by_id('pagDesdeTextId')
        pagelast = browser.find_element_by_id('pagHastaTextId')
        pages = pub['pages'].split('-')
        if (len(pages) > 1):
            pagefrom.send_keys(pages[0])
            pagelast.send_keys(pages[1])
        else:
            pagefrom.send_keys(0)
            pagelast.send_keys(pages[0])

    """Check if has YEAR & fill the field"""
    if 'year' in pub:
        browser.find_element_by_id(
            'annioPublicacionTextId').send_keys(pub['year'])
    else:
        browser.find_element_by_id('annioPublicacionTextId').send_keys(1900)#TODO
    """ Check if has ISBN & fill the field"""
    if 'issn' in pub:
        browser.find_element_by_id('issnTextId').send_keys(pub['issn'])

    """ Check if has D.O.I & fill the field """
    if 'doi' in pub:
        browser.find_element_by_id('doiTextId').send_keys(pub['doi'])

    # TODO
    browser.find_element_by_id('posicionSolicitanteTextId').send_keys(1)
    browser.find_element_by_class_name('col-sm-5').click()
    browser.find_element_by_xpath('//*[@data-value="2"]').click()

    """save"""
    browser.find_element_by_id('saveBtn').click()


def fillNewInproceedings(pub, browser):
    """Open new pub form """
    browser.find_element_by_id('nuevoCongreso').click()
    time.sleep(1)
    try:
        """ fill author"""
        au = browser.find_element_by_id('autoresFilter')
        addAU = browser.find_element_by_xpath('//*[@title="Añadir"]')
        for author in pub['author'].split(' and '):
            au.send_keys(author)
            addAU.click()
        """ fill Type """
        browser.find_element_by_class_name('col-sm-4').click()
        browser.find_element_by_xpath('//*[@data-value="1"]').click()
        """ fill Title"""
        browser.find_element_by_id('tituloTextId').send_keys(pub['title'])
        """ fill Name of the congress"""
        browser.find_element_by_id('denominacionTextId').send_keys(pub['note'])
        """ fill Organizer """
        browser.find_element_by_id(
            'entidadOrganizadoraTextId').send_keys(pub['organization'])
        """ fill place of congress """
        browser.find_element_by_id('lugarTextId').send_keys(pub['address'])
        """ fill date"""
        browser.find_element_by_id('fDesdeTextId').send_keys(pub['da'])
        browser.find_element_by_id('fHastaTextId').send_keys(pub['da'])
        """ fill volume """
        if 'volume' in pub:
            browser.find_element_by_id(
                'volumenTextId').send_keys(pub['volume'])
        """fill pages"""
        if 'pages' in pub:
            pagefrom = browser.find_element_by_id('pagDesdeTextId')
            pagelast = browser.find_element_by_id('pagHastaTextId')
            pages = pub['pages'].split('-')
            if (len(pages) > 1):
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
    except:
        """ Cancel publication"""
        browser.find_element_by_class_name('close').click()
