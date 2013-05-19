#!/bin/sh


## Clean files .pyc
find . -type f -iname *.pyc -exec rm  -f {} \;


## Start webserver https
source env/bin/activate
echo 1 > http.log

echo "Log File http.log"
echo "Access https://0.0.0.0:8010" 

gunicorn -w 2 --bind 0.0.0.0:8010 app:app --keyfile=ssl/server.key --certfile=ssl/server.crt --log-file=http.log

