#!/bin/bash

rm db.sqlite3
rm -rf ./cookprojectapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations cookprojectapi
python3 manage.py migrate cookprojectapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata customer
python3 manage.py loaddata recipe
python3 manage.py loaddata review
python3 manage.py loaddata favorite
python3 manage.py loaddata category
python3 manage.py loaddata recipe_category
python3 manage.py loaddata recipe_image

