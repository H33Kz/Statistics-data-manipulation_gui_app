from tkinter.ttk import Combobox, Notebook, Treeview
from tkinter import *
from dateutil import parser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os
import easygui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# * Old libraries - functionality duplicated by pandas
# import csv
# import copy


class appMenu():
    def __init__(self, root, geometry, title):
        # =========Initiating empty variables for plot data
        # self.uniqueCountries = ['No data']
        # self.uniqueUnit = ['No data']
        pd.set_option('display.float_format', lambda x: '%.2f' % x)
        self.monthHeaders = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                             'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # =========Title and geometry setup
        self.root = root
        self.root.geometry(
            f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()-100}+0+0')
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
        self.countryComboBox['values'] = ('nodata')
        self.countryComboBox['state'] = 'readonly'
        self.countryComboBox.pack(padx=10, pady=10)
        # ===Unit selection
        self.unitLabel = Label(self.boxPlotSelectionFrame, text='Unit:')
        self.unitLabel.pack()
        self.unitComboBox = Combobox(self.boxPlotSelectionFrame)
        self.unitComboBox['values'] = ('nodata')
        self.unitComboBox['state'] = 'readonly'
        self.unitComboBox.pack(padx=10, pady=10)
        # ===Initialize analysys button
        self.analyseButton = Button(
            self.boxPlotSelectionFrame, text='Analyze data', command=self.AnalyzeData)
        self.analyseButton.pack(padx=10, pady=10)
        # ===Exit button
        self.exitButton1 = Button(
            self.boxPlotSelectionFrame, text='Exit app', command=self.root.quit)
        self.exitButton1.pack(padx=10, pady=10)
        # ====Variance analysis frame
        self.varianceAnalysysFrame = Frame(self.boxPlotTab)
        self.varianceAnalysysFrame.grid(column=0, row=2, sticky=NSEW)
        # ====ANOVA frame
        self.anovaFrame = Frame(self.varianceAnalysysFrame)
        self.anovaFrame.grid(column=0, row=0)
        # ====ANOVA text field
        self.anovaTextField = Text(
            self.anovaFrame, width=50, state='disabled', font=("Helvetica", 10))
        self.anovaTextField.pack(padx=10, pady=10)
        # ====PostHoc frame
        self.posthocFrame = Frame(self.varianceAnalysysFrame)
        self.posthocFrame.grid(column=1, row=0)
        # ====PostHoc text field
        self.posthocTextField = Text(
            self.posthocFrame, width=50, state='disabled', font=("Helvetica", 10))
        self.posthocTextField.pack(padx=10, pady=10)
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
        self.barGraphToolbar = NavigationToolbar2Tk(
            self.barGraphCanvas, self.barGraphToolbarFrame)
        # =========Selection frame
        self.barGraphSelectionFrame = Frame(self.generalStatsTab)
        self.barGraphSelectionFrame.grid(column=1, row=0, sticky=N)
        # ==Exit Button
        self.exitButton2 = Button(
            self.barGraphSelectionFrame, text='Exit app', command=self.root.quit)
        self.exitButton2.pack(padx=10, pady=10)
        # * Old code - exchanged for text frame for pandas report
        # # ==========Treeview frame
        # self.treeviewFrame = Frame(self.generalStatsTab)
        # self.treeviewFrame.grid(column=0, row=2, sticky=NSEW)
        # # ======Treeview(Table for general information)
        # self.generalStatsTreeview = Treeview(self.treeviewFrame, show='headings', columns=(
        #     'month', 'min', 'max', 'median', 'mean', 'std', 'iqr'))
        # # ====Setting up coulmns
        # self.generalStatsTreeview.column('month', anchor=W, width=60)
        # self.generalStatsTreeview.column('min', anchor=W, width=60)
        # self.generalStatsTreeview.column('max', anchor=W, width=60)
        # self.generalStatsTreeview.column('median', anchor=W, width=60)
        # self.generalStatsTreeview.column('mean', anchor=W, width=60)
        # self.generalStatsTreeview.column('std', anchor=W, width=60)
        # self.generalStatsTreeview.column('iqr', anchor=W, width=60)
        # # ====Setting up names for columns
        # self.generalStatsTreeview.heading('month', anchor=CENTER, text='mth')
        # self.generalStatsTreeview.heading('min', anchor=CENTER, text='min')
        # self.generalStatsTreeview.heading('max', anchor=CENTER, text='max')
        # self.generalStatsTreeview.heading('median', anchor=CENTER, text='med')
        # self.generalStatsTreeview.heading('mean', anchor=CENTER, text='mean')
        # self.generalStatsTreeview.heading('std', anchor=CENTER, text='std')
        # self.generalStatsTreeview.heading('iqr', anchor=CENTER, text='iqr')

        # self.generalStatsTreeview.pack(pady=10, padx=10)

        # ======Textfield frame
        self.generalStatsTextFieldFrame = Frame(self.generalStatsTab)
        self.generalStatsTextFieldFrame.grid(column=0, row=2, sticky=NSEW)
        # ======Textfield
        self.generalStatsTextField = Text(
            self.generalStatsTextFieldFrame, width=80, state='disabled', font=("Helvetica", 10))
        self.generalStatsTextField.pack(padx=10, pady=10)

        # ==============================================CORRELATION TAB=================================
        # =========Plot frame
        self.correlGraphFrame = Frame(self.correlationTab)
        self.correlGraphFigure = plt.figure(figsize=(10, 6), dpi=100)
        self.correlGraph = self.correlGraphFigure.add_subplot(111)
        self.correlGraphCanvas = FigureCanvasTkAgg(
            self.correlGraphFigure, self.correlGraphFrame)
        self.correlGraphCanvas.get_tk_widget().pack()
        self.correlGraphCanvas.draw()
        self.correlGraphFrame.grid(column=0, row=0)
        # =========Toolbar frame
        self.correlGraphToolbarFrame = Frame(self.correlationTab)
        self.correlGraphToolbarFrame.grid(column=0, row=1)
        self.correlGraphToolbar = NavigationToolbar2Tk(
            self.correlGraphCanvas, self.correlGraphToolbarFrame)
        # =========Selection frame
        self.correlGraphSelectionFrame = Frame(self.correlationTab)
        self.correlGraphSelectionFrame.grid(column=1, row=0, sticky=N)
        # ==Exit Button
        self.exitButton3 = Button(
            self.correlGraphSelectionFrame, text='Exit app', command=self.root.quit)
        self.exitButton3.pack(padx=10, pady=10)
        # ===Country selection
        self.correlCountryLabel = Label(
            self.correlGraphSelectionFrame, text='Country:')
        self.correlCountryLabel.pack()
        self.correlCountryComboBox = Combobox(self.correlGraphSelectionFrame)
        self.correlCountryComboBox['values'] = ('nodata')
        self.correlCountryComboBox['state'] = 'readonly'
        self.correlCountryComboBox.pack(padx=10, pady=10)
        # ===First unit selection
        self.firstUnitLabel = Label(
            self.correlGraphSelectionFrame, text='First unit:')
        self.firstUnitLabel.pack()
        self.firstUnitComboBox = Combobox(self.correlGraphSelectionFrame)
        self.firstUnitComboBox['values'] = ('nodata')
        self.firstUnitComboBox['state'] = 'readonly'
        self.firstUnitComboBox.pack(padx=10, pady=10)
        # ===Unit selection
        self.secondUnitLabel = Label(
            self.correlGraphSelectionFrame, text='Second Unit:')
        self.secondUnitLabel.pack()
        self.secondUnitComboBox = Combobox(self.correlGraphSelectionFrame)
        self.secondUnitComboBox['values'] = ('nodata')
        self.secondUnitComboBox['state'] = 'readonly'
        self.secondUnitComboBox.pack(padx=10, pady=10)
        # ===Initialize analysis button
        self.checkCorrelButton = Button(
            self.correlGraphSelectionFrame, text='Check for correlation', command=self.CorrelationAnalysis)
        self.checkCorrelButton.pack(padx=10, pady=10)

    def LoadData(self):
        filepath = easygui.fileopenbox()

        if filepath.endswith('.csv'):
            # * Old code - without usage of pandas
            # ====Opening csv file and saving its data to a list of lists
            # rows = []
            # with open(filepath, 'r', encoding='utf-8') as file:
            #     csvreader = csv.reader(file)
            #     self.header = next(csvreader)
            #     for row in csvreader:
            #         rows.append(row)
            # self.records = rows
            # # ====Parsing unique country names to a list
            # self.uniqueCountries = []
            # for row in self.records:
            #     self.uniqueCountries.append(row[-1])
            # self.uniqueCountries = np.ndarray.tolist(
            #     np.unique(np.array(self.uniqueCountries)))
            # self.countryComboBox['values'] = (self.uniqueCountries)
            # # ====Parsing unique units to a list
            # self.uniqueUnit = []
            # for row in self.records:
            #     self.uniqueUnit.append(row[-6])
            # self.uniqueUnit = np.ndarray.tolist(
            #     np.unique(np.array(self.uniqueUnit)))
            # self.unitComboBox['values'] = (self.uniqueUnit)
            df = pd.read_csv(filepath, sep=',')
            uniqueCountries = pd.unique(df['Country Label'])
            self.countryComboBox['values'] = uniqueCountries.tolist()
            self.correlCountryComboBox['values'] = uniqueCountries.tolist()

            uniqueUnit = pd.unique(df['Pollutant'])
            self.unitComboBox['values'] = uniqueUnit.tolist()
            self.firstUnitComboBox['values'] = uniqueUnit.tolist()
            self.secondUnitComboBox['values'] = uniqueUnit.tolist()
            self.Dataframe = df

        else:
            print('Datatype not supported')

    def AnalyzeData(self):
        # ====Using methods to perform different means of data analysys
        selectedData = self.ParseSelectedData(
            selectedCountry=self.countryComboBox.get(), selectedUnit=self.unitComboBox.get())
        boxPlotData = self.CreateBoxPlot(selectedData=selectedData)
        barGraphData = self.CreateBarGraph(boxPlotData=boxPlotData)
        self.GenerateGeneralStats(boxPlotData=boxPlotData)
        self.VarianceAnalysis(boxPlotData=boxPlotData)

    def VarianceAnalysis(self, boxPlotData):
        # =============================Computing variance analysis - ANOVA, Post Hoc TukeyHSD
        # ====ANOVA
        # df = pd.DataFrame(boxPlotData)
        # df = df.transpose()
        # df.columns = self.monthHeaders

        df = boxPlotData
        fvalue, pvalue = stats.f_oneway(df['Jan'], df['Feb'], df['Mar'], df['Apr'], df['May'],
                                        df['Jun'], df['Jul'], df['Aug'], df['Sep'], df['Oct'], df['Nov'], df['Dec'])

        self.anovaTextField['state'] = 'normal'
        self.anovaTextField.insert(
            END, f'ANOVA:\nF={fvalue}   p={pvalue}\nWARNING: If number of data points in any of the\n months is <0 then ANOVA test will evaluate\n only non empty ones')
        self.anovaTextField['state'] = 'disabled'
        self.anovaTextField.pack()

        # ====TukeyHSD
        df_melt = pd.melt(df.reset_index(), id_vars=[
                          'index'], value_vars=self.monthHeaders)

        p_tukey = pairwise_tukeyhsd(df_melt['value'], df_melt['variable'])
        result = str(p_tukey._results_table)

        # Another tukey analysis - not used
        # result = stats.tukey_hsd(df['Jan'], df['Feb'], df['Mar'], df['Apr'], df['May'],
        #                          df['Jun'], df['Jul'], df['Aug'], df['Sep'], df['Oct'], df['Nov'], df['Dec'])

        self.posthocTextField['state'] = 'normal'
        self.posthocTextField.insert(END, result)
        self.posthocTextField['state'] = 'disabled'
        self.posthocTextField.pack()

    def CorrelationAnalysis(self):
        # ====Parse selected data for correlation
        firstUnitData = self.ParseSelectedData(
            selectedCountry=self.correlCountryComboBox.get(), selectedUnit=self.firstUnitComboBox.get())
        secondUnitData = self.ParseSelectedData(
            selectedCountry=self.correlCountryComboBox.get(), selectedUnit=self.secondUnitComboBox.get())

        correlationData = pd.DataFrame()
        correlationData['first pollutant'] = firstUnitData.loc[(firstUnitData['Last Updated'] ==
                                                               secondUnitData['Last Updated']) & (firstUnitData['Source Name'] == secondUnitData['Source Name']), 'Value'].values
        correlationData['second pollutant'] = secondUnitData.loc[(secondUnitData['Last Updated'] ==
                                                                 firstUnitData['Last Updated']) & (secondUnitData['Source Name'] == firstUnitData['Source Name']), 'Value'].values
        print(correlationData)

    def ParseSelectedData(self, selectedCountry, selectedUnit):
        # * Old code - without usage of pandas
        # # ====Parsing readings that fit chosen category
        # copiedRecords = copy.deepcopy(self.records)
        # selectedData = []
        # for row in copiedRecords:
        #     if row[-1] == selectedCountry and row[-6] == selectedUnit:
        #         selectedData.append(row)

        # # ====Transforming date record to be only month and measurements to be float
        # for row in selectedData:
        #     row[-2] = str(parser.parse(row[-2]).month)
        #     row[-3] = float(row[-3])

        resultDataFrame = self.Dataframe.copy()
        resultDataFrame = resultDataFrame[resultDataFrame['Country Label']
                                          == selectedCountry]
        resultDataFrame = resultDataFrame[resultDataFrame['Pollutant']
                                          == selectedUnit]
        resultDataFrame['Last Updated'] = resultDataFrame['Last Updated'].apply(
            lambda x: str(parser.parse(x).day)+'.'+str(parser.parse(x).month))

        return resultDataFrame

    def CreateBoxPlot(self, selectedData):
        # * Old code - without pandas
        # # =============================Data Parsing for boxplot
        # # ====Transforming data for graph drawing
        # boxPlotData = [[] for i in range(12)]
        # for row in selectedData:
        #     for idx, dataRow in enumerate(boxPlotData):
        #         if idx == int(row[-2])-1:
        #             dataRow.append(float(row[-3]))

        # =============================Data Parsing for boxplot
        # ====Transforming data for graph drawing
        selectedData['Last Updated'] = selectedData['Last Updated'].apply(
            lambda x: str(x).split('.')[1])

        boxPlotData = pd.DataFrame()
        for i in range(12):
            boxPlotData[str(i+1)] = pd.Series(selectedData.loc[selectedData['Last Updated']
                                                               == str(i + 1), 'Value'].values)
        boxPlotData.columns = self.monthHeaders

        # =============================Ploting boxplot
        # ====Clearing boxplot graph
        self.boxPlotFigure.clear()
        self.boxPlotGraph.clear()
        self.boxPlotGraph = self.boxPlotFigure.add_subplot(111)
        # ====Ploting boxplot with a new data
        self.boxPlotGraph.boxplot(boxPlotData, labels=self.monthHeaders)
        self.boxPlotCanvas.draw()

        return boxPlotData

    def CreateBarGraph(self, boxPlotData):
        # =============================Data parsing for bar graph
        # barGraphData = [[] for i in range(12)]
        # for idx, row in enumerate(boxPlotData):
        #     barGraphData[idx] = len(row)

        barGraphData = boxPlotData.count()
        barGraphData = barGraphData.to_frame()
        barGraphData = barGraphData.transpose()

        # ============================Ploting bar graph
        # ====Clearing bar graph
        self.barGraphFigure.clear()
        self.barGraph.clear()
        self.barGraph = self.barGraphFigure.add_subplot(111)
        # ====Ploting bar graph with new data
        bars = self.barGraph.barh(
            self.monthHeaders, barGraphData.values.tolist()[0])
        self.barGraph.bar_label(bars)
        self.barGraphCanvas.draw()

        return barGraphData

    def GenerateGeneralStats(self, boxPlotData):
        # * Old code - without using pandas
        # # ==================Computing general statistic values for chosen criteria
        # # ====Creating treeview data variable wich will contain stats in form of a list of lists
        # treeviewData = [[] for i in range(12)]
        # for idx, month in enumerate(self.monthHeaders):
        #     treeviewData[idx].append(month)

        # # ====Taking previously parsed boxplot data and converting it to floating point numbers in order to compute their statistic measurements
        # for idx, row in enumerate(boxPlotData):
        #     convertedRow = [float(x) for x in row]
        #     convertedRow = sorted(convertedRow)

        #     # ====Series of try-except blocks for every stat - necessery in order to avoid problems, when number of meassurements is insufficient or inexistent
        #     try:
        #         treeviewData[idx].append(min(convertedRow))
        #     except ValueError:
        #         treeviewData[idx].append(None)

        #     try:
        #         treeviewData[idx].append(max(convertedRow))
        #     except ValueError:
        #         treeviewData[idx].append(None)

        #     try:
        #         treeviewData[idx].append(np.median(convertedRow))
        #     except ValueError:
        #         treeviewData[idx].append(None)

        #     try:
        #         treeviewData[idx].append(np.mean(convertedRow))
        #     except RuntimeWarning:
        #         treeviewData[idx].append(None)

        #     try:
        #         treeviewData[idx].append(np.std(convertedRow))
        #     except ValueError:
        #         treeviewData[idx].append(None)

        #     try:
        #         # TODO Test more possibilities - use better examples etc.
        #         # !Evaluating IQR not possible - probably not suited variables
        #         # treeviewData[idx].append(np.median(
        #         #    sorted(convertedRow[math.floor(len(convertedRow)/2):])) - np.median(sorted(convertedRow[:math.floor(len(convertedRow)/2)])))
        #         treeviewData[idx].append('iqr')
        #     except ValueError:
        #         treeviewData[idx].append(None)

        # # ====Deleting previous data from treeview
        # for child in self.generalStatsTreeview.get_children():
        #     self.generalStatsTreeview.delete(child)
        # # ====Displaying computed data in respective frame
        # for month in treeviewData:
        #     self.generalStatsTreeview.insert(parent="",
        #                                      index='end', values=tuple(month))
        # self.generalStatsTreeview.pack()

        self.generalStatsTextField['state'] = 'normal'
        self.generalStatsTextField.insert(
            END, boxPlotData.describe().transpose())
        self.generalStatsTextField['state'] = 'disabled'
        self.generalStatsTextField.pack()
