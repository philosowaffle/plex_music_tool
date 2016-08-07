from django.contrib import messages
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import Settings, Playlist, Song, SettingsForm, PlaylistForm, QueryField, QueryOperator, Async, Task
import async_runner as async_runner

from datetime import datetime

import logging
import signal

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):

    pending_tasks = Task.objects.count()
    async_runner = Async.objects.count()
    logger.debug("Pending Tasks: {} Async Runners: {}".format(pending_tasks, async_runner))

    settings_row = list(Settings.objects.filter()[:1])
    plex_db_location = None
    lastfm_username = None
    lastfm_api_key = None
    plex_username = None
    if settings_row:
        plex_db_location = settings_row[0].plex_db_path
        plex_username = settings_row[0].plex_username
        lastfm_username = settings_row[0].lastfm_username
        lastfm_api_key = settings_row[0].lastfm_api_key
    else:
        logger.warn("No settings found for user.")

    playlists = Playlist.objects.all()
    songs = Song.objects.all()
    query_fields = QueryField.objects.all()
    query_operators = QueryOperator.objects.all()

    # FORMS
    settings_form = SettingsForm(initial={'db_path':plex_db_location, 'plex_username':plex_username, 'lastfm_username':lastfm_username, 'lastfm_api_key':lastfm_api_key})
    playlist_form = PlaylistForm(query_fields=query_fields, query_operators=query_operators)

    context = {
        'plex_db_location': plex_db_location,
        'playlists': playlists,
        'songs': songs,
        'settings_form': settings_form,
        'playlist_form': playlist_form,
        'query_fields': query_fields,
        'query_operators': query_operators
    }

    return render(request, 'musicTool/index.html', context)

def setSettings(request):
    # create a form instance and populate it with data from the request:
    form = SettingsForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        settings = list(Settings.objects.filter()[:1])

        db_path = form.cleaned_data['db_path']
        plex_username = form.cleaned_data['plex_username']
        lastfm_username = form.cleaned_data['lastfm_username']
        lastfm_api_key = form.cleaned_data['lastfm_api_key']

        if(settings):
            settings[0].set_db_path(db_path)
            settings[0].set_plex_username(plex_username)
            settings[0].set_lastfm_username(lastfm_username)
            settings[0].set_lastfm_api_key(lastfm_api_key)
            settings[0].save()
        else:
            settings = Settings()
            settings.set_plex_username(plex_username)
            settings.set_db_path(db_path)
            settings.set_lastfm_username(lastfm_username)
            settings.set_lastfm_api_key(lastfm_api_key)
            settings.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('musicTool:index'))

def addPlaylist(request):
    form = PlaylistForm(request.POST)

    if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        query_field = form.cleaned_data['query_fields']
        query_operator = form.cleaned_data['query_operators']
        value = form.cleaned_data['value']

        playlist = Playlist(name=name, description=description, last_updated=datetime.now())
        playlist.save()

        query_condition = null

        if (query_field == "Play Count" or query_field == "Skip Count"):
            query_condition = QueryCondition(playlist_id=playlist.id, order=0, field_type=query_field, operator_type=query_operator, query_value_int=value)
        elif (query_field == "Last Played" or query_field == "Date Added"):
            query_condition = QueryCondition(playlist_id=playlist.id, order=0, field_type=query_field, operator_type=query_operator, query_value_datetime=value)
        else:
            query_condition = QueryCondition(playlist_id=playlist.id, order=0, field_type=query_field, operator_type=query_operator, query_value_char=value)

        if (query_condition != null):
            query_condition.save()

    return HttpResponseRedirect(reverse('musicTool:index'))

def updateLastFmData(request):

    # https://stackoverflow.com/questions/15959936/how-can-i-run-my-python-script-from-within-a-web-browser-and-process-the-results

    # TODO: get an error here saying signal only works in main thread
    # need to figure out how to make sure we kill this when the program is killed
    # Shutdown async task runner on CTRL-C event
    # signal.signal(signal.SIGINT, async_runner.stop())

    settings_row = list(Settings.objects.filter()[:1])
    plex_db_location = None
    lastfm_username = None
    lastfm_api_key = None
    plex_username = None

    if settings_row:
        plex_db_location = settings_row[0].plex_db_path
        lastfm_username = settings_row[0].lastfm_username
        lastfm_api_key = settings_row[0].lastfm_api_key
        plex_username = settings_row[0].plex_username

        try:
            call_command('updateLastFmStats', lastfm_username, lastfm_api_key, plex_db_location, plex_username)
            messages.add_message(request, messages.INFO, 'LastFm sync in progress.')
        except Exception as e:
            logger.error("Failed to sync LastFm. " + str(e))
            messages.add_message(request, messages.ERROR, str(e))
    else:
        logger.error("No settings found for user.")
        messages.add_message(request, messages.ERROR, 'No settings found for user.')


    return HttpResponseRedirect(reverse('musicTool:index'))
