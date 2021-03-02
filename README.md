Copyright (c) 2020 Karlsruhe Institute of Technology - Steinbuch Centre for Computing.

This code is distributed under the GNU LGPLv3 License. Please, see the LICENSE file

# O3as WebApp

O3as WebApp is a part of the service for Ozone (O3) Assessment, http://o3as.data.kit.edu/

Pre-Requisites:
Python installed, together with pip (the following instructions will be given based on pip)
Python virtualenv installed, and added to PATH

Setup Authentication:
win10: 
set-ExecutionPolicy Unrestricted -Scope CurrentUser

build \venv under the \o3webapp\backend folder:
Win10: 
..\backend> python -m venv venv
..\backend> .\venv\Scripts\activate
(venv) ..\backend>

install packages:
Win10:
..\backend> pip install Flask
..\backend> pip install bokeh
..\backend> pip install requests
..\backend> pip install --user numpy scipy pandas
..\backend> pip install pdfkit
..\backend> pip install flask-cors

start-up backend service:
Win10:
..\backend> $env:FLASK_APP="back_end.py"
..\backend> flask run


