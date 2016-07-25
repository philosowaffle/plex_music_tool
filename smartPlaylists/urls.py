from django.conf.urls import url

from . import views

app_name = 'smartPlaylists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'setDatabasePath/$', views.setDatabasePath, name='setDatabasePath'),
    url(r'addPlaylist/$', views.addPlaylist, name='addPlaylist')
]