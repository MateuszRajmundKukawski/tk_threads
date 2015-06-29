# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
import threading

from gistools import GisTools
import os

class MyApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.userUI()
        self.pack()

    def initUI(self):
        self.parent.geometry("360x100")
        self.parent.title("Example app")

    def userUI(self):
        self.pad_x = 10
        self.pad_y = 5
        self.buttonWidth = 12
        self.file_name = StringVar()
        self.runApp_text = StringVar()
        self.runApp_text.set('?')
        self.workdir_fullpath = None
        self.path_file = 'app.data'

        self.initMenu()

        self.get_file_Button = Button(self, text="File", command=self.get_file, width=self.buttonWidth)
        self.get_file_Button.grid(row=0, column=0, sticky=W, padx=self.pad_x,pady = self.pad_y)

        self.file_name_Label = Label(self, textvariable=self.file_name)
        self.file_name_Label.grid(row=0, column=1)

        self.runApp_Button = Button(self, text="runAPP", command=self.runApp, width=self.buttonWidth)
        self.runApp_Button.grid(row=1, column=0, sticky=W, padx=self.pad_x,pady = self.pad_y)

        self.runApp_Label = Label(self, textvariable=self.runApp_text)
        self.runApp_Label.grid(row=1, column=1, sticky=W, padx=self.pad_x,pady = self.pad_y)


    def initMenu(self):
        menubar = Menu(self)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Info", command=self.app_info)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

    def onExit(self):

        self.quit()

    def get_file(self):

        self.get_lastdir()
        self.file_fullpath = askopenfilename(
            initialdir=self.workdir_fullpath,
            filetypes=[("Text files", "*.txt")], )
        if os.path.isfile(self.file_fullpath):
            self.set_lastdir(os.path.dirname(self.file_fullpath))
            self.file_name.set(os.path.basename(self.file_fullpath))

    def get_lastdir(self):

        if os.path.isfile(self.path_file):
            with open(self.path_file) as f:
                tmp = f.read()
                if os.path.isdir(tmp):
                    self.workdir_fullpath = tmp
                else:
                    self.workdir_fullpath = "c:/"
        else:
                    self.workdir_fullpath = "c:/"

    def set_lastdir(self, dirpath):

        with open(self.path_file, 'w') as f:
            f.write(dirpath)

    def app_info(self):

        msgText = 'This is my app'
        tkMessageBox.showinfo("Info", msgText)

    def runApp(self):
        """
        dlaczego gdy uzyje przyciusku, w trakcie trwania analizy
        przycisk pozostaje wciśniety (samo wcisniecie wiem, ze moge zmienic),
        ale tekst etykiety się nie zmienia
        dopiero po zakończniu nalizy tekst sie zmienia
        """

        self.runApp_text.set('...')
        GisThread(self.file_fullpath).start()




class GisThread(threading.Thread):
    def __init__(self, file_path):
        threading.Thread.__init__(self)
        self.file_path = file_path
	self.daemon = True 
    def run(self):
        file2qgis = GisTools()
        file2qgis.export2qgis(self.file_path)





app_window = Tk()
app = MyApp(parent=app_window)
app.mainloop()
