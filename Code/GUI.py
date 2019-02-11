#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk, ImageFont
from GetPublicationsScholar import *
from GetPublicationsScopus import *
from GetPublicationsWOS import *
from GroupFiles import *
from aneca import *
from aneca_utils import login
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ConnectionError
import textwrap
import tkinter.messagebox
import sys
import subprocess
import traceback
import datetime


def info_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""
    def func(event):
        return_au()

    window.bind('<Return>', func)
    def return_au():
        # rest entry border color
        reset_entry(entry_google_scholar, entry_scopus, entry_wos, entry_user, entry_pswd)

        global au_google, au_scopus, au_wos, user, pswd
        user = entry_user.get()
        pswd = entry_pswd.get()
        au_google = entry_google_scholar.get()
        au_scopus = entry_scopus.get()
        au_wos = entry_wos.get()

        # Check if entry len is bigger than 0
        if check_entry(entry_google_scholar, entry_scopus, entry_wos):
            return

        if login(user, pswd) is True:
            error = tkinter.messagebox.showerror(title="Error",
                                                 message="Usuario o Contraseña Incorrectos \nPor favor introduzca los datos de nuevo")

            # delete input and set red border to indicate the user what is wrong
            entry_user.delete(0, 'end')
            entry_user.config(highlightbackground="red", highlightthickness=2)

            entry_pswd.delete(0, 'end')
            entry_pswd.config(highlightbackground="red", highlightthickness=2)

        else:
            x, y = get_window_pos(window)
            window.destroy()
            google_search(x, y)

    txt = "Cuando se pulse el botón 'Comenzar', se procederá a la búsqueda de los datos referentes al autor introducido, si durante el proceso ocurriera algún problema con los datos introducidos, podrá introducirlos nuevamente."
    # Background
    bg = Background(window, txt, 'background1.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # ///////// Google Scholar Entry /////////#
    # Label
    label_google_scholar = Label(frame, text="Google Scholar Author:")
    font = ('times', 15)
    label_google_scholar.config(font=font)
    label_google_scholar.grid(row=0, column=0, sticky=E)
    # Entry
    entry_google_scholar = Entry(frame, width=50)
    entry_google_scholar.grid(row=0, column=1)

    # ///////// Scopus Entry /////////#
    # Label
    label_scopus = Label(frame, text="Scopus Author ID:")
    label_scopus.config(font=font)
    label_scopus.grid(row=1, column=0, sticky=E)
    # Entry
    entry_scopus = Entry(frame, width=50)
    entry_scopus.grid(row=1, column=1)

    # ///////// WOS Entry /////////#
    # Label
    label_wos = Label(frame, text="WOS Author Name:")
    label_wos.config(font=font)
    label_wos.grid(row=2, column=0, sticky=E)
    # Entry
    entry_wos = Entry(frame, width=50)
    entry_wos.grid(row=2, column=1, pady=10)

    # Label Academia
    label_academia = Label(frame, text='Acceso a ACADEMIA')
    label_academia.config(font=font)
    label_academia.grid(columnspan=2, sticky=S)

    # Label User
    label_user = Label(frame, text="Usuario:")
    label_user.config(font=font)
    label_user.grid(row=5, column=0, sticky=E)
    # Entry User
    entry_user = Entry(frame, width=30)
    entry_user.grid(row=5, column=1, sticky=W)

    # Label Password
    label_pswd = Label(frame, text="Contraseña:")
    label_pswd.config(font=font)
    label_pswd.grid(row=6, column=0, sticky=E)
    # Entry Password
    entry_pswd = Entry(frame, width=20)
    entry_pswd.grid(row=6, column=1, sticky=W)
    entry_pswd.config(show="*")  # Make password invisible

    # //////////////////////////////////////////////
    # Search Button
    bt_scopus = Button(frame, text="Comenzar", height=1, width=30, command=return_au)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.grid(columnspan=2, sticky=N, pady=20)

    window, frame = center_frame(window, frame)

    window.mainloop()


def get_only_info_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        return_au()

    window.bind('<Return>', func)

    def return_au():
        # rest entry border color
        entry_google_scholar.config(highlightthickness=0)
        entry_scopus.config(highlightthickness=0)
        entry_wos.config(highlightthickness=0)

        global au_google, au_scopus, au_wos
        au_google = entry_google_scholar.get()
        au_scopus = entry_scopus.get()
        au_wos = entry_wos.get()

        # Check if entry len is bigger than 0
        if check_entry(entry_google_scholar, entry_scopus, entry_wos) is False:
            x, y = get_window_pos(window)
            window.destroy()
            google_search(x, y)

    txt = "Cuando se pulse el botón 'Comenzar', se procederá a la búsqueda de los datos referentes al autor introducido, si durante el proceso ocurriera algún problema con los datos introducidos, podrá introducirlos nuevamente."
    # Background
    bg = Background(window, txt, 'background_ext1.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # ///////// Google Scholar Entry /////////#
    # Label
    label_google_scholar = Label(frame, text="Google Scholar Author:")
    font = ('times', 15)
    label_google_scholar.config(font=font)
    label_google_scholar.grid(row=0, column=0, sticky=E)
    # Entry
    entry_google_scholar = Entry(frame, width=50)
    entry_google_scholar.grid(row=0, column=1)

    # ///////// Scopus Entry /////////#
    # Label
    label_scopus = Label(frame, text="Scopus Author ID:")
    label_scopus.config(font=font)
    label_scopus.grid(row=1, column=0, sticky=E)
    # Entry
    entry_scopus = Entry(frame, width=50)
    entry_scopus.grid(row=1, column=1)

    # ///////// WOS Entry /////////#
    # Label
    label_wos = Label(frame, text="WOS Author Name:")
    label_wos.config(font=font)
    label_wos.grid(row=2, column=0, sticky=E)
    # Entry
    entry_wos = Entry(frame, width=50)
    entry_wos.grid(row=2, column=1, pady=10)

    # //////////////////////////////////////////////
    # Search Button
    bt_scopus = Button(frame, text="Comenzar", height=1, width=30, command=return_au)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.grid(columnspan=2, sticky=N, pady=20)

    window, frame = center_frame(window, frame)

    window.mainloop()


""" Fucntion that will show process of data scrapping in Google Scholar """


def google_search(x, y):
    window = Tk()
    window = set_window(window, x, y)

    def get_scholar_pub():
        # place progressbar in window
        pbar_google_scholar.place(x=200, y=400)
        pbar_google_scholar.update()
        pbar_google_scholar['maximum'] = 100
        # Call function to retrieve publications
        try:
            get_publications_scholar(au_google, pbar_google_scholar, num_var, max_p)
        except StopIteration:
            pbar_google_scholar.stop()
            answer = tkinter.messagebox.askyesno('Sin resultados',
                                                 'No se han encontrado resultados \n ¿Desea Volver a buscar?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                google_window(x, y)
            else:
                window.destroy()
        except ConnectionError:
            pbar_google_scholar.stop()
            answer = tkinter.messagebox.askyesno('Error de Conexión',
                                                 'Ha ocurrido un error con la conexión \n ¿Desea Volver a intentarlo?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                google_search(x, y)
            else:
                window.destroy()
        except:
            pbar_google_scholar.stop()
            # Write error to log file
            logfile = open("log.txt", "a")
            logfile.write('\n\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
            traceback.print_exc(file=logfile)
            logfile.close()
            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 "Ha ocurrido un error inesperado\n La descripción completa del error ha sido guardad en 'log.txt'\n ¿Desea abrir el archivo?")
            if answer:
                open_file('log.txt')

            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 '¿Desea volver a intentar el proceso donde\n se produjo el error?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                google_search(x, y)
            else:
                window.destroy()
        else:
            pbar_google_scholar.stop()
            # Destroy Window
            x, y = get_window_pos(window)
            window.destroy()
            scopus_search(x, y)

    # Background
    txt = "Actualmente, se está realizando la obtención de los datos desde GOOGLE SCHOLAR.\n Cuando se termine el proceso, comenzará automáticamente la búsqueda en Scopus."
    if log_flag:
        bg = Background(window, txt, 'background2.png')
    else:
        bg = Background(window, txt, 'background_ext2.png')
    # Menu
    menu = GuiMenu(window)

    # Numb publications label
    num_var = StringVar()
    num_var.set('Número de publicaciones obtenidas:\n')
    num_label = Label(window, textvariable=num_var)
    num_font = ('times', 18)
    num_label.config(font=num_font)
    num_label.place(x=220, y=300)
    # Progress Bar
    pbar_google_scholar = ttk.Progressbar(window, mode='determinate', length=400)
    # Get publications
    get_scholar_pub()

    window.mainloop()


""" Function tha will ask again for user input for Google Scholar author, if at first try it does not work"""


def google_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        retry()

    window.bind('<Return>', func)
    """ Function to be executed when click search button"""

    def retry():
        # author name , will be used later
        global au_google
        au_google = entry_google_scholar.get()
        x, y = get_window_pos(window)
        window.destroy()
        google_search(x, y)

    # backGround Image
    if log_flag:
        bg = Background(window, '', 'background2.png')
    else:
        bg = Background(window, '', 'background_ext2.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # ///////// Google Scholar Entry /////////#
    # Label
    label_google_scholar = Label(frame, text="Google Scholar Author:")
    font = ('times', 15)
    label_google_scholar.config(font=font)
    label_google_scholar.grid(row=0, column=0, sticky=E)
    # Entry
    entry_google_scholar = Entry(frame, width=50)
    entry_google_scholar.grid(row=0, column=1)

    # //////////////////////////////////////////////
    # Search Button
    bt_google_scholar = Button(frame, text="Buscar", height=1, width=20, command=retry)
    bfont = ('times', 17)
    bt_google_scholar.config(font=bfont)
    bt_google_scholar.grid(columnspan=2, pady=15)

    window.mainloop()


""" Fucntion that will show process of data scrapping in Scopus"""


def scopus_search(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def get_scopus_pub():
        # Place progress bar in window
        pbar_scopus.place(x=200, y=300)
        pbar_scopus.update()
        pbar_scopus['maximum'] = 100
        # Call function to retrieve publications
        try:
            if get_publications_scopus(au_scopus, pbar_scopus):
                pbar_scopus.stop()
                answer = tkinter.messagebox.askyesno('Sin resultados',
                                                     'No se han encontrado resultados \n ¿Desea Volver a buscar?')
                if answer:
                    x, y = get_window_pos(window)
                    window.destroy()
                    scopus_window(x, y)
                else:
                    window.destroy()
        except (KeyError, NoSuchElementException, ConnectionError):
            answer = tkinter.messagebox.askyesno('Error de Conexión',
                                                 'Ha ocurrido un error con la conexión \n ¿Desea Volver a intentarlo?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                scopus_search(x, y)
            else:
                window.destroy()
        except:
            # Write error to log file
            logfile = open("log.txt", "a")
            logfile.write('\n\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
            traceback.print_exc(file=logfile)
            logfile.close()
            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 "Ha ocurrido un error inesperado\n La descripción completa del error ha sido guardad en 'log.txt'\n ¿Desea abrir el archivo?")
            if answer:
                open_file('log.txt')

            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 '¿Desea volver a intentar el proceso donde\n se produjo el error?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                scopus_search(x, y)
            else:
                window.destroy()
        else:
            x, y = get_window_pos(window)
            window.destroy()
            wos_search(x, y)

    # Menu
    menu = GuiMenu(window)
    # backGround
    text = "Actualmente, se está realizando la obtención de los datos desde SCOPUS.\n Cuando se termine el proceso, comenzará automáticamente la búsqueda en Web of Science."
    if log_flag:
        bg = Background(window, text, 'background3.png')
    else:
        bg = Background(window, text, 'background_ext3.png')

    # Progress Bar
    pbar_scopus = ttk.Progressbar(window, mode='determinate', length=400)
    # Label information

    # get publications
    get_scopus_pub()
    window.mainloop()


""" Function tha will ask again for user input for Scopus author, if at first try it does not work"""


def scopus_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        retry()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def retry():
        # author name , will be used later
        global au_scopus
        au_scopus = entry_scopus.get()
        x, y = get_window_pos(window)
        window.destroy()
        scopus_search(x, y)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # backGround Image
    if log_flag:
        bg = Background(window, '', 'background3.png')
    else:
        bg = Background(window, '', 'background_ext3.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # ///////// Scopus Entry /////////#
    # Label
    label_scopus = Label(frame, text="Scopus Author ID:")
    font = ('times', 15)
    label_scopus.config(font=font)
    label_scopus.grid(row=0, column=0, sticky=E)
    # Entry
    entry_scopus = Entry(frame, width=50)
    entry_scopus.grid(row=0, column=1)

    # //////////////////////////////////////////////
    # Search Button
    bt_scopus = Button(frame, text="Buscar", height=1, width=20, command=retry)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.grid(columnspan=2, pady=15)

    window.mainloop()


""" Fucntion that will show process of data scrapping in WOS """


def wos_search(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def get_wos_pub():
        # Place progressbar in window
        pbar_wos.place(x=200, y=300)
        pbar_wos.update()
        pbar_wos['maximum'] = 100
        try:
            # Call function to retrieve publications
            if get_publications_wos(au_wos, pbar_wos):
                pbar_wos.stop()
                answer = tkinter.messagebox.askyesno('Sin resultados',
                                                     'No se han encontrado resultados \n ¿Desea Volver a buscar?')
                if answer:
                    x, y = get_window_pos(window)
                    window.destroy()
                    wos_window(x, y)
                else:
                    window.destroy()
            else:
                pbar_wos.stop()
                # Destroy window
                x, y = get_window_pos(window)
                window.destroy()
                group_window(x, y)
        except ConnectionError:
            answer = tkinter.messagebox.askyesno('Error de Conexión',
                                                 'Ha ocurrido un error con la conexión \n ¿Desea Volver a intentarlo?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                wos_search(x, y)
            else:
                window.destroy()
        except:
            # Write error to log file
            logfile = open("log.txt", "a")
            logfile.write('\n\n'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
            traceback.print_exc(file=logfile)
            logfile.close()
            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 "Ha ocurrido un error inesperado\n La descripción completa del error ha sido guardad en 'log.txt'\n ¿Desea abrir el archivo?")
            if answer:
                open_file('log.txt')
            answer = tkinter.messagebox.askyesno('Error inesperado',
                                                 '¿Desea volver a intentar el proceso donde\n se produjo el error?')
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                wos_search(x, y)
            else:
                window.destroy()

    # Background
    text = "Actualmente, se está realizando la obtención de los datos desde WEB OF SCIENCE.\n Cuando se termine el proceso, comenzará automáticamente el tratamiento de datos."
    if log_flag:
        bg = Background(window, text, 'background4.png')
    else:
        bg = Background(window, text, 'background_ext4.png')
    # Menu
    menu = GuiMenu(window)

    # Progress Bar
    pbar_wos = ttk.Progressbar(window, mode='determinate', length=400)
    # Get Publicatiosn
    get_wos_pub()
    window.mainloop()


def wos_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        retry()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def retry():
        # author name , will be used later
        global au_wos
        au_wos = entry_wos.get()
        x, y = get_window_pos(window)
        window.destroy()
        wos_search(x, y)

    # backGround Image
    if log_flag:
        bg = Background(window, '', 'background4.png')
    else:
        bg = Background(window, '', 'background_ext4.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # ///////// WOS /////////#
    # Label
    label_wos = Label(frame, text="WOS Author name:")
    font = ('times', 15)
    label_wos.config(font=font)
    label_wos.grid(row=0, column=0, sticky=E)
    # Entry
    entry_wos = Entry(frame, width=50)
    entry_wos.grid(row=0, column=1)

    # //////////////////////////////////////////////
    # Search Button
    bt_wos = Button(frame, text="Buscar", height=1, width=20, command=retry)
    bfont = ('times', 17)
    bt_wos.config(font=bfont)
    bt_wos.grid(columnspan=2, pady=15)

    window.mainloop()

    window.mainloop()


""" Function that will show window indicating the user that 
the process of Grouping files and parsing is taking place """


def group_window(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that will place progress bar and start 
    groupfiles process"""

    def groupfiles():
        # Place progressbar in window
        pbar_g_files.place(x=200, y=250)
        pbar_g_files.update()
        pbar_g_files['maximum'] = 100
        # Call function that group & parse files
        group_files(pbar_g_files, max_p)

        pbar_g_files.stop()
        # Destroy window
        x, y = get_window_pos(window)
        window.destroy()
        aneca_window(au_google, x, y)

    # backGround

    if log_flag:
        text = "Se está procediendo al tratamiento de los datos, eliminación de elementos duplicados y agrupación en un solo fichero.\n Cuando se termine, comenzará el proceso de subida a ACADEMIA."
        bg = Background(window, text, 'background5.png')
    else:
        text = "Se está procediendo al tratamiento de los datos, eliminación de elementos duplicados y agrupación en un solo fichero.\n Este es el último paso del proceso."
        bg = Background(window, text, 'background_ext5.png')
    # Menu
    menu = GuiMenu(window)

    # Progress BarF
    pbar_g_files = ttk.Progressbar(window, mode='determinate', length=400)

    groupfiles()

    window.mainloop()

    """ Function that will show the user a window to log in in Academia 
    these credential will be later use in Aneca() """


def aneca_login(x, y):
    window = Tk()
    window = set_window(window, x, y)
    """ Function that get data from entries """

    def get_login():
        # needed global variables for use in other windows process
        global user, pswd, au_google

        au_google = entry_autor.get()
        user = entry_user.get()
        pswd = entry_pswd.get()
        # Destroy window
        x, y = get_window_pos(window)
        window.destroy()
        aneca_window(au_google, x, y)

    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_login()

    window.bind('<Return>', func)

    # Background
    bg = Background(window, '', 'background_subir2.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=50)

    # Label Author
    label_autor = Label(frame, text="Nombre de autor:")
    font = ('times', 15)
    label_autor.config(font=font)
    label_autor.grid(row=0, column=0, sticky=E)
    # Entry Author
    entry_autor = Entry(frame, width=30)
    entry_autor.grid(row=0, column=1, sticky=W)

    # Label Academia
    label_academia = Label(frame, text='Acceso a ACADEMIA')
    label_academia.config(font=font)
    label_academia.grid(columnspan=2, sticky=S)

    # Label User
    label_user = Label(frame, text="Usuario:")
    label_user.config(font=font)
    label_user.grid(row=2, column=0, sticky=E)
    # Entry User
    entry_user = Entry(frame, width=30)
    entry_user.grid(row=2, column=1, sticky=W)

    # Label Password
    label_pswd = Label(frame, text="Contraseña:")
    label_pswd.config(font=font)
    label_pswd.grid(row=3, column=0, sticky=E)
    # Entry Password
    entry_pswd = Entry(frame, width=20)
    entry_pswd.grid(row=3, column=1, sticky=W)
    entry_pswd.config(show="*")  # Make password invisible

    # //////////////////////////////////////////////
    # Search Button
    bt_scopus = Button(frame, text="Login", height=1, width=20, command=get_login)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.grid(columnspan=2, sticky=N, pady=20)

    window, frame = center_frame(window, frame)

    window.mainloop()


""" Function that will log the user in Academia and start process to 
upload all data stored previously to platform
will also show a window for login, and later will show a window
indicating the progress taken """


def aneca_window(author, x, y):
    if log_flag is False:
        completed_window(x, y)
        return ()
    window = Tk()
    window = set_window(window, x, y)
    """ Function that will place progress bar and start 
    upload process"""

    def start_aneca():
        # Place progressbar in window
        pbar_aneca.place(x=220, y=300)
        pbar_aneca.update()
        pbar_aneca['maximum'] = 100
        # Call Aneca function to start upload process
        global total, failed
        total = failed = 0
        try:
            total, failed = aneca(author, pbar_aneca, user, pswd, num_var, total, failed)
            if total is True:
                error = tkinter.messagebox.showerror(title="Error",
                                                     message="Usuario o Contraseña Incorrectos \nPor favor introduzca los datos de nuevo")
                x, y = get_window_pos(window)
                window.destroy()
                aneca_login(x, y)
        except FileNotFoundError:
            answer = tkinter.messagebox.askyesno(title="Archivo no encontrado",
                                                 message="No se encuentra el archivo 'todas.bib'\n Por favor asegúrese que el archivo \nse encuentra en el directorio y está correctamente nombrado\n¿Desea volver a intentarlo?")
            if answer:
                x, y = get_window_pos(window)
                window.destroy()
                aneca_window(x, y)
            else:
                window.destroy()
        else:
            pbar_aneca.stop()
            x, y = get_window_pos(window)
            # Destroy Window
            window.destroy()
            completed_window(x, y)

    # backGround
    text = "Se está procediendo a la subida de los datos a ACADEMIA.\n Este es el último paso del proceso, cuando termine, se mostrará cuantas publicaciones pudieron ser subidas. Las que no se hayan podido subir, se guardarán en un fichero para su subida manual"
    if ext_flag:
        bg = Background(window, text, 'background6.png')
    else:
        bg = Background(window, text, 'background_subir3.png')
    # Menu
    menu = GuiMenu(window)

    # Numb publications label
    num_var = StringVar()
    num_var.set('Número de publicaciones subidas:\n')
    num_label = Label(window, textvariable=num_var)
    num_font = ('times', 18)
    num_label.config(font=num_font)
    num_label.place(x=220, y=200)
    # Progress Bar
    pbar_aneca = ttk.Progressbar(window, mode='determinate', length=400)

    # Start Aneca
    start_aneca()

    window.mainloop()


def completed_window(x, y):
    window = Tk()
    window = set_window(window, x, y)

    def end_gui():
        # Destroy Window
        window.destroy()

    def open_pub():
        open_file('pendientes.bib')

    def open_pub_extract():
        open_file('todas.bib')

    def execute_again():
        max_p = 10000
        log_flag = True
        ext_flag = True
        x, y = get_window_pos(window)
        window.destroy()
        info_window(x, y)

    # backGround
    if log_flag:
        text = 'Número de publicaciones que no pudieron ser subidas:\n' + str(failed) + '/' + str(total)
        if ext_flag:
            bg = Background(window, text, 'background7.png')
        else:
            bg = Background(window, text, 'background_subir4.png')
    else:
        bg = Background(window, '', 'background_ext5.png')
    # Menu #
    menu = GuiMenu(window)

    # Frame
    frame = Frame(borderwidth=15)
    frame.place(x=135, y=100)

    # ///////// END Label /////////#
    # Label
    label_completed = Label(frame, text="Proceso finalizado")
    font = ('times', 25)
    label_completed.config(font=font)
    label_completed.grid(row=0, column=0, sticky=E)

    # ///////// Close Button /////////#
    bt_close = Button(frame, text="Cerrar Aplicación", height=1, width=18, command=end_gui)
    bfont = ('times', 17)
    bt_close.config(font=bfont)
    bt_close.grid(columnspan=2, pady=15)
    # ///////// Execute again Button /////////#
    bt_close = Button(frame, text="Volver a Ejecutar", height=1, width=18, command=execute_again)
    bt_close.config(font=bfont)
    bt_close.grid(columnspan=2, pady=15)
    # ///////// Open Publications Button /////////#
    if log_flag:
        bt_open = Button(frame, text="Abrir publicaciones\n Erroneas", height=1, width=18, command=open_pub)
    else:
        bt_open = Button(frame, text="Abrir publicaciones\n Extraídas", height=1, width=18, command=open_pub_extract)
    bt_open.config(font=bfont)
    bt_open.grid(columnspan=2, pady=15)

    window, frame = center_frame(window, frame)
    window.mainloop()


def check_entry(entry_google_scholar, entry_scopus, entry_wos):
    flag = False
    if len(au_google) < 1:
        # delete input and set red border to indicate the user what is wrong
        entry_google_scholar.delete(0, 'end')
        entry_google_scholar.config(highlightbackground="red", highlightthickness=2)
        flag = True
    if len(au_scopus) < 1:
        # delete input and set red border to indicate the user what is wrong
        entry_scopus.delete(0, 'end')
        entry_scopus.config(highlightbackground="red", highlightthickness=2)
        flag = True
    if len(au_wos) < 1:
        # delete input and set red border to indicate the user what is wrong
        entry_wos.delete(0, 'end')
        entry_wos.config(highlightbackground="red", highlightthickness=2)
        flag = True

    return flag


def reset_entry(entry_google_scholar, entry_scopus, entry_wos, entry_user, entry_pswd):
    entry_google_scholar.config(highlightthickness=0)
    entry_scopus.config(highlightthickness=0)
    entry_wos.config(highlightthickness=0)
    entry_user.config(highlightthickness=0)
    entry_pswd.config(highlightthickness=0)


def set_window(window, x, y):
    window.title('PCVN')
    window.geometry('750x750' + '+' + str(x) + '+' + str(y))
    window.iconbitmap('logo.ico')
    window.resizable(width=False, height=False)

    return window


def center_frame(window, frame):
    window.update()
    window_width = 750
    frame_width = frame.winfo_width()
    frame.place(x=(window_width - frame_width) / 2, y=50)
    return window, frame


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def get_window_pos(window):
    x = window.winfo_x()
    y = window.winfo_y()
    return x, y


class GuiMenu:
    def __init__(self, master):
        self.master = master
        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.submenu = Menu(self.menu)

        # ///////// Sub Menu Max Publications /////////#
        self.submenu_pub = Menu(self.submenu)
        # Options of submenu
        self.submenu_pub.add_command(label="10", command=self.set10)
        self.submenu_pub.add_command(label="20", command=self.set20)
        self.submenu_pub.add_command(label="50", command=self.set50)
        self.submenu_pub.add_command(label="Todas", command=self.set_all)
        self.submenu.add_cascade(label="Máx Publicaciones", menu=self.submenu_pub)

        # ///////// Sub Menu Steps to Execute /////////#
        self.submenu_steps = Menu(self.submenu)
        # Options of submenu
        self.submenu_steps.add_command(label="Extraer", command=self.extract)
        self.submenu_steps.add_command(label="Subir", command=self.log)
        self.submenu_steps.add_command(label="Extraer y subir", command=self.full_process)
        self.submenu.add_cascade(label="Pasos a Ejecutar", menu=self.submenu_steps)

        # ///////// Main Options Menu /////////#
        self.menu.add_cascade(label="Configuración", underline=0, menu=self.submenu)
        self.menu.add_command(label="Ayuda", command=self.open)

    def open(self):
        open_file('ayuda.pdf')

    def set10(self):
        global max_p
        max_p = 10

    def set20(self):
        global max_p
        max_p = 20

    def set50(self):
        global max_p
        max_p = 50

    def set_all(self):
        global max_p
        max_p = 10000

    def log(self):
        x, y = get_window_pos(self.master)
        self.master.destroy()
        global ext_flag, log_flag
        ext_flag = False
        log_flag = True
        aneca_login(x, y)

    def extract(self):
        x, y = get_window_pos(self.master)
        self.master.destroy()
        global ext_flag, log_flag
        ext_flag = True
        log_flag = False
        get_only_info_window(x, y)

    def full_process(self):
        x, y = get_window_pos(self.master)
        self.master.destroy()
        global ext_flag, log_flag
        ext_flag = True
        log_flag = True
        info_window(x, y)


class Background:
    def __init__(self, master, text, file):
        self.image = Image.open('./backgrounds/' + file)
        self.draw = ImageDraw.Draw(self.image)
        try:
            self.font = ImageFont.truetype("times.ttf", 22)
        except OSError:
            self.font = ImageFont.truetype("Times New Roman", 22)
        self.lines = textwrap.wrap(text, width=60)
        self.y = 470
        for line in self.lines:
            self.draw.text((140, self.y), line, fill="white", font=self.font)
            self.y += 25
        self.photoimage = ImageTk.PhotoImage(self.image)
        Label(master, image=self.photoimage).place(x=0, y=0)


if __name__ == '__main__':
    max_p = 10000
    log_flag = True
    ext_flag = True
    info_window(0, 0)
