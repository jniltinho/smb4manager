#!/bin/bash


## Requirements
## gcc, make, Python 2.5+, python-devel, python-pip, python-virtualenv

## Instalation
## Create a virtualenv, and activate this: 

virtualenv flask 
flask/bin/pip install -r requirements.txt


chmod 400 ssl/*
chmod +x run.py

echo 'Production ...'
echo './run.py'

echo 'Production and Debug ...'
echo './run.py --debug'

