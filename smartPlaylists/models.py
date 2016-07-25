from __future__ import unicode_literals

from django import forms
from django.db import models

from django.utils.encoding import python_2_unicode_compatible

import os

# Create your models here.

@python_2_unicode_compatible
class Settings(models.Model):

    # FIELDS
    plex_db_path = models.CharField(max_length=200)

    # METHODS
    def set_db_path(self, new_path):
        self.plex_db_path = new_path

    # HELPERS
    def __str__(self):
        return 'DB Path: {}'.format(self.plex_db_path)

@python_2_unicode_compatible
class Playlist(models.Model):

    # FIELDS
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    query = models.CharField(max_length=350)
    last_updated = models.DateTimeField('last updated')

    # METHODS

    # HELPERS
    def __str__(self):
        return 'Name: {}' \
            '\nQuery: {}' \
            '\nLast Updated: {}'.format(self.name, self.query, self.last_updated)

@python_2_unicode_compatible
class Song(models.Model):

    # FIELDS
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    last_played = models.DateTimeField('last played')
    play_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField('last upadated')

    # METHODS

    # HELPERS
    def __str__(self):
        return 'Title: {} ' \
            '\nArtist: {}'\
            '\nLast Played: {}' \
            '\nPlay Count: {}' \
            '\nLast Updated: {}'.format(self.title, self.artist, self.last_played, self.play_count, self.last_updated)

class DBPathForm(forms.Form):

    # FIELDS
    db_path = forms.CharField(label='Plex Database Path', max_length=500)

    # HELPERS
    def __str__(self):
        return 'Database Path: {}'.format(self.db_path)

class PlaylistForm(forms.Form):

    # FIELDS
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=500)
    play_count_operator = forms.ChoiceField(label='Play Count', choices=[(1, "greater than"), (0, "equal to"), (-1, "less than")])
    play_count = forms.IntegerField(label='', required=True)

    def __str__(self):
        return 'Playlist Name: {}' \
                '\nPlaylist Description: {}' \
                '\nPlay Count Operator: {}' \
                '\nPlay Count: {}'.format(self.name, self.description, self.play_count_operator, self.play_count)