<a name="readme-top"></a>


<!-- ABOUT THE PROJECT -->
## About The Project

This is my Engineer degree project. It's goal was to create graphical application for performing basic statistical data analysis of air quallity annual data. Data was acquired from [Opendatasoft](https://public.opendatasoft.com/explore/?sort=modified).

Main features:
* Performing all main parameter calculations (i.e. average, mean)
* Performing basic variance analysis
* Performing correlation analysis between two air pollution units
* Creating graphs suited for representing all included analysis

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Pandas][Pandas.io]][Pandas-url]
* [![Tkinter][Tkinter.io]][Tkinter-url]
* [![Scipy][Scipy.io]][Scipy-url]
* [![Matplotlib][Matplotlib.io]][Matplotlib-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!--INSTALLATION-->
## Installation
This application was created with `Python 3.10` and requires external libraries:

1. `Matplotlib`
2. `Statsmodels`
3. `Scipy`
4. `Pandas`

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage
After installing required packages, you can run the program with command:
```sh
python ./src/main.py
```

1. At first, you'll see main application window:

  <p align="center">
    <img src="https://i.imgur.com/VPWCmzX.png" />
  </p>
  
2. In order to start performing tests you need to load data. App ships with 3 sets of data in `static` folder inside project directory. You can load it with menu in upper-left corner of a window:

   <p align="center">
    <img src="https://i.imgur.com/JvAATNs.png" />
   </p>

  Among the data sets you can find `synthetic_data.csv` file which was created for demonstration purpouses and is used in further screenshots.

3. After loading the data you can perform tests distributed between three tabs: `boxplot` - variance analysis, `general` - for general stats (i.e. average, mean) and `correlation` - for correlation analysis. Every tab contains menu for selecting data and performing calculations. Here are examples how all tabs would look after performing all calculations:

   <p align="center">
    <img src="https://i.imgur.com/PGIu5pd.png" />
   </p>

   <p align="center">
    <img src="https://i.imgur.com/ARs67eR.png" />
   </p>

   <p align="center">
    <img src="https://i.imgur.com/hWYRQja.png" />
   </p>
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- DATA FORMATTING -->
## Data formatting
This project was created with specific data format in mind, suited for air pollution data found on [opendatasoft.com](https://public.opendatasoft.com/explore/?sort=modified). However, with careful data formatting it could be used to analyze different data than just air pollution data. Note that data suited for analyzing with included tests should be timestamped data collected troughout entire year with at least 3 measurements per month (Variance analysis requirements).

Used format with example data:

| Country Code | City | Location | Coordinates | Pollutant | Source Name | Unit | Value | Last Updated | Country Label |
| ------------ | ---- | -------- | ----------- | --------- | ----------- | ---- | ----- | ------------ | ------------- |
| PL | Szczecin | Szczecin: ul. Andrzejewskiego | 53.380975:14.663347 | PM10 | GIOS | µg/m³ | 1.5 | 2022-01-12T09:00:00+02:00 | Poland |

Not all data contained in this format is used by application. As of now required columns are: `Pollutant`, `Unit`, `Value`, `Last Updated`, `Country Label`.
* `Pollutant` column is used mainly in correlatiioin analysis. It can contain any name of measured data
* `Unit` as name suggest is column containing units of measurements - used for graph labeling
* `Value` value of measured data
* `Last Updated` is a timestamp column. It can be formated in any standard way thanks to included date parser. However it has to include month of measurement.
* `Country label` column containing name that defines set of data. For air pollution it is a country name


<!-- Prospect of developement -->
## Prospect of developement
Application could be extended with another features, for example:
* Unifig naming of different columns in source code to make using different sets of data easier
* Saving calculated results
* Add other file format support
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Piotr Snarski - snarski.piotrek@gmail.com

Project Link: [https://github.com/H33Kz/CovidStatsSummary](https://github.com/H33Kz/CovidStatsSummary)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Pandas.io]:https://img.shields.io/badge/Pandas-green?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]:https://pandas.pydata.org/docs/

[Tkinter.io]:https://img.shields.io/badge/Tkinter-blue?style=for-the-badge&logo=python&logoColor=white
[Tkinter-url]:https://tkdocs.com/

[Scipy.io]:https://img.shields.io/badge/Scipy-purple?style=for-the-badge&logo=scipy&logoColor=white
[Scipy-url]:https://docs.scipy.org/doc/scipy/

[Matplotlib.io]:https://img.shields.io/badge/Matplotlib-yellow?style=for-the-badge&logo=python&logoColor=white
[Matplotlib-url]:https://matplotlib.org/
