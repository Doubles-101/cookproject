#!/bin/bash

rm db.sqlite3
rm -rf ./cookprojectapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations cookprojectapi
python3 manage.py migrate cookprojectapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

