#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from PIL import Image
from GetPublicationsScholar import *
from GetPublicationsScopus import *
from GetPublicationsWOS import *
from GroupFiles import *
from ANECA import *

""" Fucntion that will show window to entry author name to be searched
in Google Scholar """


def google_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_scholar_pub()

    window.bind('<Return>', func)
    """ Function to be executed when click search button"""
    def re_start():
        window.destroy()
        google_window()

    def skip():
        window.destroy()

    def get_scholar_pub():
        # author name , will be used later
        author = entry_google_scholar.get()
        global author_google
        author_google = author
        # place progressbar in window
        pbar_google_scholar.place(x=200, y=550)
        pbar_google_scholar.update()
        pbar_google_scholar['maximum'] = 100
        # Call function to retrieve publications
        try:
            get_publications_scholar(author, pbar_google_scholar)
        except StopIteration:
            pbar_google_scholar.stop()
            # remove all widgets on window
            widget_list = window.place_slaves()
            for l in widget_list:
                l.destroy()
            window.update()
            time.sleep(1)
            # Label that indicates that there are No publications found
            label_no_pub = Label(window, text="There are no publications returned for this author",
                                 bg='red')
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
            b_font = ('times', 17)
            bt_search_again.config(font=b_font)
            bt_search_again.place(x=200, y=480)

            window.update()
        else:
            pbar_google_scholar.stop()
            # Destroy Window
            window.destroy()

    # backGround Image
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
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
                               command=get_scholar_pub, height=1, width=30)
    bfont = ('times', 17)
    bt_google_scholar.config(font=bfont)
    bt_google_scholar.place(x=200, y=430)
    # Progress Bar
    pbar_google_scholar = ttk.Progressbar(window, mode='determinate', length=400)

    window.mainloop()


""" Fucntion that will show window to entry author name to be searched
in Scopus """


def scopus_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_scopus_pub()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def re_start():
        window.destroy()
        scopus_window()

    def skip():
        window.destroy()

    def get_scopus_pub():
        # Get ID from entry
        author = entry_scopus.get()
        # Place progress bar in window
        pbar_scopus.place(x=200, y=550)
        pbar_scopus.update()
        pbar_scopus['maximum'] = 100
        # Call function to retrieve publications
        try:
            if get_publications_scopus(author, pbar_scopus):
                pbar_scopus.stop()
                # remove all widgets on window
                widget_list = window.place_slaves()
                for l in widget_list:
                    l.destroy()
                window.update()
                time.sleep(1)
                # Label that indicates that there are No publications found
                label_no_pub = Label(window, text="There are no publications returned for this author",
                                     bg='red')
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
                b_font = ('times', 17)
                bt_search_again.config(font=b_font)
                bt_search_again.place(x=200, y=480)

                window.update()
            else:
                pbar_scopus.stop()
                window.destroy()

        except KeyError:

            # Label that indicates the failure of the function to connect with Scopus API
            label_fail = Label(window, text="Error en la conexion , compruebe si su conexion tiene acceso a Scopus",
                               bg='red')
            label_fail.config(font=font)
            label_fail.place(x=150, y=500)
            window.update()

            time.sleep(2)

            window.destroy()
            scopus_window()

    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
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
                       command=get_scopus_pub, height=1, width=30)
    bfont = ('times', 17)
    bt_scopus.config(font=bfont)
    bt_scopus.place(x=200, y=430)
    # Progress Bar
    pbar_scopus = ttk.Progressbar(window, mode='determinate', length=400)

    window.mainloop()


""" Fucntion that will show window to entry author name to be searched
in Web Of Science """


def wos_window():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_wos_pub()

    window.bind('<Return>', func)
    """ Function to be executed when click on search button"""

    def get_wos_pub():
        # Get name from entry
        author = entry_wos.get()
        # Place progressbar in window
        pbar_wos.place(x=200, y=550)
        pbar_wos.update()
        pbar_wos['maximum'] = 100
        # Call function to retrieve publications
        get_publications_wos(author, pbar_wos)
        pbar_wos.stop()
        # Destroy window
        window.destroy()

    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
    # Label
    label_wos = Label(window, text="WOS Author Name:")
    font = ('times', 15)
    label_wos.config(font=font)
    label_wos.place(x=140, y=320)
    # Entry
    entry_wos = Entry(window, width=50)
    entry_wos.place(x=350, y=325)
    # Search Button
    bt_wos = Button(window, text="Search",
                    command=get_wos_pub, height=1, width=30)
    bfont = ('times', 17)
    bt_wos.config(font=bfont)
    bt_wos.place(x=200, y=430)
    # Progress Bar
    pbar_wos = ttk.Progressbar(window, mode='determinate', length=400)

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
        pbar_g_files.place(x=200, y=550)
        pbar_g_files.update()
        pbar_g_files['maximum'] = 100
        # Call function that group & parse files
        group_files(pbar_g_files)
        pbar_g_files.stop()
        # Destroy window
        window.destroy()

    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
    # Label
    label_g_files = Label(window, text="Grouping files & Removing duplicates")
    font = ('times', 25)
    label_g_files.config(font=font)
    label_g_files.place(x=125, y=320)

    # Label_2
    label_g_files_2 = Label(window, text="(Please Wait)")
    font = ('times', 15)
    label_g_files_2.config(font=font)
    label_g_files_2.place(x=300, y=400)

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

    """ Function that make possible push enter keyboard button 
    and it will work as search button"""

    def func(event):
        get_login()

    window.bind('<Return>', func)
    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()

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
    # Call login function
    aneca_login()
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')
    """ Function that will place progress bar and start 
    upload process"""

    def start_aneca():
        # Place progressbar in window
        pbar_aneca.place(x=220, y=420)
        pbar_aneca.update()
        pbar_aneca['maximum'] = 100
        # Call Aneca function to start upload process
        if aneca(author, pbar_aneca, user, pswd):
            window.destroy()
            fail_login()
            aneca_window(author)

        pbar_aneca.stop()
        # Destroy Window
        window.destroy()

    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
    # Label
    label_aneca = Label(window, text="Uploading Files to Academia")
    font = ('times', 25)
    label_aneca.config(font=font)
    label_aneca.place(x=220, y=320)

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
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
    # Label
    label_completed = Label(window, text="Proceso finalizado")
    font = ('times', 25)
    label_completed.config(font=font)
    label_completed.place(x=300, y=320)

    # Close Button
    bt_close = Button(window, text="Close", height=1,
                      width=10, command=end_gui)
    bfont = ('times', 17)
    bt_close.config(font=bfont)
    bt_close.place(x=350, y=430)

    window.mainloop()


def fail_login():
    window = Tk()
    window.title('PCVN')
    window.geometry('800x800')

    def end_gui():
        # Destroy Window
        window.destroy()

    # backGround
    photo = PhotoImage(file="background.png")
    labelbg = Label(window, image=photo)
    labelbg.pack()
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


if __name__ == '__main__':
    google_window()
    scopus_window()
    wos_window()
    group_window()
    aneca_window(author_google)
    completed_window()
