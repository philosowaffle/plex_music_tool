Plex Music Tool
============

A tool for enhancing the Plex Music Database.

## Features
- Get track play count information from LastFm and initialize the Plex music database with your play count information.

## Dependencies
- python 2.7
- Django

## Clear Database
```
python manage.py flush
```

## Build Database
```
python manage.py makemigrations
python manage.py migrate
```
## Run Server
```
python manage.py runserver
```