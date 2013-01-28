#!/bin/sh



## Clean files .pyc
find . -type f -iname *.pyc -exec rm  -f {} \;

## Clean logs files
rm -f logs/*
rm -f applications/dashboard/errors/*
rm -f applications/dashboard/sessions/*


## Start webserver https
python web2py.py -c ssl/server.crt -k ssl/server.key --ip=0.0.0.0 --port=8010 --nogui --password=smb4manager -D 100
