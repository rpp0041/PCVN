from tkinter import *
from tkinter import ttk
from PIL import Image
from GetPublicationsScholar import *
from GetPublicationsScopus import *
from GetPublicationsWOS import *
from GroupFiles import *
from ANECA import *
import time

def Google():
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def func(event):
        get_scholar_pub()
    window.bind('<Return>', func)
    
    def get_scholar_pub():
        author=entryGoogleScholar.get()
        global authorGoogle
        authorGoogle=author 
        
        pbarGoogleScholar.place(x=200,y=550)
        pbarGoogleScholar.update()
        pbarGoogleScholar['maximum']=100
    
        GetPublicationsScholar(author,pbarGoogleScholar)
        pbarGoogleScholar.stop()
        window.destroy()

    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    # Label 
    labelGoogleScholar = Label(window, text="Google Scholar Author:")
    font=('times', 15)
    labelGoogleScholar.config(font=font)
    labelGoogleScholar.place(x=130,y=320)
    # Entry
    entryGoogleScholar = Entry(window,width=50)
    entryGoogleScholar.place(x=350,y=325)
    # Button
    BTGoogleScholar=Button(window, text="Search", command=get_scholar_pub , height=1,width=30)
    bfont=('times', 17)
    BTGoogleScholar.config(font=bfont)
    BTGoogleScholar.place(x=200,y=430)
    # Progress Bar
    pbarGoogleScholar=ttk.Progressbar(window,mode='determinate',length=400)

    window.mainloop()

""" """
def Scopus():
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def func(event):
        get_scopus_pub()
    window.bind('<Return>', func)
    
    def get_scopus_pub():
        author=entryScopus.get()

        pbarScopus.place(x=200,y=550)
        pbarScopus.update()
        pbarScopus['maximum']=100
        GetPublicationsScopus(author,pbarScopus)
        pbarScopus.stop()
        print('DONE')
        window.destroy()

    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    # Label 
    labelScopus = Label(window, text="Scopus Author ID:")
    font=('times', 15)
    labelScopus.config(font=font)
    labelScopus.place(x=185,y=320)
    # Entry
    entryScopus = Entry(window,width=50)
    entryScopus.place(x=350,y=325)
    # Button
    BTScopus=Button(window, text="Search", command=get_scopus_pub , height=1,width=30)
    bfont=('times', 17)
    BTScopus.config(font=bfont)
    BTScopus.place(x=200,y=430)
    # Progress Bar
    pbarScopus=ttk.Progressbar(window,mode='determinate',length=400)

    window.mainloop()

""" """ 

def wos():
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def func(event):
        get_wos_pub()
    window.bind('<Return>', func)
    
    def get_wos_pub():
        author=entry_wos.get()

        pbar_wos.place(x=200,y=550)
        pbar_wos.update()
        pbar_wos['maximum']=100
        get_publications_wos(author,pbar_wos)
        pbar_wos.stop()
        print('DONE')
        window.destroy()

    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    # Label 
    label_wos = Label(window, text="WOS Author Name:")
    font=('times', 15)
    label_wos.config(font=font)
    label_wos.place(x=140,y=320)
    # Entry
    entry_wos = Entry(window,width=50)
    entry_wos.place(x=350,y=325)
    # Button
    BT_wos=Button(window, text="Search", command=get_wos_pub , height=1,width=30)
    bfont=('times', 17)
    BT_wos.config(font=bfont)
    BT_wos.place(x=200,y=430)
    # Progress Bar
    pbar_wos=ttk.Progressbar(window,mode='determinate',length=400)

    window.mainloop()

""" """ 
def Groupfiles():
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def groupfiles():
        pbar_g_files.place(x=200,y=550)
        pbar_g_files.update()
        pbar_g_files['maximum']=100
        group_files(pbar_g_files)
        pbar_g_files.stop()
        print('DONE')
        window.destroy()

    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    # Label 
    label_g_files = Label(window, text="Grouping files & Removing duplicates")
    font=('times', 25)
    label_g_files.config(font=font)
    label_g_files.place(x=125,y=320)
    
    # Label_2
    label_g_files_2 = Label(window, text="(Please Wait)")
    font=('times', 15)
    label_g_files_2.config(font=font)
    label_g_files_2.place(x=300,y=400)
    
    
    # Progress Bar
    pbar_g_files=ttk.Progressbar(window,mode='determinate',length=400)
    
    groupfiles()

    window.mainloop()

""" """ 
def aneca_login():
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def get_login():
        global user
        global pswd
        user=entry_user.get()
        pswd=entry_pswd.get()
        window.destroy()
    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    
    # Label User
    label_user = Label(window, text="Usuario")
    font=('times', 20)
    label_user.config(font=font)
    label_user.place(x=220,y=320)
    # Entry User
    entry_user = Entry(window,width=40)
    entry_user.place(x=360,y=325)
    
    # Label Password
    label_pswd = Label(window, text="Contraseña")
    font=('times', 20)
    label_pswd.config(font=font)
    label_pswd.place(x=220,y=370)
    # Entry Password
    entry_pswd = Entry(window,width=20)
    entry_pswd.place(x=360,y=385)
    entry_pswd.config(show="*");
    
    
    # Button
    bt_login=Button(window, text="Login", height=1,width=10,command=get_login)
    bfont=('times', 17)
    bt_login.config(font=bfont)
    bt_login.place(x=360,y=430)
    
    window.mainloop()
""" """
def Aneca(author):
    aneca_login()
    window=Tk()
    window.title('PCVN')
    window.geometry('800x800')
    
    def start_aneca():
        pbar_aneca.place(x=220,y=420)
        pbar_aneca.update()
        pbar_aneca['maximum']=100
        aneca(author,pbar_aneca,user,pswd)
        pbar_aneca.stop()
        print('DONE')
        window.destroy()

    # backGround
    photo = PhotoImage(file="test.png")
    labelbg=Label(window,image=photo)
    labelbg.pack()
    # Label 
    label_aneca = Label(window, text="Uploading Files to Academia")
    font=('times', 25)
    label_aneca.config(font=font)
    label_aneca.place(x=220,y=320)
    
    
    # Progress Bar
    pbar_aneca=ttk.Progressbar(window,mode='determinate',length=400)
    
    #Start Aneca
    start_aneca()

    window.mainloop()

if __name__ == '__main__':
	Google() 
	Scopus()
	wos()
	Groupfiles()
	Aneca(authorGoogle)