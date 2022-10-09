from tkinter.ttk import Combobox
import easygui
import matplotlib
import os
import PIL.Image, PIL.ImageTk
from tkinter import *

class appMenu():
    def __init__(self,root,geometry,title):
        #=========Loading of plot placeholder image
        self.BASE_DIR = os.path.dirname(__file__)
        filePath = os.path.join(self.BASE_DIR,'..','static','Figure_1.png')
        self.img = PIL.Image.open(filePath)
        self.img = PIL.ImageTk.PhotoImage(self.img)

        #=========Title and geometry setup
        self.root = root
        self.root.geometry(geometry)
        self.root.title(title)

        #=========Window icon setup
        iconPath = os.path.join(self.BASE_DIR,'..','static','chart.ico')
        self.root.iconbitmap(iconPath)

        #=========Upper menus
        self.fileMenu = Menu(self.root)
        self.menuItems = Menu(self.fileMenu)
        self.menuItems.add_command(label='Load data',command=self.LoadData)
        self.menuItems.add_command(label='Load image',command=self.LoadImage)
        self.fileMenu.add_cascade(label='File',menu=self.menuItems)
        self.root.config(menu=self.fileMenu)

        #=========Plot frame
        self.imageFrame = Frame(self.root)
        self.plotCanvas = Canvas(self.imageFrame,width=640,height=480)
        self.plotCanvas.create_image(10,10,anchor=NW,image=self.img)
        self.plotCanvas.pack()
        self.imageFrame.grid(column=0,row=0)

        #=========Optons frame
        self.buttonFrame = Frame(self.root)

        self.countryLabel = Label(self.buttonFrame,text='Country:')
        self.countryLabel.pack()
        self.countryComboBox = Combobox(self.buttonFrame)
        self.countryComboBox['values'] = ('Nodata')
        self.countryComboBox.pack(padx=10,pady=10)

        self.categoryLabel = Label(self.buttonFrame,text='Category:')
        self.categoryLabel.pack()
        self.categoryComboBox = Combobox(self.buttonFrame)
        self.categoryComboBox['values'] = ('Nodata')
        self.categoryComboBox.pack(padx=10,pady=10)
        self.buttonFrame.grid(column=1,row=0,sticky=N)
    
    def LoadImage(self):
        #====Opening file and saviing it as photoimage type
        filepath = easygui.fileopenbox()
        tempImage = PIL.Image.open(filepath)
        self.img = PIL.ImageTk.PhotoImage(tempImage)

        #====Resizing canvas for image size
        self.plotCanvas.config(width=tempImage.width,height=tempImage.height)
        self.plotCanvas.create_image(10,10,anchor=NW,image=self.img)

    
    def LoadData(self):
        filepath = easygui.fileopenbox()

        if filepath.endswith('.json'):
            print('its json')
        elif filepath.endswith('.csv'):
            print('its csv')
        elif filepath.endswith('.xlsx'):
            print('its xlsx')

