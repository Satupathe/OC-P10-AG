# OC-P10-AG

This readme focus on how to set up your computer, launch the local server and use the different API's features with the following steps:
-download elements on your computer
-set your computer on the right configuration
-launch your local server
-use endpoints on Postman

### This program respect PEP8 writing conventions

Be careful: - In your powershell windows, using your right click will automatically paste
	    - In your terminal application for mac or linux use the right click and paste

## PYTHON INSTALLATION:
To run this code you need Python 3.8 version or further 
Download python's executable file on the following website: https://www.python.org/downloads/
Lauch the installation without any modification.

## CREATION OF THE WORKING REPOSITORY:
To run this code and find the informations you seek for, you need to create a working folder.
With your explorer go at the place you choose to work, create a new working folder. 

## SET YOUR SYSTEM TO THE RIGHT PLACE (your working folder pathway):
You now need to open your terminal:
- windows: use Windows Powershell(admin). to find it use windows + x as keyboard shortcut 
- mac: use terminal. to find it open your Utilities folder in applications
- linux: use terminal. to find it type terminal in your applications's research bar

In the new window, you have to put your working folder's path
For that go back to your windows explorer, go in your working folder.
now you're in, copy the pathway of your folder found in the adress bar (C:\Users\...\.... for windows)

In the terminal type ```cd ..``` several time. you need to be at the root of your computer (C: for Windows, /Home on Mac)
Next type ```cd 'yourfolderpathwaythatyoujustcopied'``` (keep the small quote marksand let a space after cd) and ENTER

## CREATE A SPECIAL WORKING ENVIRONMENT:
With Python, you have to create a special working environment to install specifics modules for each project.
In the terminal using the following command will set a new environment 'env':
```python -m venv env``` and ENTER

You now need to activate it, for that:
-On Windows: ```source env/Scripts/activate``` or ```env/Scripts/activate.ps1``` and ENTER
-On Mac and Linux: ```source env/bin/activate``` and ENTER

if you have any issue to activate your environment:
-go to the env folder and search for the folder name which contain the "activate" file 
-replace "Scripts" by this name

With this step your working environment is now running

## DOWNLOAD REQUESTED FILES AND MODULES:
Go to the following repository: https://github.com/Satupathe/OC-P10-AG
-find the green button
-clic on the arrow
-choose download ZIP
-download the zip file
-extract its content and put it in your working folder

now use this command on the terminal:
```pip install -r requirements.txt```

This step will install necessary modules to execute the code. 
Let it work because it can take few minutes depending on your internet connection

## LAUNCH THE SERVER:
In your terminal type ```cd 'SoftDesk/OC-P10-AG/SoftProjects```
Then type "python manage.py runserver and after a few seconds you'll see the following messages:

```
System check identified no issues (0 silenced).
November 08, 2021 - 11:39:14 (with your actual date)
Django version 3.2.7, using settings 'LITReview.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK
```

You have now activated your local server.

## POSTMAN ENDPOINTS:
Go to the following url: https://documenter.getpostman.com/view/15685214/UVC5E7Ct 
You can now launch Postman and start using endpoints following documentation


Thank you for reading this README and using this API




