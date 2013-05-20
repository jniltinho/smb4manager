#!/bin/bash


## Requirements
## gcc, make, Python 2.5+, python-pip, virtualenv

## Instalation
## Create a virtualenv, and activate this: 

virtualenv flask 
flask/bin/pip install -r requirements.txt


chmod 400 ssl/*
chmod +x run.py

## Prod
flask/bin/python run.py --prod

## For Debug
flask/bin/python run.py --prod --debug

