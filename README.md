
<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![LinkedIn][LinkedIn]][LinkedIn-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/agatabiesiekierska/UV-VIS-spectra">
    <img src="icon.png"" alt="Logo" width="300" height="300">
  </a>

<h3 align="center">UV-VIS Spectra</h3>

  <p align="center">
    This project is dedicated to users of the HACH DR6000 spectrophotometer. It allows to create multiple spectra and linear regression for specific wavelength based on data downloaded from the device.
    <br />
    <a href="https://github.com/agatabiesiekierska/UV-VIS-spectra"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/agatabiesiekierska/UV-VIS-spectra/issues">Report Bug</a>
    ·
    <a href="https://github.com/agatabiesiekierska/UV-VIS-spectra">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation and Starting the program</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
# About The Project

[![Main_Window][Main_Window]](https://github.com/agatabiesiekierska/UV-VIS-spectra)

<H4>The illustration depicts the program interface, where users have the capability to upload a data folder. Upon filling in the necessary fields, they can produce a spectrum graph covering the entire measurement range or generate a graph illustrating absorbance versus concentration at a designated wavelength. Furthermore, the program provides the option to consolidate data from the device into a singular Excel file.</H4>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



## Built With

[![Python][Python]][Python-url]
[![Tkinter][Tkinter]][Tkinter-url]
[![Matplotlib][Matplotlib]][Matplotlib-url]
[![Pandas][Pandas]][Pandas-url]
[![Scipy][Scipy]][Scipy-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

If you want to use this script, follow these instructions:

### Download program


### Prerequisites

To use properly this program you need Python on your computer and PyQt5.
* Python    
[![Python][Python]][Python-url]

* PyQt5
  ```sh
  pip install PyQt5
  ```

### Installation and Starting the program

1. Clone the repo (or just download folder with all files)
   ```sh
   git clone https://github.com/agatabiesiekierska/Statistical_tests.git
   ```
2. Launch Windows PowerShell and move to the directory with files
   ```sh
   cd C:\Users\Your_UserName\Statistical_tests
   ```
4. Launch main.py file with Python
   ```sh
   python main.py
   ```
5. **(Alternatively)** Find main.py file and open with Python

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This paragraph will explain how to use this script

1. If you want to perform any test you need to type a location of your file with dataset (must have less than **11** measurements - it's related to critical value and consist only your measurments with dots or commas as decimal separator. File cannot have special signs or blank spaces - **otherwise the Error will appear**),

2. Type significance - confidence level - there are 3 values possible: **0.90, 0.95, 0.99**,

3. Type **Real Value** - a parameter needed only in t-Student test

4. Type path to export results for example: <br/> 
```
"C:\Users\Your_Username\Documents\results"
```
In the picture below you can see correctly entered values: <br/><br/>
[![Data Screenshot][app_window_2]]()

If everythig worked successfully the checkbox will appear: <br/><br/>
[![Checkbox Screenshot][results_1]]()

But if something went wrong, the user will get notification: <br/><br/>
[![ERROR][results_2]]()

5. The file with results will appear in given folder

In the picture below you can see the example output file in .txt format: <br/><br/>
[![Output Screenshot][output]]()


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this program better, please fork the repo and create a pull request. 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

![Agata Biesiekierska](https://img.shields.io/badge/Agata_Biesiekierska-blue?style=for-the-badge) [![LinkedIn][LinkedIn]][LinkedIn-url] ![Gmail](https://img.shields.io/badge/ag.biesiekierska@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white) 

Project Link: [https://github.com/agatabiesiekierska/UV-VIS-spectra](https://github.com/agatabiesiekierska/UV-VIS-spectra)

<p align="right">(<a href="#readme-top">back to top</a>)</p>






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/agatabiesiekierska/UV-VIS-spectra.svg?style=for-the-badge
[contributors-url]: https://github.com/agatabiesiekierska/UV-VIS-spectra/graphs/contributors

[issues-shield]: https://img.shields.io/github/issues/agatabiesiekierska/UV-VIS-spectra.svg?style=for-the-badge
[issues-url]: https://github.com/agatabiesiekierska/UV-VIS-spectra/issues

[LinkedIn]: https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white
[LinkedIn-url]: https://www.linkedin.com/in/agata-biesiekierska-6293a4271

[Main_Window]: Source_code\images_for_readme\main_window.png
[app_window_2]: images/app_window_2.png
[results_1]: images/results_1.png
[results_2]: images/result_2.png
[output]: images/output.png

[Python]: https://img.shields.io/badge/python_3.11-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/downloads

[Tkinter]: https://img.shields.io/badge/Tkinter-red?style=for-the-badge&logo=python&logoColor=white
[Tkinter-url]: https://docs.python.org/3/library/tkinter.html#module-tkinter

[Pandas]: https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org

[Matplotlib]: https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black
[Matplotlib-url]: https://matplotlib.org

[Scipy]: https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white
[Scipy-url]: https://scipy.org

[Pyinstaller]: https://img.shields.io/badge/SciPy-%230C55A5.svg?style=for-the-badge&logo=scipy&logoColor=%white
[Pyinstaller-url]: https://pyinstaller.org/en/stable/


