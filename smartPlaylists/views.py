from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse

from .models import Settings, Playlist, Song, DBPathForm, PlaylistForm, QueryField, QueryOperator, LastFmForm

from datetime import datetime

# Create your views here.
def index(request):
    plex_db_location = list(Settings.objects.filter()[:1])
    if plex_db_location:
        plex_db_location = plex_db_location[0].plex_db_path

    playlists = Playlist.objects.all()
    songs = Song.objects.all()
    query_fields = QueryField.objects.all()
    query_operators = QueryOperator.objects.all()

    # FORMS
    db_path_form = DBPathForm(initial={'db_path':plex_db_location})
    playlist_form = PlaylistForm(query_fields=query_fields, query_operators=query_operators)
    lastfm_form = LastFmForm()

    context = {
        'plex_db_location': plex_db_location,
        'playlists': playlists,
        'songs': songs,
        'db_path_form': db_path_form,
        'playlist_form': playlist_form,
        'query_fields': query_fields,
        'query_operators': query_operators,
        'lastfm_form': lastfm_form
    }

    return render(request, 'smartPlaylists/index.html', context)

def setDatabasePath(request):
    # create a form instance and populate it with data from the request:
    form = DBPathForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        settings = list(Settings.objects.filter()[:1])

        db_path = form.cleaned_data['db_path']

        if(settings):
            settings[0].set_db_path(db_path)
            settings[0].save()
        else:
            settings = Settings()
            settings.set_db_path(db_path)
            settings.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('smartPlaylists:index'))

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

    return HttpResponseRedirect(reverse('smartPlaylists:index'))

def updateLastFmData():
    form = LastFmForm(request.POST)

    if form.is_valid():
        syncAllData = form.cleaned_data['syncAllData']

    return HttpResponseRedirect(reverse('smartPlaylists:index'))
