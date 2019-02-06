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

from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ConnectionError
import textwrap
import tkinter.messagebox


def info_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    window.resizable(width=False, height=False)
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def return_au():
        global au_google, au_scopus, au_wos
        au_google = entry_google_scholar.get()
        au_scopus = entry_scopus.get()
        au_wos = entry_wos.get()
        window.destroy()
        google_search()

    txt = "Cuando se pulse el botón 'search' se procederá a la búsqueda de los datos referentes al autor introducidos durante el proceso ocurriera algún problema con los datos introducidos podrá introducirlos nuevamente"
    # Background
    bg = Background(window, txt)
    # Menu #
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()

    # ///////// Google Scholar Entry /////////#
    # Label
    label_google_scholar = Label(window, text="Google Scholar Author:")
    font = ('times', 15)
    label_google_scholar.config(font=font)
    label_google_scholar.place(x=150, y=70)
    # Entry
    entry_google_scholar = Entry(window, width=50)
    entry_google_scholar.place(x=350, y=75)

    # ///////// Scopus Entry /////////#
    # Label
    label_scopus = Label(window, text="Scopus Author ID:")
    label_scopus.config(font=font)
    label_scopus.place(x=190, y=170)
    # Entry
    entry_scopus = Entry(window, width=50)
    entry_scopus.place(x=350, y=175)

    # ///////// WOS Entry /////////#
    # Label
    label_wos = Label(window, text="WOS Author Name:")
    label_wos.config(font=font)
    label_wos.place(x=180, y=270)
    # Entry
    entry_wos = Entry(window, width=50)
    entry_wos.place(x=350, y=275)

    # Search Button
    bt_scopus = Button(window, text="Search",
                       command=return_au, height=1, width=30)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.place(x=200, y=370)
    """ 
    # Label information
    txt = "Cuando se pulse el botón 'search' se procederá a la búsqueda de los datos referentes al autor introducidos durante el proceso ocurriera algún problema con los datos introducidos podrá introducirlos nuevamente"
    label_info = Label(window, text=txt, width=48, height=8, wraplength=520, relief=RIDGE)
    label_info.config(font=font)
    label_info.place(x=130, y=470)
    """
    window.mainloop()


""" Fucntion that will show process of data scrapping in Google Scholar """


def google_search():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def re_start():
        window.destroy()
        google_window()

    def skip():
        window.destroy()

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
            answer = tkinter.messagebox.askyesno('Sin resultados', 'No se han encontrado resultados \n ¿Desea Volver a buscar?')
            if answer:
                window.destroy()
                google_window()
            else:
                window.destroy()
        except ConnectionError:
            pbar_google_scholar.stop()
            answer = tkinter.messagebox.askyesno('Error de Conexión', 'Ha ocurrido un error con la conexión \n ¿Desea Volver a intentarlo?')
            if answer:
                window.destroy()
                google_window()
            else:
                window.destroy()
        else:
            pbar_google_scholar.stop()
            # Destroy Window
            window.destroy()
            scopus_search()
    # Background
    txt = "Actualmente se está realizando la obtención de los datos desde GOOGLE SCHOLAR.\n Cuando se termine el proceso comenzará automáticamente la búsqueda en Scopus"
    bg = Background(window, txt)
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()
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


def google_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
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
        print(au_google)
        window.destroy()
        google_search()

    # backGround Image
    bg = Background(window, '')
    # Label
    label_google_scholar = Label(window, text="Google Scholar Author:")
    font = ('times', 15)
    label_google_scholar.config(font=font)
    label_google_scholar.place(x=130, y=320)
    # Entry
    entry_google_scholar = Entry(window, width=50)
    entry_google_scholar.place(x=350, y=325)
    # Search Button
    bt_google_scholar = Button(window, text="Search",
                               command=retry, height=1, width=30)
    bfont = ('times', 17)
    bt_google_scholar.config(font=bfont)
    bt_google_scholar.place(x=200, y=430)

    window.mainloop()


""" Fucntion that will show process of data scrapping in Scopus"""


def scopus_search():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def re_start():
        window.destroy()
        scopus_window()

    def skip():
        window.destroy()

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
                    window.destroy()
                    scopus_window()
                else:
                    window.destroy()
            else:
                window.destroy()
                wos_search()

        except (KeyError, NoSuchElementException, ConnectionError):
            pbar_scopus.stop()
            answer = tkinter.messagebox.askyesno('Error de Conexión', 'Ha ocurrido un error con la conexión \n ¿Desea Volver a intentarlo?')
            if answer:
                window.destroy()
                scopus_window()
            else:
                window.destroy()
    # Menu
    menu = GuiMenu(window)
    # backGround
    text = "Actualmente se está realizando la obtención de los datos desde SCOPUS.\n Cuando se termine el proceso comenzará automáticamente la búsqueda en Web of Science."
    bg = Background(window, text)
    # Estado
    estado = State(window)
    estado.actualiza()
    # Progress Bar
    pbar_scopus = ttk.Progressbar(window, mode='determinate', length=400)
    # Label information

    # get publications
    get_scopus_pub()
    window.mainloop()


""" Function tha will ask again for user input for Scopus author, if at first try it does not work"""


def scopus_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        retry()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def retry():
        # author name , will be used later
        au_scopus = entry_scopus.get()
        window.destroy()
        scopus_search()

    # backGround
    bg = Background(window, '')
    # Label
    label_scopus = Label(window, text="Scopus Author ID:")
    font = ('times', 15)
    label_scopus.config(font=font)
    label_scopus.place(x=185, y=320)
    # Entry
    entry_scopus = Entry(window, width=50)
    entry_scopus.place(x=350, y=325)
    # Search Button
    bt_scopus = Button(window, text="Search",
                       command=retry, height=1, width=30)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.place(x=200, y=430)

    window.mainloop()


""" Fucntion that will show process of data scrapping in WOS """


def wos_search():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def re_start():
        window.destroy()
        wos_window()

    def skip():
        window.destroy()

    def get_wos_pub():
        # Place progressbar in window
        pbar_wos.place(x=200, y=300)
        pbar_wos.update()
        pbar_wos['maximum'] = 100
        try:
            # Call function to retrieve publications
            if get_publications_wos(au_wos, pbar_wos):
                pbar_wos.stop()
                # remove all widgets on window
                widget_list = window.place_slaves()
                for l in widget_list:
                    l.destroy()
                window.update()
                time.sleep(1)
                # Label that indicates that there are No publications found
                label_no_pub = Label(window, text="There are no publications returned for this author",
                                     bg='red')
                font = ('times', 15)
                label_no_pub.config(font=font)
                label_no_pub.place(x=200, y=300)
                # Search Again Button
                bt_search_again = Button(window, text="Search again",
                                         command=re_start, height=1, width=30)
                b_font = ('times', 17)
                bt_search_again.config(font=b_font)
                bt_search_again.place(x=200, y=430)
                # Skip Button
                bt_search_again = Button(window, text="Skip",
                                         command=skip, height=1, width=30)
                bt_search_again.config(font=b_font)
                bt_search_again.place(x=200, y=480)

                window.update()
            else:
                pbar_wos.stop()
                # Destroy window
                window.destroy()
                group_window()
        except ConnectionError:

            # Label that indicates the failure of the function to connect with Scopus API
            label_fail = Label(window, text="Error en la conexion , compruebe si tiene acceso a internet",
                               bg='red')
            font = ('times', 15)
            label_fail.config(font=font)
            label_fail.place(x=150, y=200)
            window.update()

            time.sleep(2)

            # Search Again Button
            bt_search_again = Button(window, text="Search again",
                                     command=re_start, height=1, width=30)
            b_font = ('times', 17)
            bt_search_again.config(font=b_font)
            bt_search_again.place(x=200, y=430)
            # Skip Button
            bt_search_again = Button(window, text="Skip",
                                     command=skip, height=1, width=30)
            bt_search_again.config(font=b_font)
            bt_search_again.place(x=200, y=480)

    # Background
    text = "Actualmente se está realizando la obtención de los datos desde WEB OF SCIENCE.\n Cuando se termine el proceso comenzará automáticamente el tratamiento de datos."
    bg = Background(window, text)
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()
    # Progress Bar
    pbar_wos = ttk.Progressbar(window, mode='determinate', length=400)
    # Get Publicatiosn
    get_wos_pub()
    window.mainloop()


def wos_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        retry()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def retry():
        # author name , will be used later
        au_wos = entry_wos.get()
        window.destroy()
        wos_search()

    # backGround
    bg = Background(window, '')
    # Label
    label_wos = Label(window, text="WOS Author name:")
    font = ('times', 15)
    label_wos.config(font=font)
    label_wos.place(x=185, y=320)
    # Entry
    entry_wos = Entry(window, width=50)
    entry_wos.place(x=350, y=325)
    # Search Button
    bt_wos = Button(window, text="Search", command=retry, height=1, width=30)
    bfont = ('times', 17)
    bt_wos.config(font=bfont)
    bt_wos.place(x=200, y=430)

    window.mainloop()


""" Function that will show window indicating the user that 
the process of Grouping files and parsing is taking place """


def group_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that will place progress bar and start 
    groupfiles process"""

    def groupfiles():
        # Place progressbar in window
        pbar_g_files.place(x=200, y=250)
        pbar_g_files.update()
        pbar_g_files['maximum'] = 100
        # Call function that group & parse files
        group_files(pbar_g_files)
        pbar_g_files.stop()
        # Destroy window
        window.destroy()
        aneca_login()

    # backGround
    text = "Se esta procediendo al tratamiento de los datos, eliminación de elementos duplicados y agrupación en un solo fichero.\n Cuando se termine comenzará el proceso de subida a ACADEMIA"
    bg = Background(window, text)
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()
    # Progress Bar
    pbar_g_files = ttk.Progressbar(window, mode='determinate', length=400)

    groupfiles()

    window.mainloop()

    """ Function that will show the user a window to log in in Academia 
    these credential will be later use in Aneca() """


def aneca_login():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that get data from entries """

    def get_login():
        # needed global variables for use in other windows process
        global user
        global pswd
        user = entry_user.get()
        pswd = entry_pswd.get()
        # Destroy window
        window.destroy()
        aneca_window(au_google)

    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_login()

    window.bind('<Return>', func)
    # backGround
    bg = Background(window, '')
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()

    # Label User
    label_user = Label(window, text="Usuario")
    font = ('times', 20)
    label_user.config(font=font)
    label_user.place(x=220, y=320)
    # Entry User
    entry_user = Entry(window, width=40)
    entry_user.place(x=360, y=325)

    # Label Password
    label_pswd = Label(window, text="Contraseña")
    font = ('times', 20)
    label_pswd.config(font=font)
    label_pswd.place(x=220, y=370)
    # Entry Password
    entry_pswd = Entry(window, width=20)
    entry_pswd.place(x=360, y=385)
    entry_pswd.config(show="*")  # Make password invisible

    # Login Button
    bt_login = Button(window, text="Login", height=1,
                      width=10, command=get_login)
    bfont = ('times', 17)
    bt_login.config(font=bfont)
    bt_login.place(x=360, y=430)

    window.mainloop()


""" Function that will log the user in Academia and start process to 
upload all data stored previously to platform
will also show a window for login, and later will show a window
indicating the progress taken """


def aneca_window(author):
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
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
        total, failed = aneca(author, pbar_aneca, user, pswd, num_var, total, failed)
        if total is True:
            error = tkinter.messagebox.showerror("Usuario o Contraseña Incorrectos \n Por favor introduzca los datos de nuevos")
            window.destroy()
            aneca_login()

        pbar_aneca.stop()
        # Destroy Window
        window.destroy()
        completed_window()

    # backGround
    text = "Se está procediendo a la subida de los datos a ACADEMIA.\n Este es el último paso del proceso, cuando termine se mostrará cuantas publicaciones pudieron ser subidas y las que no, habrán sido guardadas en un fichero para su corrección manual."
    bg = Background(window, text)
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    estado.actualiza()

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


def completed_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')

    def end_gui():
        # Destroy Window
        window.destroy()

    # backGround
    text = 'Número de publicaciones que no pudieron ser subidas:\n' + str(failed) + '/' + str(total)
    bg = Background(window, text)
    # Menu
    menu = GuiMenu(window)
    # Estado
    estado = State(window)
    # Label
    label_completed = Label(window, text="Proceso finalizado")
    font = ('times', 25)
    label_completed.config(font=font)
    label_completed.place(x=300, y=300)

    # Close Button
    bt_close = Button(window, text="Close", height=1,
                      width=10, command=end_gui)
    bfont = ('times', 17)
    bt_close.config(font=bfont)
    bt_close.place(x=350, y=410)

    window.mainloop()


def fail_login():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')

    def end_gui():
        # Destroy Window
        window.destroy()

    # backGround
    bg = Background(window, '')
    # Menu
    menu = GuiMenu(window)
    # Label
    label_completed = Label(window, text="Login fallído", bg='red')
    font = ('times', 25)
    label_completed.config(font=font)
    label_completed.place(x=300, y=320)

    # Close Button
    bt_login = Button(window, text="Intentar otra vez", height=1,
                      width=15, command=end_gui)
    bfont = ('times', 17)
    bt_login.config(font=bfont)
    bt_login.place(x=295, y=430)

    window.mainloop()


class GuiMenu:
    def __init__(self, master):
        self.menu = Menu(master)
        master.config(menu=self.menu)

        self.submenu_pub = Menu(self.menu)

        self.submenu_pub.add_command(label="10", command=self.set10)
        self.submenu_pub.add_command(label="20", command=self.set20)
        self.submenu_pub.add_command(label="50", command=self.set50)
        self.submenu_pub.add_command(label="Todas", command=self.set_all)
        self.menu.add_cascade(label="Máx Publicaciones", menu=self.submenu_pub)

        self.menu.add_command(label="Ayuda",command=self.test)

    def test(self):
        print('testing')

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


class Background:
    def __init__(self, master, text):
        self.image = Image.open("background.png")
        self.draw = ImageDraw.Draw(self.image)
        try:
            self.font = ImageFont.truetype("times.ttf", 22)
        except OSError:
            self.font = ImageFont.truetype("arial.ttf", 22)
        self.lines = textwrap.wrap(text, width=60)
        self.y = 470
        for line in self.lines:
            self.draw.text((140, self.y), line, fill="white", font=self.font)
            self.y += 25
        self.photoimage = ImageTk.PhotoImage(self.image)
        Label(master, image=self.photoimage).place(x=0, y=0)


class State:
    def __init__(self, master):
        self.list_label = list()

        self.frame = Frame(master)
        self.frame.place(x=145, y=0)

        self.label_inicio = Label(self.frame, text='Inicio', bg='red', relief="groove")
        self.label_inicio.pack(side=LEFT)
        self.list_label.append(self.label_inicio)

        self.label_scholar = Label(self.frame, text='Google Scholar', bg='red', relief="groove")
        self.label_scholar.pack(side=LEFT)
        self.list_label.append(self.label_scholar)

        self.label_scopus = Label(self.frame, text='Scopus', bg='red', relief="groove")
        self.label_scopus.pack(side=LEFT)
        self.list_label.append(self.label_scopus)

        self.label_wos = Label(self.frame, text='Web of Science', bg='red', relief="groove")
        self.label_wos.pack(side=LEFT)
        self.list_label.append(self.label_wos)

        self.label_data = Label(self.frame, text='Tratando Datos', bg='red', relief="groove")
        self.label_data.pack(side=LEFT)
        self.list_label.append(self.label_data)

        self.label_aneca = Label(self.frame, text='Aneca Login', bg='red', relief="groove")
        self.label_aneca.pack(side=LEFT)
        self.list_label.append(self.label_aneca)

        self.label_academia = Label(self.frame, text='Academia', bg='red', relief="groove")
        self.label_academia.pack(side=LEFT)
        self.list_label.append(self.label_academia)

        self.label_completado = Label(self.frame, text='Completado', bg='red', relief="groove")
        self.label_completado.pack(side=LEFT)
        self.list_label.append(self.label_completado)

    def actualiza(self):
        global cont
        if cont < 0:
            cont += 1
            self.list_label[cont].config(bg='green', relief="sunken")

        else:
            self.list_label[cont].config(bg='red', relief="groove")
            cont += 1
            self.list_label[cont].config(bg='green', relief="sunken")


if __name__ == '__main__':
    max_p = 10000
    cont = -1
    info_window()
