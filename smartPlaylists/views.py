from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse

from .models import Settings, Playlist, Song, DBPathForm

# Create your views here.
def index(request):
    plex_db_location = list(Settings.objects.filter()[:1])
    if plex_db_location:
        plex_db_location = plex_db_location[0].plex_db_path

    playlists = Playlist.objects.all()
    songs = Song.objects.all()
    db_path_form = DBPathForm(initial={'db_path':plex_db_location})

    context = {
        'plex_db_location': plex_db_location,
        'playlists': playlists,
        'songs': songs,
        'db_path_form': db_path_form
    }

    return render(request, 'smartPlaylists/index.html', context)

def setDatabasePath(request):
    # create a form instance and populate it with data from the request:
    form = DBPathForm(request.POST)

    # check whether it's valid:
    if form.is_valid():
        settings = list(Settings.objects.filter()[:1])

        if(settings):
            settings[0].plex_db_path = form.cleaned_data['db_path']
            settings[0].save()
        else:
            settings = Settings(plex_db_path=form.cleaned_data['db_path'])
            settings.save()



    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('smartPlaylists:index'))