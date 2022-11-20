from statistics import median
from tkinter.ttk import Combobox, Notebook, Treeview
from tkinter import *
from turtle import width
from dateutil import parser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import math
import os
import csv
import copy
import easygui
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats


class appMenu():
    def __init__(self, root, geometry, title):
        # =========Initiating empty variables for plot data
        self.uniqueCountries = ['No data']
        self.uniqueUnit = ['No data']
        self.monthHeaders = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                             'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # =========Title and geometry setup
        self.root = root
        self.root.geometry(geometry)
        self.root.title(title)

        # =========Window icon setup
        self.BASE_DIR = os.path.dirname(__file__)
        iconPath = os.path.join(self.BASE_DIR, '..', 'static', 'chart.ico')
        self.root.iconbitmap(iconPath)

        # =========Upper menus
        self.fileMenu = Menu(self.root)
        self.menuItems = Menu(self.fileMenu)
        self.menuItems.add_command(label='Load data', command=self.LoadData)
        self.menuItems.add_command(label='Exit app', command=self.root.quit)
        self.fileMenu.add_cascade(label='File', menu=self.menuItems)
        self.root.config(menu=self.fileMenu)

        # =========Tab control(Moving between app functionality) and frames for different tabs
        self.tabControl = Notebook(
            self.root, style='Custom.TNotebook', width=1200, height=900)
        self.boxPlotTab = Frame(self.root)
        self.generalStatsTab = Frame(self.root)
        self.correlationTab = Frame(self.root)

        self.tabControl.add(self.boxPlotTab, text='boxplot')
        self.tabControl.add(self.generalStatsTab, text='general')
        self.tabControl.add(self.correlationTab, text='correlation')
        self.tabControl.pack()

        # ==============================================BOXPLOT TAB====================================
        # =========Plot frame
        self.boxPlotFrame = Frame(self.boxPlotTab)
        self.boxPlotFigure = plt.figure(figsize=(10, 6), dpi=100)
        self.boxPlotGraph = self.boxPlotFigure.add_subplot(111)
        self.boxPlotCanvas = FigureCanvasTkAgg(
            self.boxPlotFigure, self.boxPlotFrame)
        self.boxPlotCanvas.get_tk_widget().pack()
        self.boxPlotCanvas.draw()
        self.boxPlotFrame.grid(column=0, row=0)
        # =========Toolbar frame
        self.boxPlotToolbarFrame = Frame(self.boxPlotTab)
        self.boxPlotToolbarFrame.grid(column=0, row=1)
        self.toolbar = NavigationToolbar2Tk(
            self.boxPlotCanvas, self.boxPlotToolbarFrame)
        # =========Selection frame
        self.boxPlotSelectionFrame = Frame(self.boxPlotTab)
        self.boxPlotSelectionFrame.grid(column=1, row=0, sticky=N)
        # ===Country selection
        self.countryLabel = Label(self.boxPlotSelectionFrame, text='Country:')
        self.countryLabel.pack()
        self.countryComboBox = Combobox(self.boxPlotSelectionFrame)
        self.countryComboBox['values'] = (self.uniqueCountries)
        self.countryComboBox['state'] = 'readonly'
        self.countryComboBox.pack(padx=10, pady=10)
        # ===Unit selection
        self.unitLabel = Label(self.boxPlotSelectionFrame, text='Unit:')
        self.unitLabel.pack()
        self.unitComboBox = Combobox(self.boxPlotSelectionFrame)
        self.unitComboBox['values'] = (self.uniqueUnit)
        self.unitComboBox['state'] = 'readonly'
        self.unitComboBox.pack(padx=10, pady=10)
        # ===Graph drawing button
        self.graphButton = Button(
            self.boxPlotSelectionFrame, text='Analyze data', command=self.AnalyzeData)
        self.graphButton.pack(padx=10, pady=10)
        # ===Exit button
        self.exitButton1 = Button(
            self.boxPlotSelectionFrame, text='Exit app', command=self.root.quit)
        self.exitButton1.pack(padx=10, pady=10)

        # ==============================================GENERAL STATS TAB=================================
        # =========Plot frame
        self.barGraphFrame = Frame(self.generalStatsTab)
        self.barGraphFigure = plt.figure(figsize=(10, 6), dpi=100)
        self.barGraph = self.barGraphFigure.add_subplot(111)
        self.barGraphCanvas = FigureCanvasTkAgg(
            self.barGraphFigure, self.barGraphFrame)
        self.barGraphCanvas.get_tk_widget().pack()
        self.barGraphCanvas.draw()
        self.barGraphFrame.grid(column=0, row=0)
        # =========Toolbar frame
        self.barGraphToolbarFrame = Frame(self.generalStatsTab)
        self.barGraphToolbarFrame.grid(column=0, row=1)
        self.toolbar = NavigationToolbar2Tk(
            self.barGraphCanvas, self.barGraphToolbarFrame)
        # =========Selection frame
        self.barGraphSelectionFrame = Frame(self.generalStatsTab)
        self.barGraphSelectionFrame.grid(column=1, row=0, sticky=N)
        # ==Exit Button
        self.exitButton2 = Button(
            self.barGraphSelectionFrame, text='Exit app', command=self.root.quit)
        self.exitButton2.pack(padx=10, pady=10)
        # ==========Treeview frame
        self.treeviewFrame = Frame(self.generalStatsTab)
        self.treeviewFrame.grid(column=0, row=2, sticky=NSEW)
        # ======Treeview(Table for general information)
        self.generalStatsTreeview = Treeview(self.treeviewFrame, show='headings', columns=(
            'month', 'min', 'max', 'median', 'mean', 'std', 'iqr'))
        # ====Setting up coulmns
        self.generalStatsTreeview.column('month', anchor=W, width=60)
        self.generalStatsTreeview.column('min', anchor=W, width=60)
        self.generalStatsTreeview.column('max', anchor=W, width=60)
        self.generalStatsTreeview.column('median', anchor=W, width=60)
        self.generalStatsTreeview.column('mean', anchor=W, width=60)
        self.generalStatsTreeview.column('std', anchor=W, width=60)
        self.generalStatsTreeview.column('iqr', anchor=W, width=60)
        # ====Setting up names for columns
        self.generalStatsTreeview.heading('month', anchor=CENTER, text='mth')
        self.generalStatsTreeview.heading('min', anchor=CENTER, text='min')
        self.generalStatsTreeview.heading('max', anchor=CENTER, text='max')
        self.generalStatsTreeview.heading('median', anchor=CENTER, text='med')
        self.generalStatsTreeview.heading('mean', anchor=CENTER, text='mean')
        self.generalStatsTreeview.heading('std', anchor=CENTER, text='std')
        self.generalStatsTreeview.heading('iqr', anchor=CENTER, text='iqr')

        self.generalStatsTreeview.pack(pady=10, padx=10)

        # ==============================================CORRELATION TAB=================================

    def LoadData(self):
        filepath = easygui.fileopenbox()

        if filepath.endswith('.csv'):
            # ====Opening csv file and saving its data to a list of lists
            rows = []
            with open(filepath, 'r', encoding='utf-8') as file:
                csvreader = csv.reader(file)
                self.header = next(csvreader)
                for row in csvreader:
                    rows.append(row)
            self.records = rows
            # ====Parsing unique country names to a list
            self.uniqueCountries = []
            for row in self.records:
                self.uniqueCountries.append(row[-1])
            self.uniqueCountries = np.ndarray.tolist(
                np.unique(np.array(self.uniqueCountries)))
            self.countryComboBox['values'] = (self.uniqueCountries)
            # ====Parsing unique units to a list
            self.uniqueUnit = []
            for row in self.records:
                self.uniqueUnit.append(row[-6])
            self.uniqueUnit = np.ndarray.tolist(
                np.unique(np.array(self.uniqueUnit)))
            self.unitComboBox['values'] = (self.uniqueUnit)

        else:
            print('Datatype not supported')

    def AnalyzeData(self):

        # ====Getting chosen options
        selectedCountry = self.countryComboBox.get()
        selectedUnit = self.unitComboBox.get()
        # ====Parsing readings that fit chosen category
        copiedRecords = copy.deepcopy(self.records)
        selectedData = []
        rawData = []
        for row in copiedRecords:
            if row[-1] == selectedCountry and row[-6] == selectedUnit:
                selectedData.append(row)

        rawData = copy.deepcopy(selectedData)

        # ====Transforming date record to be only month
        for row in selectedData:
            row[-2] = str(parser.parse(row[-2]).month)

        # =============================Data Parsing for boxplot
        # ====Transforming data for graph drawing
        boxPlotData = [[] for i in range(12)]
        for row in selectedData:
            for idx, dataRow in enumerate(boxPlotData):
                if idx == int(row[-2])-1:
                    dataRow.append(float(row[-3]))
        # =============================Data parsing for bar graph
        barGraphData = [[] for i in range(12)]
        for idx, row in enumerate(boxPlotData):
            barGraphData[idx] = len(row)

        # =============================Ploting boxplot
        # ====Clearing boxplot graph
        self.boxPlotFigure.clear()
        self.boxPlotGraph.clear()
        self.boxPlotGraph = self.boxPlotFigure.add_subplot(111)
        # ====Ploting boxplot with a new data
        self.boxPlotGraph.boxplot(boxPlotData)
        self.boxPlotCanvas.draw()

        # =============================Computing variance analysis - ANOVA, Post Hoc and Tukey
        # !====ANOVA giving NaN values in a case where some months have 0 data - With data used it cannot compute answer
        fvalue, pvalue = stats.f_oneway(*boxPlotData)
        print(f'{fvalue}  {pvalue}')
        # ============================Ploting bar graph
        # ====Clearing bar graph
        self.barGraphFigure.clear()
        self.barGraph.clear()
        self.barGraph = self.barGraphFigure.add_subplot(111)
        # ====Ploting bar graph with new data
        bars = self.barGraph.barh(self.monthHeaders, barGraphData)
        self.barGraph.bar_label(bars)
        self.barGraphCanvas.draw()

        # ==================Computing general statistic values for chosen criteria
        # ====Creating treeview data variable wich will contain stats in form of a list of lists
        treeviewData = [[] for i in range(12)]
        for idx, month in enumerate(self.monthHeaders):
            treeviewData[idx].append(month)

        # ====Taking previously parsed boxplot data and converting it to floating point numbers in order to compute their statistic measurements
        for idx, row in enumerate(boxPlotData):
            convertedRow = [float(x) for x in row]
            convertedRow = sorted(convertedRow)

            # ====Series of try-except blocks for every stat - necessery in order to avoid problems, when number of meassurements is insufficient or inexistent
            try:
                treeviewData[idx].append(min(convertedRow))
            except ValueError:
                treeviewData[idx].append(None)

            try:
                treeviewData[idx].append(max(convertedRow))
            except ValueError:
                treeviewData[idx].append(None)

            try:
                treeviewData[idx].append(np.median(convertedRow))
            except ValueError:
                treeviewData[idx].append(None)

            try:
                treeviewData[idx].append(np.mean(convertedRow))
            except RuntimeWarning:
                treeviewData[idx].append(None)

            try:
                treeviewData[idx].append(np.std(convertedRow))
            except ValueError:
                treeviewData[idx].append(None)

            try:
                # TODO Test more possibilities - use better examples etc.
                # !Evaluating IQR not possible - probably not suited variables
                # treeviewData[idx].append(np.median(
                #    sorted(convertedRow[math.floor(len(convertedRow)/2):])) - np.median(sorted(convertedRow[:math.floor(len(convertedRow)/2)])))
                treeviewData[idx].append('iqr')
            except ValueError:
                treeviewData[idx].append(None)

        # ====Deleting previous data from treeview
        for child in self.generalStatsTreeview.get_children():
            self.generalStatsTreeview.delete(child)
        # ====Displaying computed data in respective frame
        for month in treeviewData:
            self.generalStatsTreeview.insert(parent="",
                                             index='end', values=tuple(month))
        self.generalStatsTreeview.pack()
