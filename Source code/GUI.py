import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import subprocess
from main import *


class Options_Linear_Dialog(simpledialog.Dialog):
    def body(self, master):

        title_lin = 'Title of the plot:'
        self.title_lin = ttk.Label(master, text=title_lin).pack(pady=10)
        self.title_lin_entry = ttk.Entry(master)
        self.title_lin_entry.pack(pady=10)

        color = 'Color of the plot:'
        self.color = ttk.Label(master, text=color).pack(pady=10)
        self.color_entry = ttk.Entry(master)
        self.color_entry.pack(pady=10)

        marker = 'Type of markers:'
        marker_choices = ['circle','point','star','triangle_up','triangle_down','plus','x-point']
        self.marker = ttk.Label(master, text=marker).pack(pady=10)
        self.marker_entry = ttk.Combobox(master,values=marker_choices)
        self.marker_entry.pack(pady=10)

        col_rej = 'Color of rejected samples:'
        self.col_rej = ttk.Label(master, text=col_rej).pack(pady=10)
        self.col_rej_entry = ttk.Entry(master)
        self.col_rej_entry.pack(pady=10)      

        return self.title_lin
    
    def apply(self):
        self.result = {
            'title_lin' : self.title_lin_entry.get(),
            'color' : self.color_entry.get(),
            'marker' : self.marker_entry.get(),
            'col_rej' : self.col_rej_entry.get(),
        }

class Options_Spectra_Dialog(simpledialog.Dialog):
    def body(self, master):

        x_min = 'Minimum value of x [nm]:'
        self.x_min = ttk.Label(master, text=x_min).pack(pady=10)
        self.x_min_entry = ttk.Entry(master)
        self.x_min_entry.pack(pady=10)

        x_max = 'Maksimum value of x [nm]:'
        self.x_max = ttk.Label(master, text=x_max).pack(pady=10)
        self.x_max_entry = ttk.Entry(master)
        self.x_max_entry.pack(pady=10)

        y_min = 'Minimum value of y [nm]:'
        self.y_min = ttk.Label(master, text=y_min).pack(pady=10)
        self.y_min_entry = ttk.Entry(master)
        self.y_min_entry.pack(pady=10)

        y_max = 'Maksimum value of y [nm]:'
        self.y_max = ttk.Label(master, text=y_max).pack(pady=10)
        self.y_max_entry = ttk.Entry(master)
        self.y_max_entry.pack(pady=10)
        
        title = 'Title of the plot:'
        self.title = ttk.Label(master, text=title).pack(pady=10)
        self.title_entry = ttk.Entry(master)
        self.title_entry.pack(pady=10)        

        return self.title
    
    def apply(self):
        self.result = {
            'x_min' : self.x_min_entry.get(),
            'x_max' : self.x_max_entry.get(),
            'y_min' : self.y_min_entry.get(),
            'y_max' : self.y_max_entry.get(),
            'title' : self.title_entry.get(),
        }

class Program:
    def __init__(self, window):
        self.window = window
        self.window.title("UV-Vis SPECTRA")
        style = ttk.Style()
        self.window.protocol('WM_DELETE_WINDOW', self._exitprogram)
        self.window.iconbitmap(default = os.path.join(os.path.dirname(__file__),str('icon.ico')))       
       
        # Deafult parameters for "Draw Spectra" Function
        self.x_min = 200
        self.x_max = 700
        self.y_min = 0
        self.y_max = 3
        self.title_1 = ''

        # Deafult parameters for "Linear Plot" Function
        self.title_2 = ''
        self.color = 'blue'
        self.marker = 'o'
        self.col_rej = 'red'


        # Allow the columns and rows to expand
        for i in range(2):
            self.window.grid_columnconfigure(i, weight=1)
            self.window.grid_rowconfigure(i, weight=1)

        # Create two frames
        self.frame_spectra_options = ttk.Frame(window)
        self.frame_spectra_options.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.frame_images = ttk.Frame(window)
        self.frame_images.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        # Create an area for displaying images
        self.result_label = ttk.Label(self.frame_images, text="Result Image")
        self.result_label.grid(row=1, column=1, columnspan=2, pady=10, sticky='nsew')

        # Updated labels and checkbox text
        label1_text = 'Pass directory of your folder with data:'
        label2_text = 'Pass concentrations of the samples in increasing order [ppm]:'
        label3_text = 'Concentrations of the samples:'
        label4_text = 'Pass wavelength to plot:'
        label5_text = 'Rejected samples (pass labels):'
        checkbox_1_text = 'Show rejected samples in the plot'
        checkbox_2_text = 'Make linear regression'

        # Label for "UV-Vis SPECTRA" above all elements
        uv_vis_label = ttk.Label(window, text="UV-Vis SPECTRA", font=('Helvetica', 16, 'bold'))
        uv_vis_label.grid(row=0, column=0, columnspan=2, pady=10, sticky='')
        uv_vis_label.configure(anchor='center')

        # Label for generated image - above the plot
        generated_image = ttk.Label(window, text="Generated Image", font=('Helvetica', 16, 'bold'))
        generated_image.grid(row=0, column=1, columnspan=2, pady=10, sticky='')
        generated_image.configure(anchor='center')

        # Create menu bar
        menu_bar = tk.Menu(window)
        window.config(menu=menu_bar)

        # Create File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Data", menu=file_menu)
        file_menu.add_command(label="Import Folder", command=self._import_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Open Merged Files", command=self._open_merged_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._exitprogram)

        # Create Options menu
        options_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Change Draw Spectra Options", command=self._open_options_window)
        options_menu.add_command(label="Change Draw Linear Plot Options", command=self.open_linear_options_window)
        
        # Create Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "UV-Vis SPECTRA App\nVersion 1.0"))

        # Labels and widgets in frame_spectra_options - functions of the programm
        
        make_spectra_label = ttk.Label(self.frame_spectra_options, text="Make UV-Vis spectra", font=('Helvetica', 14, 'bold'))
        make_spectra_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="nsew")
        make_spectra_label.configure(anchor='center')

        # Passing directory of the folder with measurments
        label1 = ttk.Label(self.frame_spectra_options, text=label1_text)
        label1.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.entry1 = ttk.Entry(self.frame_spectra_options)
        self.entry1.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # import button
        import_button = ttk.Button(self.frame_spectra_options, text="Import Folder", command=self._import_folder)
        import_button.grid(row=3, column=2, padx=10, pady=5, sticky="e")

        # Labels of the files - concentrations of the samples or names
        label2 = ttk.Label(self.frame_spectra_options, text=label2_text)
        label2.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.entry2 = ttk.Entry(self.frame_spectra_options)
        self.entry2.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # "Merge All Files" button
        merge_button = ttk.Button(self.frame_spectra_options, text="Merge All Files", command=self._merge_all_files)
        merge_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        # Create UV-Vis spectra button
        draw_spectra_button = ttk.Button(self.frame_spectra_options, text="Draw Spectra", command=self.draw_spectra)
        draw_spectra_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Second function of the programm - makes graph from selected wavelength
        # Label for title
        draw_curve_label = ttk.Label(self.frame_spectra_options, text="Draw curve for specific wavelength", font=('Helvetica', 14, 'bold'))
        draw_curve_label.grid(row=7, column=0, columnspan=2, pady=5, sticky="nsew")
        draw_curve_label.configure(anchor='center')

        # Label for labels of the samples
        label3 = ttk.Label(self.frame_spectra_options, text=label3_text)
        label3.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.entry3 = ttk.Entry(self.frame_spectra_options)
        self.entry3.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Label for wavelength to plot
        label4 = ttk.Label(self.frame_spectra_options, text=label4_text)
        label4.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.entry4 = ttk.Entry(self.frame_spectra_options)
        self.entry4.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        # Labels for the rejected samples
        label5 = ttk.Label(self.frame_spectra_options, text=label5_text)
        label5.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        self.entry5 = ttk.Entry(self.frame_spectra_options)
        self.entry5.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        # Checkbox if user wants to show rejected samples in the plot
        self.checkbox_var_1 = tk.BooleanVar()
        checkbox = ttk.Checkbutton(self.frame_spectra_options, text=checkbox_1_text, variable=self.checkbox_var_1)
        checkbox.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Checkbox if user wants to make linear regression to the plot
        self.checkbox_var_2 = tk.BooleanVar()
        checkbox = ttk.Checkbutton(self.frame_spectra_options, text=checkbox_2_text, variable=self.checkbox_var_2)
        checkbox.grid(row=12, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Create button for drawing linear plot 
        draw_linear_plot_button = ttk.Button(self.frame_spectra_options, text="Draw Linear Plot", command=self.draw_linear_plot)
        draw_linear_plot_button.grid(row=13, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Create button for opening image directory
        open_image_directory_button = ttk.Button(self.frame_spectra_options, text="Open Image Directory", command=self._open_image_directory)
        open_image_directory_button.grid(row=14, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Create a Reset button
        reset = ttk.Button(window, text="Reset", command=self.reset_options)
        reset.grid(row=15, column=1, columnspan=2, padx=10, pady=5, sticky="ew")


    def _open_options_window(self):
        dialog = Options_Spectra_Dialog(self.window)
        result = dialog.result

        if result:
            if result['x_min'].isalnum() and 200 <= result['x_min'] <= 700: self.x_min = float(result['x_min'])
            if result['x_max'].isalnum() and 200 <= result['x_min'] <= 700: self.x_max = float(result['x_max'])
            if result['y_min'].isalnum() and result['y_min'] > 0: self.y_min = float(result['y_min'])
            if result['y_max'].isalnum() and result['y_max'] > 0: self.y_max = float(result['y_max'])
            self.title_1 = result['title']

    def open_linear_options_window(self):
        dialog = Options_Linear_Dialog(self.window)
        result = dialog.result
        marker_choices = {'circle':'o','point':'.','star':'*','triangle_up':'^','triangle_down':'v','plus':'+','x-point':'x'}
        if result:
            self.title_2 = result['title_lin']
            self.color = result['color']
            self.marker = marker_choices[result['marker']]
            self.col_rej = result['col_rej']
       
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

    def _open_image_directory(self):
        image_directory = os.path.join(os.path.dirname(__file__),str('graphs'))
        subprocess.Popen(['explorer', image_directory], shell=True)

    def draw_spectra(self):
        try:    
            folder_path = self.entry1.get()
            concentrations = self.entry2.get()
            self.directory = Multiple_files(folder_path)
            path = self.directory.draw_multiple_plot(x_min = self.x_min, x_max = self.x_max, y_min = self.y_min, y_max = self.y_max,title=self.title_1, labels=concentrations)
            self.show_image(path)

        except ValueError as e:
            messagebox.showerror('Error', f'Error with input value: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Error with drawing plot function: {str(e)}')


    def draw_linear_plot(self):
        try:
            folder_path = self.entry1.get()
            labels_of_samples = self.entry3.get()
            wavelength = int(self.entry4.get())
            show = self.checkbox_var_1.get()
            regression = self.checkbox_var_2.get()
            rejected_samples = self.entry5.get()
            self.directory = Multiple_files(folder_path)
            path = self.directory.scatter_plot(wavelength, labels_of_samples, self.title_2, rejected_samples, show, regression, self.color, self.marker, self.col_rej)
            self.show_image(path)

        except ValueError as e:
            messagebox.showerror('Error', f'Error with input value: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'Error with drawing plot function: {str(e)}')

    
    def show_image(self, image_path):
        try:
            
            image = Image.open(image_path)
            # Resize the image if needed
            image = image.resize((600, 400), Image.ADAPTIVE)
            # Convert the image to Tkinter PhotoImage format
            tk_image = ImageTk.PhotoImage(image)
            # Update the label with the new image
            self.result_label.config(image=tk_image)
            self.result_label.image = tk_image
        
        except Exception as e:
            messagebox.showerror('Error', f'Error loading image: {str(e)}')
    
    def _exitprogram(self):
        if messagebox.askokcancel('Close', 'Are you sure...?'):
            window.destroy()
            exit()

    def reset_options(self):
        
        # reset path to import files
        del self.directory
        
        # reset options for draw spectra
        self.x_min = 200
        self.x_max = 700
        self.y_min = 0
        self.y_max = 3
        self.title_1 = ''

        # reset all widgets 
        for widget in self.frame_spectra_options.winfo_children():
            if isinstance(widget,ttk.Entry):
                widget.delete(0,'end')
            if isinstance(widget,ttk.Checkbutton):
                self.checkbox_var_1.set(False)
                self.checkbox_var_2.set(False)

        # reset options for linear plot
        self.title_2 = ''
        self.color = 'blue'
        self.marker = 'o'
        self.col_rej = 'red'
        
        # reset displaying image
        self.result_label = ttk.Label(self.frame_images, text='Result Image')
        self.result_label.grid(row=1, column=1, columnspan=2, pady=10, sticky='nsew')


if __name__ == '__main__':
    window = ThemedTk(theme='breeze')
    program = Program(window)
    window.mainloop()
