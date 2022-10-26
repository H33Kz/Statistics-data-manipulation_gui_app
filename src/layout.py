from tkinter.ttk import Combobox
from tkinter import *
from dateutil import parser
import easygui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import os
import PIL.Image, PIL.ImageTk
import csv
import numpy as np



class appMenu():
    def __init__(self,root,geometry,title):
        #=========Initiating empty variables for plot data
        self.uniqueCountries = ['No data']
        self.uniqueUnit = ['No data']

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
        self.fileMenu.add_cascade(label='File',menu=self.menuItems)
        self.root.config(menu=self.fileMenu)

        #=========Plot frame
        self.imageFrame = Frame(self.root)

        self.figure = plt.figure(figsize=(8,6),dpi=100)
        self.graph = self.figure.add_subplot(111)
        self.plotCanvas = FigureCanvasTkAgg(self.figure,self.imageFrame)
        self.plotCanvas.get_tk_widget().pack()
        self.plotCanvas.draw()
        

        self.imageFrame.grid(column=0,row=0)

        #=========Toolbar frame
        self.toolbarFrame = Frame(self.root)
        self.toolbarFrame.grid(column=0,row=1)
        self.toolbar=NavigationToolbar2Tk(self.plotCanvas,self.toolbarFrame)

        #=========Categories frame
        self.buttonFrame = Frame(self.root)
        #===Country selection
        self.countryLabel = Label(self.buttonFrame,text='Country:')
        self.countryLabel.pack()
        self.countryComboBox = Combobox(self.buttonFrame)
        self.countryComboBox['values'] = (self.uniqueCountries)
        self.countryComboBox['state'] = 'readonly'
        self.countryComboBox.pack(padx=10,pady=10)
        #===Unit selection
        self.unitLabel = Label(self.buttonFrame,text='Unit:')
        self.unitLabel.pack()
        self.unitComboBox = Combobox(self.buttonFrame)
        self.unitComboBox['values'] = (self.uniqueUnit)
        self.unitComboBox['state'] = 'readonly'
        self.unitComboBox.pack(padx=10,pady=10)        
        #===Graph drawing button
        self.graphButton = Button(self.buttonFrame, text='Create graph',command=self.CreateGraph)
        self.graphButton.pack()

        self.buttonFrame.grid(column=1,row=0,sticky=N)

    
    def LoadData(self):
        filepath = easygui.fileopenbox()

        if filepath.endswith('.csv'):
            #====Opening csv file and saving its data to a list of lists
            rows = []
            with open(filepath, 'r', encoding='utf-8') as file:
                csvreader = csv.reader(file)
                self.header = next(csvreader)
                for row in csvreader:
                    rows.append(row)
            self.records = rows
            #====Parsing unique country names to a list
            self.uniqueCountries = []
            for row in self.records:
                self.uniqueCountries.append(row[-1])
            self.uniqueCountries = np.ndarray.tolist(np.unique(np.array(self.uniqueCountries)))
            self.countryComboBox['values'] = (self.uniqueCountries)
            #====Parsing unique units to a list
            self.uniqueUnit = []
            for row in self.records:
                self.uniqueUnit.append(row[-6])
            self.uniqueUnit = np.ndarray.tolist(np.unique(np.array(self.uniqueUnit)))
            self.unitComboBox['values'] = (self.uniqueUnit)

        else:
            print('Datatype not supported')

    def CreateGraph(self):
        #====Getting chosen options
        selectedCountry = self.countryComboBox.get()
        selectedUnit = self.unitComboBox.get()
        #====Parsing readings that fit chosen category
        selectedData = []
        for row in self.records:
            if row[-1] == selectedCountry and row[-6] == selectedUnit:
                selectedData.append(row)
        #====Transforming date record to be only month
        for row in selectedData:
            row[-2] = str(parser.parse(row[-2]).month)
        #====Transforming data for graph drawing
        plotData = [[] for i in range(12)]
        for row in selectedData:
            for idx,dataRow in enumerate(plotData):
                if idx == int(row[-2])-1:
                    dataRow.append(float(row[-3]))

        #====Clearing graph
        self.figure.clear()
        self.graph.clear()
        self.graph = self.figure.add_subplot(111)
        #====Ploting with a new data
        self.graph.boxplot(plotData)
        self.plotCanvas.draw()


