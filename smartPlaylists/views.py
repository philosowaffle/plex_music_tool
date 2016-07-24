from django.shortcuts import render, HttpResponse

from .models import Settings, Playlist, Song

# Create your views here.
def index(request):
    plex_db_location = Settings.objects.filter()[:0]
    playlists = Playlist.objects.all()
    songs = Song.objects.all()

    output = 'DB Location: {}' \
                 '\nPlaylists: {}' \
                 '\nSongs: {}'.format(plex_db_location, playlists, songs)
    return HttpResponse(output)