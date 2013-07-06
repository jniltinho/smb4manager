#!/bin/bash


## Requirements
## gcc, make, Python 2.5+, python-devel, python-pip, python-virtualenv, python-pyOpenSSL

## Instalation
## Create a virtualenv, and activate this: 

virtualenv flask 
flask/bin/pip install -r requirements.txt


chmod 400 ssl/*
chmod +x runserver.py

echo 'Production ...'
echo './runserver.py'

echo 'Production and Debug ...'
echo './runserver.py --debug'

