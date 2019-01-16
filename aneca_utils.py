#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import urllib
from GroupFilesUtils import parse_string


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


def login(user, pswd):
    """ LOGIN"""
    se = requests.Session()

    url = 'https://sede.educacion.gob.es/sede/login/loginConv.jjsp'

    data = 'convocatoriaForm.URLCerSinRegistro=&usuarioForm.mostrarCaptcha=&usuarioForm.ultimoIntento=0&usuarioForm.minTCaptha.valor=30&convocatoriaForm.fichero.id=&convocatoriaForm.id=590&convocatoriaForm.idTema=&convocatoriaForm.urlInfo=http%3A%2F%2Fwww.mecd.gob.es%2Fservicios-al-ciudadano-mecd%2Fcatalogo%2Fgeneral%2Feducacion%2Facademia%2Fficha%2Facademia.html&convocatoriaForm.descripcion.descripcion.desc=Programa+ACADEMIA+de+acreditaci%F3n+nacional+para+el+acceso+a+los+cuerpos+docentes+universitarios&paginaAnteriorALlamada=inicio.jjsp&paginaVolver=seleccionarConvocatoria.jjsp&pagStrAC=&idIdS=1&esClave=N&nivelIdentificacionQaa=MQ%3D%3D&codigoSia=MA%3D%3D&idAplicacion=educacion&iA=no&login=' + user + '&clave=' + pswd + '&boton_entrar=Acceder'

    headers = {'Host': 'sede.educacion.gob.es',
               'Connection': 'close',
               'Content-Length': '736',
               'Cache-Control': 'max-age=0',
               'Origin': 'https://sede.educacion.gob.es',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Referer': 'https://sede.educacion.gob.es/sede/login/inicio.jjsp?idConvocatoria=590',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'es-ES,es;q=0.9'}

    a = se.post(url, headers=headers, data=data)

    if re.findall('logueado', a.text):
        print("Logged in!")
    else:
        return True

    return se


def redirect(se):
    """ FOLLOW REDIRECT """
    url2 = 'https://sede.educacion.gob.es/sede/login/accesotramiteexterno.jjsp'
    data = 'redirectUrl=https%3A%2F%2Fsrv.aneca.es%2FAcademia3%2Fsolicitudes%3Ftoken%3D&codigoConvocatoria=590'

    headers = {'Host': 'sede.educacion.gob.es',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': 'https://sede.educacion.gob.es/sede/login/loginConv.jjsp',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Connection': 'close'}

    b = se.post(url2, headers=headers, data=data)

    temp_url = b.url

    new_url = re.findall('<meta http-equiv="Refresh" content="1; URL=(.+?)">', b.text)

    """ OBTAIN CODE IDENTIFIER TO ACCESS PUBLICATION AREA"""

    headers = {
        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': temp_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9',
    }

    se2 = requests.Session()
    c = se2.get(new_url[0], headers=headers)

    other_url = re.findall('<li><a href="(.+?)">Calidad y dif', c.text)

    return se2, new_url, other_url


def acces_publication_area(se2, new_url, other_url):
    """ ACCES TO PUBLICATIONS AREA (GET)"""
    headers = {

        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': new_url[0],
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9'

    }

    final_url = "https://srv.aneca.es" + other_url[0]

    d = se2.get(final_url, headers=headers)
    return se2, d, headers, final_url


def add_no_idx(se2, d, headers, final_url, l, author_input, db_salida, pbar, pbar_inc):
    no_dix = re.findall(
        '<a id="nuevaPublicacionNoIdxId" onclick="cargarModal\(this\);return false;" href="(.+?)" title="Nuevo">',
        d.text)

    url_noidx = "https://srv.aneca.es" + no_dix[0]

    f = se2.get(url_noidx, headers=headers)

    value_for_post = re.findall('<input type="hidden" name="_HDIV_STATE_" value="(.+?)" /></form>', f.text)

    posturl = 'https://srv.aneca.es/Academia3/actInvestigadora/calidadDifusion/guardarPublicacionNoIndexada'
    newheaders = {
        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Accept': '*/*',
        'Origin': 'https://srv.aneca.es',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': final_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    for x in l:
        post_data_test = post_article_no_index(x, value_for_post[0], author_input)
        test_request = se2.post(posturl, headers=newheaders, data=post_data_test)

        if test_request.text != '':
            print('FAILED!')
            db_salida.entries.append(x)
        else:
            print('SUCCESSED!')
        """ update progress bar GUI"""
        pbar['value'] += pbar_inc
        pbar.update()
    return se2, d


def post_article_no_index(pub, value_for_post, author_input):
    num_author = len(pub['author'].split('and'))
    pos_author = author_position(pub['author'], author_input)
    postdata = ''
    postdata += 'totalAutores=' + str(num_author) + '&'
    postdata += 'publicacionNoIndexada.posAutor=' + str(pos_author) + '&'
    postdata += 'publicacionNoIndexada.tipoPubliCient.id=1&'

    if 'doi' in pub.keys():
        postdata += 'publicacionNoIndexada.doi=' + urllib.parse.quote(pub['doi']) + '&'
    if 'title' in pub.keys():
        postdata += 'publicacionNoIndexada.titulo=' + urllib.parse.quote(pub['title']) + '&'
    if 'journal' in pub.keys():
        postdata += 'publicacionNoIndexada.nombre=' + urllib.parse.quote(pub['journal']) + '&'
    if 'volume' in pub.keys():
        postdata += 'publicacionNoIndexada.volumen=' + pub['volume'] + '&'
    if 'pages' in pub.keys():
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            postdata += 'publicacionNoIndexada.paginaDesde=' + pages[0] + '&'
            postdata += 'publicacionNoIndexada.paginaHasta=' + pages[1] + '&'
        else:
            postdata += 'publicacionNoIndexada.paginaDesde=' + pages[0] + '&'
            postdata += 'publicacionNoIndexada.paginaHasta=' + pages[0] + '&'

    if 'publisher' in pub.keys():
        postdata += 'publicacionNoIndexada.editorial=' + urllib.parse.quote(pub['publisher']) + '&'
    postdata += 'publicacionNoIndexada.pais.id=194&'
    if 'year' in pub.keys():
        postdata += 'publicacionNoIndexada.annio=' + pub['year'] + '&'
    if 'issn' in pub.keys():
        postdata += 'publicacionNoIndexada.issn=' + pub['issn'] + '&'
    postdata += '_HDIV_STATE_=' + value_for_post + '&'
    postdata += 'autores=' + urllib.parse.quote(pub['author']).replace('and', '%3B%3D')

    return postdata.encode("utf-8", "replace")


def add_idx(se2, d, headers, final_url, l, author_input, db_salida, pbar, pbar_inc):
    no_dix = re.findall(
        '<a id="nuevaPublicacionIdxId" onclick="cargarModal\(this\);return false;" href="(.+?)" title="Nuevo">', d.text)

    url_noidx = "https://srv.aneca.es" + no_dix[0]

    f = se2.get(url_noidx, headers=headers)

    value_for_post = re.findall('<input type="hidden" name="_HDIV_STATE_" value="(.+?)" /></form>', f.text)

    posturl = 'https://srv.aneca.es/Academia3/actInvestigadora/calidadDifusion/guardarPublicacionIndexada'

    newheaders = {
        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Accept': '*/*',
        'Origin': 'https://srv.aneca.es',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': final_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    for x in l:
        post_data_test = post_article_index(x, value_for_post[0], author_input)
        test_request = se2.post(posturl, headers=newheaders, data=post_data_test)

        if test_request.text != '':
            print('FAILED!')
            db_salida.entries.append(x)
        else:
            print('SUCCESSED!')
        """ update progress bar GUI"""
        pbar['value'] += pbar_inc
        pbar.update()

    return se2, d


def post_article_index(pub, value_for_post, author_input):
    num_author = len(pub['author'].split('and'))
    pos_author = author_position(pub['author'], author_input)
    postdata = ''
    postdata += 'totalAutores=' + str(num_author) + '&'
    postdata += 'publicacionIndexada.posAutor=' + str(pos_author) + '&'
    postdata += 'publicacionIndexada.tipoPubliCient.id=1&'
    """ 
    if 'doi' in pub.keys():
        postdata+='publicacionIndexada.doi='+pub['doi']+'&'
    """
    if 'title' in pub.keys():
        postdata += 'publicacionIndexada.titulo=' + urllib.parse.quote(pub['title']) + '&'
    if 'journal' in pub.keys():
        postdata += 'publicacionIndexada.nombre=' + urllib.parse.quote(pub['journal']) + '&'
    if 'volume' in pub.keys():
        postdata += 'publicacionIndexada.volumen=' + pub['volume'] + '&'
    if 'pages' in pub.keys():
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            postdata += 'publicacionIndexada.paginaDesde=' + pages[0] + '&'
            postdata += 'publicacionIndexada.paginaHasta=' + pages[1] + '&'
        else:
            postdata += 'publicacionIndexada.paginaDesde=' + pages[0] + '&'
            postdata += 'publicacionIndexada.paginaHasta=' + pages[0] + '&'
    if 'publisher' in pub.keys():
        postdata += 'publicacionIndexada.editorial=' + urllib.parse.quote(pub['publisher']) + '&'
    postdata += 'publicacionIndexada.pais.id=194&'
    if 'year' in pub.keys():
        postdata += 'publicacionIndexada.annio=' + pub['year'] + '&'
    if 'issn' in pub.keys():
        postdata += 'publicacionIndexada.issn=' + urllib.parse.quote(pub['issn']) + '&'

    """ Fill journal rank position """
    # split on '\n' for cases where journal of publications correspond to more than one category
    position = pub['journalrank'].split('\n')
    category = pub['journalcategory'].split('\n')
    quartile = pub['journalquartile'].split('\n')
    tertile = pub['journaltertile'].split('\n')
    # Flag that will indicate if quality indexes had been add or not
    # go trough all the categories
    for x in range(0, len(position)):
        # try to fill the fields , but if date is None pop data from list and try with next
        # else the data is correct ,so set quality index flag to True and break Loop
        if position[0] == 'None':
            position.pop(0)
            category.pop(0)
            quartile.pop(0)
            tertile.pop(0)
        else:
            pos1 = position[0].split('/')
            postdata += 'publicacionIndexada.posRevista=' + pos1[0] + '&'
            postdata += 'publicacionIndexada.posRevistaMax=' + pos1[1] + '&'
            postdata += 'publicacionIndexada.categoria=' + urllib.parse.quote(category[0]) + '&'
            postdata += 'publicacionIndexada.tercil=T' + tertile[0] + '&'
            postdata += 'publicacionIndexada.cuartil=' + quartile[0][1] + '&'

            """ Fill Other information """
            if len(position) > 1:
                other_information = ''
                for x in range(1, len(position)):
                    other_information += 'rank ' + position[x]
                    other_information += 'quartile ' + quartile[x]
                    other_information += 'tertile ' + tertile[x]
                    other_information += 'Category ' + category[x]

                postdata += 'publicacionIndexada.otros=' + urllib.parse.quote(other_information) + '&'

            break

    postdata += 'publicacionIndexada.baseDatos=Web of Science&'
    postdata += 'publicacionIndexada.indiceImpacto=' + pub['impactindex'] + '&'
    postdata += 'publicacionIndexada.citasJcr=' + pub['cites'] + '&'
    postdata += '_HDIV_STATE_=' + value_for_post + '&'
    postdata += 'autores=' + urllib.parse.quote(pub['author']).replace('and', '%3B%3D')

    return postdata.encode("utf-8", "replace")


def add_book(se2, d, headers, final_url, l, author_input, db_salida, pbar, pbar_inc):
    book = re.findall(
        '<a id="nuevLibroCapituloId" onclick="cargarModal\(this\);return false;" href="(.+?)" title="Nuevo">', d.text)
    url_book = "https://srv.aneca.es" + book[0]

    f = se2.get(url_book, headers=headers)

    value_for_post = re.findall('<input type="hidden" name="_HDIV_STATE_" value="(.+?)" /></form>', f.text)

    posturl = 'https://srv.aneca.es/Academia3/actInvestigadora/calidadDifusion/guardarLibroCapitulo'

    newheaders = {
        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Accept': '*/*',
        'Origin': 'https://srv.aneca.es',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': final_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    for x in l:
        post_data_test = post_book(x, value_for_post[0], author_input)
        test_request = se2.post(posturl, headers=newheaders, data=post_data_test)

        if test_request.text != '':
            print('FAILED!')
            db_salida.entries.append(x)
        else:
            print('SUCCESSED!')
        """ update progress bar GUI"""
        pbar['value'] += pbar_inc
        pbar.update()

    return se2, d


def post_book(pub, value_for_post, author_input):
    num_author = len(pub['author'].split('and'))
    pos_author = author_position(pub['author'], author_input)
    postdata = ''
    postdata += 'totalAutores=' + str(num_author) + '&'
    postdata += 'libroCapitulo.posAutor=' + str(pos_author) + '&'
    postdata += 'libroCapitulo.tipoLibroCapi.id=2&'

    if 'doi' in pub.keys():
        postdata += 'libroCapitulo.doi=' + urllib.parse.quote(pub['doi']) + '&'
    if 'title' in pub.keys():
        postdata += 'libroCapitulo.titulo=' + urllib.parse.quote(pub['title']) + '&'
    if 'volume' in pub.keys():
        postdata += 'libroCapitulo.volumen=' + pub['volume'] + '&'
    if 'pages' in pub.keys():
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            postdata += 'libroCapitulo.paginaDesde=' + pages[0] + '&'
            postdata += 'libroCapitulo.paginaHasta=' + pages[1] + '&'
        else:
            postdata += 'libroCapitulo.paginaDesde=' + pages[0] + '&'
            postdata += 'libroCapitulo.paginaHasta=' + pages[0] + '&'

    if 'publisher' in pub.keys():
        postdata += 'libroCapitulo.editorial=' + urllib.parse.quote(pub['publisher']) + '&'
    postdata += 'libroCapitulo.pais.id=194&'
    if 'year' in pub.keys():
        postdata += 'libroCapitulo.annio=' + pub['year'] + '&'
    if 'issn' in pub.keys():
        postdata += 'libroCapitulo.issn=' + pub['issn'] + '&'
    if 'cites' in pub.keys():
        postdata += 'libroCapitulo.citas=' + pub['cites'] + '&'
    postdata += '_HDIV_STATE_=' + value_for_post + '&'
    postdata += 'autores=' + urllib.parse.quote(pub['author']).replace('and', '%3B%3D')

    return postdata.encode("utf-8", "replace")


def add_inprocedings(se2, d, headers, final_url, l, db_salida, pbar, pbar_inc):
    book = re.findall('<a id="nuevoCongreso" onclick="cargarModal\(this\);return false;" href="(.+?)" title="Nuevo">',
                      d.text)
    url_book = "https://srv.aneca.es" + book[0]

    f = se2.get(url_book, headers=headers)

    value_for_post = re.findall('<input type="hidden" name="_HDIV_STATE_" value="(.+?)" /></form>', f.text)

    posturl = 'https://srv.aneca.es/Academia3/actInvestigadora/calidadDifusion/guardarCongreso'
    newheaders = {
        'Host': 'srv.aneca.es',
        'Connection': 'close',
        'Accept': '*/*',
        'Origin': 'https://srv.aneca.es',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': final_url,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    for x in l:
        post_data_test = post_inprocedings(x, value_for_post[0])
        test_request = se2.post(posturl, headers=newheaders, data=post_data_test)

        if test_request.text != '':
            print('FAILED!')
            db_salida.entries.append(x)
        else:
            print('SUCCESSED!')
        """ update progress bar GUI"""
        pbar['value'] += pbar_inc
        pbar.update()

    return se2, d


def post_inprocedings(pub, value_for_post):
    postdata = ''
    postdata += 'congreso.tipoParticipacion.id=6&'

    if 'title' in pub.keys():
        postdata += 'congreso.titulo=' + urllib.parse.quote(pub['title']) + '&'
    if 'note' in pub.keys():
        postdata += 'congreso.denominacion=' + urllib.parse.quote(pub['note']) + '&'
    if 'organization' in pub.keys():
        postdata += 'congreso.entidadOrga=' + urllib.parse.quote(pub['organization']) + '&'
    if 'address' in pub.keys():
        postdata += 'congreso.lugar==' + urllib.parse.quote(pub['address']) + '&'
    if 'da' in pub.keys():
        da_split = pub['da'].split('-')
        da = da_split[1] + '%2F' + da_split[2] + '%2F' + da_split[0]
        postdata += 'congreso.inicio=' + da + '&'
        postdata += 'congreso.fin=' + da + '&'
    if 'issn' in pub.keys():
        postdata += 'congreso.publicacion=' + urllib.parse.quote(pub['issn']) + '&'
    elif 'isbn' in pub.keys():
        postdata += 'congreso.publicacion=' + urllib.parse.quote(pub['isbn']) + '&'
    if 'volume' in pub.keys():
        postdata += 'congreso.volumen=' + pub['volume'] + '&'
    if 'pages' in pub.keys():
        pages = pub['pages'].split('-')
        if len(pages) > 1:
            postdata += 'congreso.paginaDesde=' + pages[0] + '&'
            postdata += 'congreso.paginaHasta=' + pages[1] + '&'
        else:
            postdata += 'congreso.paginaDesde=' + pages[0] + '&'
            postdata += 'congreso.paginaHasta=' + pages[0] + '&'

    postdata += '_HDIV_STATE_=' + value_for_post + '&'
    postdata += 'autores=' + urllib.parse.quote(pub['author']).replace('and', '%3B%3D')

    return postdata.encode("utf-8", "replace")
