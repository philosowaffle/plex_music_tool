from __future__ import unicode_literals

from django import forms
from django.db import models

from django.utils.encoding import python_2_unicode_compatible

import os

# /Users/philosowaffle/Desktop/com.plexapp.plugins.library.db
# Create your models here.

@python_2_unicode_compatible
class Settings(models.Model):

    # FIELDS
    plex_db_path = models.CharField(max_length=200, null=True)
    lastfm_username = models.CharField(max_length=20, null=True)
    lastfm_api_key = models.CharField(max_length=30, null=True)

    # METHODS
    def set_db_path(self, new_path):
        self.plex_db_path = new_path

    def set_lastfm_username(self, new_lastfm_username):
        self.lastfm_username = new_lastfm_username

    def set_lastfm_api_key(self, new_lastfm_api_key):
        self.lastfm_api_key = new_lastfm_api_key

    # HELPERS
    def __str__(self):
        return 'DB Path: {}' \
                '\nLastFm Username: {}' \
                '\nLastFm Api Key: {}'.format(self.plex_db_path, self.lastfm_username, self.lastfm_api_key)

@python_2_unicode_compatible
class Playlist(models.Model):

    # FIELDS
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    last_updated = models.DateTimeField('last updated')

    # METHODS

    # HELPERS
    def __str__(self):
        return 'Name: {}' \
            '\nLast Updated: {}'.format(self.name, self.last_updated)

@python_2_unicode_compatible
class QueryOperator(models.Model):

    # FIELDS
    operator_type = models.CharField(max_length=20, editable=False)

    # HELPERS
    def __str__(self):
        return 'Operator Type: {}' \
                '\nId: {}' .format(self.operator_type, self.id)

@python_2_unicode_compatible
class QueryCombiner(models.Model):

    # FIELDS
    combiner_type = models.CharField(max_length=20, editable=False)

    # HELPERS
    def __str__(self):
        return 'Combiner Type: {}' \
                '\nId: {}' .format(self.combiner_type, self.id)

@python_2_unicode_compatible
class QueryField(models.Model):

    # FIELDS
    field_type = models.CharField(max_length=20, editable=False)

    # HELPERS
    def __str__(self):
        return 'Field Type: {}'  \
                '\nId: {}'.format(self.field_type, self.id)

@python_2_unicode_compatible
class QueryCondition(models.Model):

    # FIELDS
    playlist_id = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    order = models.IntegerField()
    combiner_type = models.ForeignKey(QueryCombiner, on_delete=models.CASCADE)
    operator_type = models.ForeignKey(QueryOperator, on_delete=models.CASCADE)
    field_type = models.ForeignKey(QueryField, on_delete=models.CASCADE)
    field_value_char = models.CharField(max_length=20)
    field_value_int = models.IntegerField()
    field_value_datetime = models.DateTimeField()

    # HELPERS
    def __str__(self):
        return 'Playlist Id: {}' \
                '\nOrder: {}' \
                '\nCombiner Type: {}' \
                '\nOperator Type: {}' \
                '\nField Type: {}' \
                '\nField Value Char: {}' \
                '\nFieldValue Int: {}' \
                '\nField Value Datetime: {}'.format(self.playlist_id, self.order, self.combiner_type, self.operator_type, self.field_type, self.field_value_char, self.field_value_int, self.field_value_datetime)

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

class SettingsForm(forms.Form):

    # FIELDS
    db_path = forms.CharField(label='Plex Database Path', max_length=500)
    lastfm_username = forms.CharField(label='LastFm Username', max_length=20)
    lastfm_api_key = forms.CharField(label='LastFm Api Key', max_length=50)

    # HELPERS
    def __str__(self):
        return 'Database Path: {}' \
                '\nLastFm Username: {}' \
                '\nLastFm Api Key: {}'.format(self.db_path, self.lastfm_username, self.lastfm_api_key)

class PlaylistForm(forms.Form):

    # FIELDS
    name = forms.CharField(label='Name', max_length=30)
    description = forms.CharField(label='Description', max_length=500)

    # HELPERS
    def __init__(self,*args,**kwargs):
        query_fields = kwargs.pop("query_fields", [])
        query_operators = kwargs.pop("query_operators", [])
        super(PlaylistForm, self).__init__(*args,**kwargs)
        self.fields['query_fields'] = forms.ChoiceField(label='Field', choices=[(x.id, x.field_type) for x in query_fields])
        self.fields['query_operators'] = forms.ChoiceField(label='', choices=[(x.id, x.operator_type) for x in query_operators])
        self.fields['value'] = forms.CharField(label='', max_length=20)

    def __str__(self):
        return 'Name: {}' \
                '\nDescription: {}' \
                '\nValue: {}' \
                '\nQuery Fields: {}' \
                '\nQuery Operators: {}'.format(self.name, self.description, self.value, self.query_fields, self.query_operators)

class LastFmForm(forms.Form):

    # FIELDS
    sync_time_frame = forms.ChoiceField(label='', choices=[('day', 'Day'), ('week', 'Week'), ('month', 'Month'), ('all', 'All Data')])

    # HELPERS
    def __str__(self):
        return 'Sync Time Frame: {}'.format(self.sync_time_frame)