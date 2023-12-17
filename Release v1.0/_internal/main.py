import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import math as math
import numpy as np
import os ,sys
from scipy import stats
import time



class Multiple_files: 

    def __init__(self, directory_path):
        # initiates the class object
        self.dir_path = directory_path
        self.files = self.get_file_directories()
        self.name_of_the_file = ''

    def get_file_directories(self): 
        # Function to get list of .xml files in given directory 
        dir_list = []
        # Write a loop that iterates over the content of the directory and search for .xml files:
        for file in sorted(os.listdir(self.dir_path), key=lambda x: int(x.replace('.xml','').split('_')[3])):
            if not file.endswith('.xml'): continue
            fullname = os.path.join(self.dir_path, file)
            dir_list.append(fullname)    
        return dir_list
    
    def import_xml_file(self,path):
    # transforms .xml file into pandas dataframe object by path to file given
        tree = ET.parse(path)
        root = tree.getroot()
        columns = [root[1][0][9][0][0].text,root[1][0][9][1][0].text]
        wavelength = []
        absorbance = []

        for i in range(10,len(root[1][0]),1):
            wavelength.append(float(root[1][0][i][0][0].text))
            absorbance.append(float(root[1][0][i][1][0].text))

        measurements = {columns[0]: wavelength, columns[1]: absorbance}

        df = pd.DataFrame.from_dict(measurements, orient='columns')

        return df

    def get_name_of_file(self):
    # Function that returns names of the files in given directory
        for i in self.files:
            tree = ET.parse(i)
            root = tree.getroot()
            name_of_the_file = root[1].attrib['{urn:schemas-microsoft-com:office:spreadsheet}Name']
            yield name_of_the_file


    def import_multiple_xml(self):
    # Function that imports .xml files from given directory and returns pandas dataframe object  
        for i in self.files:
            df = self.import_xml_file(i)
            yield df

    def export_to_excel(self, name_of_the_samples = ''):
    # Function that .xml files from given directory and returns Excel file with all the samples
        if name_of_the_samples == '':
            name_of_the_samples = []
            for i in self.get_name_of_file():
                name_of_the_samples.append(i)
        else:
            name_of_the_samples = list(name_of_the_samples.split(','))

        date = str(time.strftime('%d-%m-%Y_%H-%M-%S'))
        filename = f'merged_data_{date}.xlsx'
        path = os.path.join(os.path.dirname(__file__),str('merged_files'),str(filename))
        if_first = True
        for i,j  in zip(self.import_multiple_xml(), name_of_the_samples):
            if if_first:
                merged_data = i
                merged_data.rename(columns = {'Abs': f'ABS {j} [-]'}, inplace = True)
                if_first = False
                continue
            
            extract_col = i['Abs']
            merged_data = pd.concat([merged_data, extract_col.rename(f'ABS {j} [-]')], axis=1)

            merged_data.to_excel(excel_writer=path, sheet_name='Measurments', index=False)

    def draw_multiple_plot(self, x_min = 200, x_max = 700, y_min = 0, y_max = 3, title='', labels = ''):  
    
    # draws absorbance versus concentration graph for imported files       
       
       if labels == '': labels = []
       else: labels = list(labels.split(','))

       # path to directory images, where all figures are being saved
       date = str(time.strftime('%d-%m-%Y_%H-%M-%S'))
       filename =f'uv-vis-spectra_{date}.png'
       path = os.path.join(os.path.dirname(__file__),str('graphs'),str(filename))
       
       if labels != []: # adds custom labels
        for i,j in zip(self.import_multiple_xml(),labels):
            # deafult name of dataset is equal to name of the file
            plt.plot(i['nm'], i['Abs'],linestyle='-', linewidth=2, label=f'{j} ppm')
       
       elif labels == []: # adds name of the files into labels
        for i,j in zip(self.import_multiple_xml(),self.get_name_of_file()):
            # deafult name of dataset is equal to name of the file
            plt.plot(i['nm'], i['Abs'],linestyle='-', linewidth=2, label=j)
       
       # other params of the plot
       plt.xlim(x_min,x_max) # by deafult it's the maximum range of the spectrophotometer
       plt.ylim(y_min,y_max) # by deafult it's the common absorbance range (0.0-3.0)
       plt.xlabel(r'$\lambda$ [nm]')
       plt.ylabel('ABS [-]')
       plt.grid(lw = 0.5, c = 'lightgrey')
       plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
       plt.title(title)
       
       # saving plot into directory \images
       plt.savefig(path, bbox_inches='tight')

       plt.clf()
       plt.cla()
       
       return path
       
        
    def maximum_absorbance_list(self,wavelength):
    # returns dictionary, where key is wavelength and values are absorbances for all the samples given
        abs = []
        for df in self.import_multiple_xml():
            index = df.index[df['nm']==wavelength]
            abs.append(df['Abs'][index[0]])
        return abs

    def scatter_plot(self,wavelength,concentrations,title = '', drop = '', show = True, regression = True , color='blue', marker = 'o', col_rej = 'red'):
        
        concentrations = list(concentrations.split(','))
        concentrations = list(float(x) for x in concentrations)
        if drop == '': drop = []
        else: drop = list(drop.split(','))
        drop = list(float(x) for x in drop)
        
        # creates path where generated plot will be saved
        date = str(time.strftime('%d-%m-%Y_%H-%M-%S'))
        filename =f'plot_for_wavelength_{wavelength}_nm_{date}.png'        
        path = os.path.join(os.path.dirname(__file__),str('graphs'), str(filename))
        
        # creates dictionary where there are two positions: concentrations and absorbance of samples
        dict = {'C [ppm]': concentrations,f'ABS ({wavelength}) [-]': self.maximum_absorbance_list(wavelength)}
        
        # creates dataframe from dict
        data = pd.DataFrame(dict) 

        # if user wants to reject one of the samples from series
        # show = True => rejected samples are shown on the plot
        if drop != []:
            if show:
                # creates axes of the plot
                plt.ylim(0,data[f'ABS ({wavelength}) [-]'].max()*1.1) # by deafult it's the maximum range of the spectrophotometer
                plt.xlim(0,data['C [ppm]'].max()*1.1) # by deafult it's the common absorbance range (0.0-3.0)    
                # creates series with all the samples
                plt.scatter(data['C [ppm]'], data[f'ABS ({wavelength}) [-]'], linestyle='-', linewidth=2, label='Rejected samples', marker= marker, c=col_rej)
            # drops given values from dataframe
            for i in drop:
                data.drop(data[data['C [ppm]'] == i].index.values, axis = 'index', inplace=True)

        plt.scatter(data['C [ppm]'], data[f'ABS ({wavelength}) [-]'], linestyle='-', linewidth=2, label=f'Absorbance for {wavelength} nm', marker= marker, c=color)
        
        if regression:
            # returns parameters of regression
            a, b, r, p, std_err = stats.linregress(data['C [ppm]'], data[f'ABS ({wavelength}) [-]'])
            
            # equations on the plot 
            eq1 = f'y = {round(a,4)}' + r'$*x$' + f' + {round(b,4)}'
            eq2 = r'$R^2 =$' + str(round(r,4))
            
            # generates the regression
            plt.plot(data['C [ppm]'], a*data['C [ppm]']+b, color=color)
            
            # Equation next to the plot
            plt.figtext(1.08, 0.25, f'{eq1}\n{eq2}', ha='center', fontsize=12, bbox={'facecolor':'white', 'alpha':0.5, 'pad':5})

        if not show:
            # creates axes of the plot if they weren't generated earlier
            plt.ylim(0,data[f'ABS ({wavelength}) [-]'].max()*1.1) # by deafult it's the maximum range of the spectrophotometer
            plt.xlim(0,data['C [ppm]'].max()*1.1) # by deafult it's the common absorbance range (0.0-3.0)
        
        # generates title of the plot if title = '' there will be no title
        plt.title(title)
        
        # sets labels of the axes
        plt.xlabel('C [ppm]')
        plt.ylabel('ABS [-]')
        
        # generates legend
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        
        # saves plot as a figure in given directory
        plt.savefig(path, bbox_inches='tight')
        
        plt.clf()
        plt.cla()

        return path
    
    def __del__(self):
        print('Class destroyed')






