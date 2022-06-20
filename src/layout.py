from msilib.schema import ComboBox
from tkinter.ttk import Combobox
import easygui
import matplotlib
import os
from PIL import ImageTk,Image
from tkinter import *

class appMenu():
    def __init__(self,root,geometry,title):
        #=========Loading of placeholder image
        baseDir = os.path.dirname(__file__)
        filePath = os.path.join(baseDir,'..','static','Figure_1.png')
        self.image = PhotoImage(file=filePath)

        self.root = root
        self.root.geometry(geometry)
        self.root.title(title)

        #=========Upper menus
        self.fileMenu = Menu(self.root)
        self.menuItems = Menu(self.fileMenu)
        self.menuItems.add_command(label='Load data')
        self.menuItems.add_command(label='Load image',command=self.LoadImage)
        self.fileMenu.add_cascade(label='File',menu=self.menuItems)
        self.root.config(menu=self.fileMenu)

        #=========Plot frame
        self.imageFrame = Frame(self.root)
        self.plotCanvas = Canvas(self.imageFrame,width=640,height=480)
        self.plotCanvas.create_image(10,10,anchor=NW,image=self.image)
        self.plotCanvas.pack()
        self.imageFrame.grid(column=0,row=0)

        #=========Optons frame
        self.buttonFrame = Frame(self.root)

        self.countryLabel = Label(self.buttonFrame,text='Country:')
        self.countryLabel.pack()
        self.countryComboBox = Combobox(self.buttonFrame)
        self.countryComboBox['values'] = (1,2,3,4)
        self.countryComboBox.pack(padx=10,pady=10)

        self.categoryLabel = Label(self.buttonFrame,text='Category:')
        self.categoryLabel.pack()
        self.categoryComboBox = Combobox(self.buttonFrame)
        self.categoryComboBox['values'] = (5,6,7,8)
        self.categoryComboBox.pack(padx=10,pady=10)
        self.buttonFrame.grid(column=1,row=0,sticky=N)
    
    def LoadImage(self):
        filepath = easygui.fileopenbox()
        tempImage = PhotoImage(file=filepath)
        self.image = tempImage

        self.plotCanvas.create_image(10,10,anchor=NW,image=self.image)
        
