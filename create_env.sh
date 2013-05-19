#!/bin/bash


## Requirements
## gcc, make, Python 2.5+, python-pip, virtualenv

## Instalation
## Create a virtualenv, and activate this: 

virtualenv env 
source env/bin/activate
pip install -r requirements.txt

deactivate

chmod 400 ssl/*

## Prod
python run.py --prod

## For Debug
python run.py --prod --debug

