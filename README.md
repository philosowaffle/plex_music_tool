Plex Music Tool
============

A tool for enhancing the Plex Music Database.

## Features
- Get track play count information from LastFm and initialize the Plex music database with your play count information.

## Dependencies
- python 2.7

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

## Windows Install steps

** Warning: Make a backup of your Plex database before performing any actions with the Plex Music Tool **

1. Python 2.7
2. Pip https://pip.pypa.io/en/latest/installing/
3. Open a command prompt in the project directory
4. `virtualenv venv`
5. `venv\Scripts\activate` (run deactivate to end)
3. pip install -r requirements.txt
4. py manage.py makemigrations
5. py manage.py migrate
6. py manage.py runserver
7. Go to http://localhost/8000/musicTool


## Usage

### Settings
* Plex Database Path: The path to your Plex database file.  Normally this is found in `C:\Users\Username\AppData\Local\Plex Media Server\Plug-in Support\Databases\com.plexapp.plugins.library.db`.  Provide the full path including the file name.  It is recommended you make a backup copy of the database file before performing any action.
* Plex Username:  Your Plex username, note that if you are the owner of the library then your username will be 'Administrator'.
* LastFm Username:  Your LastFm username.
* LastFm Api Key:  Your LastFm API key.  You can get one here: http://www.last.fm/api
* Update Settings:  Updates your settings in for the Plex Music Tool.  Currently only supports one user at a time, changing the user name will overwrite the existing users settings.

### Sync LastFm Scrobbles
This will query LastFm for your entire track play count history.  It will then kick off a background process that will update your Plex Database metadata for any matching tracks.  This process may take some time and will temporarily lock the database so ensure you have no active users and do not click the button multiple times as this will just trigger a new job.  The sync will overwrite any existing play count information in the database.
