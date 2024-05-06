#!/bin/bash


## Requirements
## gcc, make, Python 3, python3-dev, python3-pip, python3-virtualenv, python3-pyOpenSSL

## Instalation
## Create a virtualenv, and activate this: 

virtualenv flask 
flask/bin/pip install -r requirements.txt


chmod 400 ssl/*

echo 'Production ...'
echo 'flask/bin/python runserver.py --flask'

echo 'Production and Debug ...'
echo 'flask/bin/python runserver.py --flask --debug'

