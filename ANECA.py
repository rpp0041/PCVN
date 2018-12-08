""" Needed libraries to extract and write the data
Selenium: we will use selenium to navegate through WOS web site
Time : we will use it for add delay to code execution
Getpass: use for ask user for password
"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import getpass

""" Function that will log user in to Aneca Academia Aplication"""


def login():
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


""" Configure Browser options for Selenium"""
options = Options()
options.headless = False

""" Initialize webDriver """
#browser = webdriver.Firefox(options=options)
browser = webdriver.Firefox()
browser.get('https://sede.educacion.gob.es/sede/login/inicio.jjsp')

""" Go to ACADEMIA log in web site """
Academia = browser.find_element_by_id(
    'buscadorConvocatoriasForm.descripcion.descripcion.desc')
Academia.send_keys('academia')
browser.find_element_by_id(
    'buscarConvocatoriasInicio_boton_consulta_convocatoria').click()
browser.find_element_by_id('listaConvocatoriaForm0').click()

""" Ask and check if the user & password given are correct 
if not ask for it again """
while True:
    login()
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
