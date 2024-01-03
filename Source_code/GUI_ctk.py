import tkinter as tk
from customtkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import subprocess
from main import *

class ImageFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.result_label = CTkLabel(self, 
                                     text="Generated Image", 
                                     width=700,
                                     height=500,
                                     corner_radius=30,
                                     font=('Helvetica', 16, 'bold'),
                                     fg_color=('#E7E9F1','#2A2B40'),
                                    )                              
        self.result_label.pack(expand = True, fill = tk.BOTH, padx = 20, pady = 20, anchor = 'center')

    @staticmethod
    def show_image(image_path):
        try:
            program_image =CTkImage(Image.open(image_path), size=(700, 500))
            window.image_frame.result_label.configure(image=program_image, text = '')
            window.image_frame.result_label.image = program_image
            
        except Exception as e:
            messagebox.showerror('Error', f'Error loading image: {str(e)}')


class FunctionsFrame(CTkFrame):
    def __init__(self, master, header_name = "UV-Vis SPECTRA",  **kwargs):
        super().__init__(master, **kwargs)
        
        self.headher_name=header_name
        self.grid_columnconfigure((0), weight=0)
        self.grid_rowconfigure((0), weight=0)

        label1_text = 'Pass directory of your folder with data*'
        label2_text = 'Pass concentrations of the samples in increasing order [ppm]'
        label3_text = 'Concentrations of the samples*'
        label4_text = 'Pass wavelength to plot*'
        label5_text = 'Rejected samples (pass labels)'
        checkbox_1_text = 'Show rejected samples in the plot'
        checkbox_2_text = 'Make linear regression'

        self.uv_vis_label = CTkLabel(self, text=self.headher_name, font=('Helvetica', 16, 'bold'))
        self.uv_vis_label.grid(row=0, column=0, padx=(10,10), pady=(10, 10), sticky="nse")
        program_image =CTkImage(Image.open(os.path.join(os.path.dirname(__file__),str('icon.png'))), size=(75, 75))
        self._image = CTkLabel(self, text = '', image=program_image)
        self._image.grid(row=0, column=3, padx=(10,10), pady=(10, 10), sticky="e")
        

        self.switch_var = StringVar(value='light')
        self.switch = CTkSwitch(self, text= 'LIGHT/DARK', text_color=('#000000','#FFFFFF'), button_color=('#CED1D9','#FFFFFF'), progress_color ='#4158D0', fg_color=('#9B9DA3', '#4158D0'), command=self.switch_event, variable=self.switch_var, onvalue="dark", offvalue="light")
        self.switch.grid(row=1, column=0, padx=(10,10), pady=(10, 10), sticky="nsew")
        
        self.make_spectra_label = CTkLabel(self, text="Make UV-Vis spectra", font=('Helvetica', 14, 'bold'))
        self.make_spectra_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.entry1 = CTkEntry(self, fg_color=('white','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=label1_text, width=500, text_color=('#000000','#FFFFFF'))
        self.entry1.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.import_button = CTkButton(self, text="Import Folder", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0',command=self._import_folder)
        self.import_button.grid(row=3, column=2, columnspan=5, padx=10, sticky="e")

        self.entry2 = CTkEntry(self, fg_color=('white','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=label2_text, width=400, text_color=('#000000','#FFFFFF'))
        self.entry2.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        
        self.merge_button = CTkButton(self, text="Merge All Files", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0',width=200, height=40, command=self._merge_all_files)
        self.merge_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky = 'nsw')
        
        self.draw_spectra_button = CTkButton(self, text="Draw Spectra", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0',width=200, height=40, command=self.draw_spectra)
        self.draw_spectra_button.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky = 'nsew')

        # Second function of the programm - makes graph from selected wavelength
        # Label for title
        self.draw_curve_label = CTkLabel(self, text="Draw curve for specific wavelength", font=('Helvetica', 14, 'bold'))
        self.draw_curve_label.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.draw_curve_label.configure(anchor='center')

        # Label for labels of the samples
        self.entry3 = CTkEntry(master=self, fg_color=('white','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=label3_text, width=400, text_color=('#000000','#FFFFFF'))
        self.entry3.grid(row=9, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Label for wavelength to plot
        self.entry4 = CTkEntry(master=self, fg_color=('white','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=label4_text, width=400, text_color=('#000000','#FFFFFF'))
        self.entry4.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Labels for the rejected samples
        self.entry5 = CTkEntry(master=self, fg_color=('white','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=label5_text, width=400, text_color=('#000000','#FFFFFF'))
        self.entry5.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")


        # Checkbox if user wants to show rejected samples in the plot
        self.checkbox_var_1 = tk.BooleanVar()
        self.checkbox_1 = CTkCheckBox(master=self, text=checkbox_1_text, variable=self.checkbox_var_1, 
                               fg_color='#4158D0', hover_color='#C850C0', checkbox_height=20, checkbox_width=20, corner_radius=15)
        self.checkbox_1.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Checkbox if user wants to make linear regression to the plot
        self.checkbox_var_2 = tk.BooleanVar()
        self.checkbox_2 = CTkCheckBox(master=self, text=checkbox_2_text, variable=self.checkbox_var_2, 
                               fg_color='#4158D0', hover_color='#C850C0', checkbox_height=20, checkbox_width=20, corner_radius=15)
        self.checkbox_2.grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Create button for drawing linear plot 
        self.draw_linear_plot_button = CTkButton(master = self, text="Draw Linear Plot", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0',width=350, height=40, command=self.draw_linear_plot)
        self.draw_linear_plot_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Create button for opening image directory
        self.open_image_directory_button = CTkButton(master = self, text="Open Image Directory", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0',width=350, height=40, command=self._open_image_directory)
        self.open_image_directory_button.grid(row=15, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        
        self.tab_view = TabView(master=self, width = 300, height = 300, corner_radius = 20, 
                                border_width = 2, border_color =('#CDCFD6','#18122B'), 
                                fg_color = ('#E6E9F1','#2A2B40'), 
                                bg_color = ('white','#1A1E32'),
                                text_color = ('#F3F7FF', '#F3F7FF'),
                                segmented_button_fg_color = ('#E6E9F1','#18122B'),
                                segmented_button_selected_color = '#4158D0',
                                segmented_button_selected_hover_color = '#4158D0',
                                segmented_button_unselected_color = ('#AAADB3','#18122B'),
                                segmented_button_unselected_hover_color = '#C850C0')
        self.tab_view.grid(row=16, column=0, padx=20, pady=10)

        # Create a Reset button
        self.reset = CTkButton(master = self, text="Reset", corner_radius=32, 
                                  fg_color = '#4158D0', hover_color='#C850C0', command=self.reset_options)
        self.reset.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")


    def switch_event(self):
        set_appearance_mode(self.switch_var.get())

        
    def _merge_all_files(self):
        
        folder_path = self.entry1.get()
        concentrations = self.entry2.get()
        self.directory = Multiple_files(folder_path)
        self.directory.export_to_excel(name_of_the_samples=concentrations)
        self._open_merged_files()

    def _import_folder(self):
        folder_path = filedialog.askdirectory()
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, folder_path)
    
    def _open_merged_files(self):
        export_path = os.path.join(os.path.dirname(__file__),str('merged_files'))
        subprocess.Popen(['explorer', export_path], shell=True)
        
        
    def draw_spectra(self):
        try:    
            folder_path = self.entry1.get()
            concentrations = self.entry2.get()
            self.directory = Multiple_files(folder_path)
            self.result = self.tab_view.processing_data_draw_spectra()
            self.path = self.directory.draw_multiple_plot(x_min = self.result['x_min'], x_max = self.result['x_max'], y_min = self.result['y_min'], y_max = self.result['y_max'], title=self.result['title'], labels=concentrations)
            self.show_image()

        except ValueError as e:
                messagebox.showerror('Error', f'Error with input value: {str(e)}')
        except Exception as e:
                messagebox.showerror('Error', f'Error with drawing plot function: {str(e)}')

    def show_image(self):
        path = self.path
        ImageFrame.show_image(path)


    def _open_image_directory(self):
        image_directory = os.path.join(os.path.dirname(__file__),str('graphs'))
        subprocess.Popen(['explorer', image_directory], shell=True)
    
    def draw_linear_plot(self):
        try:
            folder_path = self.entry1.get()
            labels_of_samples = self.entry3.get()
            wavelength = int(self.entry4.get())
            show = self.checkbox_var_1.get()
            regression = self.checkbox_var_2.get()
            rejected_samples = self.entry5.get()
            self.directory = Multiple_files(folder_path)
            self.result = self.tab_view.processing_data_linear_plot()
            self.path = self.directory.scatter_plot(wavelength=wavelength,
                                                    concentrations=labels_of_samples, 
                                                    title = self.result['title_lin'], 
                                                    drop = rejected_samples, 
                                                    show = show, 
                                                    regression = regression, 
                                                    color = self.result['color'], 
                                                    marker= self.result['marker'], 
                                                    col_rej = self.result['col_rej'])
            self.show_image()

        except ValueError as e:
            messagebox.showerror('Error', f'Error with input value: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Error with drawing plot function: {str(e)}')


    def reset_options(self):
        i = 0
        # reset all widgets 
        for widget in self.winfo_children():
            if isinstance(widget,CTkEntry):
                widget.delete(0,'end')
            if isinstance(widget,CTkCheckBox):
                self.checkbox_var_1.set(False)
                self.checkbox_var_2.set(False)
        
        # reset all widgets in tabview
        for tab in window.functions_frame.tab_view.winfo_children():
            for widget in tab.winfo_children():                      
                if isinstance(widget,CTkEntry):
                    widget.delete(0,'end')
                if isinstance(widget,CTkComboBox):
                    if i == 0: 
                        widget.set('blue')
                    if i == 1: 
                        widget.set('circle')
                    if i == 2: 
                        widget.set('red')
                    i+=1



class TabView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        tab_1 = self.add('Options for Draw Spectra')
        tab_2 = self.add('Options for Draw Linear Plot')

        x_min = 'Min. value of x [nm]: (200)'
        self.text_var_x_min = tk.StringVar(value=200)
        self.x_min_entry = CTkEntry(master= tab_1, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=x_min, width=300, text_color=('#000000','#FFFFFF'))
        self.x_min_entry.grid(row=0, column=0, padx=10, pady=10)
        
        x_max = 'Max. value of x [nm]: (700)'
        self.x_max_entry = CTkEntry(master= tab_1, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=x_max, width=300, text_color=('#000000','#FFFFFF'))
        self.x_max_entry.grid(row=1, column=0, padx=10, pady=10)

        y_min = 'Min. value of y [nm]: (0)'
        self.y_min_entry = CTkEntry(master= tab_1, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=y_min, width=300, text_color=('#000000','#FFFFFF'))
        self.y_min_entry.grid(row=2, column=0, padx=10, pady=10)

        y_max = 'Max. value of y [nm]: (3)'
        self.y_max_entry = CTkEntry(master= tab_1, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=y_max, width=300, text_color=('#000000','#FFFFFF'))
        self.y_max_entry.grid(row=3, column=0, padx=10, pady=10)

        title = 'Title of the plot:'
        self.title_entry = CTkEntry(master= tab_1, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=title, width=300, text_color=('#000000','#FFFFFF'))
        self.title_entry.grid(row=4, column=0, padx=10, pady=10)

        title_lin = 'Title of the plot:'
        self.title_lin_entry = CTkEntry(master= tab_2, fg_color=('#FFFFFF','#2A2B40'), border_color='#4158D0', placeholder_text_color=('#575757','#E0E0E0'), font=('Calibri',14), placeholder_text=title_lin, width=200, text_color=('#000000','#FFFFFF'))
        self.title_lin_entry.grid(row=0, column=0, padx=10, pady=10)

        color = 'Color of the plot:'
        color_choices = ['blue','green','brown','violet','pink','magenta','red','orange', 'black']
        self.color = CTkLabel(master= tab_2, text=color, text_color=('#000000','#FFFFFF'))
        self.color.grid(row=1, column=0, padx=10, pady=10)
        self.color_entry = CTkComboBox(master= tab_2,values=color_choices, fg_color=('#FFFFFF','#2A2B40'), button_color='#4158D0', button_hover_color='#C850C0', border_color='#4158D0')
        self.color_entry.set(color_choices[0])
        self.color_entry.grid(row=1, column=1, padx=10, pady=10)


        marker = 'Type of markers:'
        marker_choices = ['circle','point','star','triangle_up','triangle_down','plus','x-point']
        self.marker = CTkLabel(master= tab_2, text=marker, text_color=('#000000','#FFFFFF'))
        self.marker.grid(row=2, column=0, padx=10, pady=10)
        self.marker_entry = CTkComboBox(master= tab_2,values=marker_choices, fg_color=('#FFFFFF','#2A2B40'), button_color='#4158D0', button_hover_color='#C850C0', border_color='#4158D0')
        self.marker_entry.set(marker_choices[0])
        self.marker_entry.grid(row=2, column=1, padx=10, pady=10)

        col_rej = 'Color of rejected samples:'
        color_choices_rej = ['blue','green','brown','violet','pink','magenta','red','orange', 'black']
        self.color_rej = CTkLabel(master= tab_2, text=col_rej, text_color=('#000000','#FFFFFF'))
        self.color_rej.grid(row=3, column=0, padx=10, pady=10)
        self.col_rej_entry = CTkComboBox(master= tab_2,values=color_choices, fg_color=('#FFFFFF','#2A2B40'), button_color='#4158D0', button_hover_color='#C850C0', border_color='#4158D0')
        self.col_rej_entry.set(color_choices_rej[6])
        self.col_rej_entry.grid(row=3, column=1, padx=10, pady=10)

    def processing_data_draw_spectra(self):    
        self.result = {
                'x_min' : self.x_min_entry.get(),
                'x_max' : self.x_max_entry.get(),
                'y_min' : self.y_min_entry.get(),
                'y_max' : self.y_max_entry.get(),
                'title' : self.title_entry.get(),
            }

        if self.result['x_min'].isalnum() and 200 <= float(self.result['x_min']) <= 700: self.result['x_min'] = float(self.result['x_min'])
        if self.result['x_max'].isalnum() and 200 <= float(self.result['x_min']) <= 700: self.result['x_max'] = float(self.result['x_max'])
        if self.result['y_min'].isalnum() and float(self.result['y_min']) > 0: self.result['y_min'] = float(self.result['y_min'])
        if self.result['y_max'].isalnum() and float(self.result['y_max']) > 0: self.result['y_max'] = float(self.result['y_max'])

        if self.result['x_min']=='' or str(self.result['x_min']).isalpha(): self.result['x_min'] = 200
        if self.result['x_max']=='' or str(self.result['x_max']).isalpha(): self.result['x_max'] = 700
        if self.result['y_min']=='' or str(self.result['y_min']).isalpha(): self.result['y_min'] = 0
        if self.result['y_max']=='' or str(self.result['y_max']).isalpha(): self.result['y_max'] = 3
        return self.result
    
    def processing_data_linear_plot(self):    
        marker_choices = {'circle':'o','point':'.','star':'*','triangle_up':'^','triangle_down':'v','plus':'+','x-point':'x'}
        self.result = {
                'title_lin' : self.title_lin_entry.get(),
                'color' : self.color_entry.get(),
                'marker' : marker_choices[self.marker_entry.get()],
                'col_rej' : self.col_rej_entry.get(),
            }
        return self.result

class Program(CTk):
    def __init__(self):
        super().__init__()
        
        self.title("UV-Vis SPECTRA")
        self.geometry('900x800')
        set_appearance_mode('light')
        self.configure(fg_color=('#E7E9F1','#18122B')) 
        self.protocol('WM_DELETE_WINDOW', self._exitprogram)
        self.iconbitmap(default = os.path.join(os.path.dirname(__file__),str('icon.ico')))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.functions_frame = FunctionsFrame(self, corner_radius = 20, border_width = 2, border_color =('#CDCFD6', '#2A2B40'), 
                                              fg_color = ('white','#1A1E32'))
        self.functions_frame.pack(side = tk.LEFT, expand = False, fill = tk.BOTH, padx = 30, pady = 10, anchor = 'w')

        
        self.image_frame = ImageFrame(self, corner_radius = 20, border_width = 2, border_color =('#CDCFD6', '#2A2B40'), 
                                              fg_color = ('white','#1A1E32'))
        self.image_frame.pack(side = tk.LEFT, expand = True, fill = tk.BOTH, padx = 10, pady = 10, anchor = 'w')


    
    
    def _exitprogram(self):
        if messagebox.askokcancel('Close', 'Are you sure...?'):
            window.destroy()
            exit()


if __name__ == '__main__':
    window = Program()
    window.mainloop()