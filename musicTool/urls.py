from django.conf.urls import url

from . import views

app_name = 'musicTool'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'setSettings/$', views.setSettings, name='setSettings'),
    url(r'addPlaylist/$', views.addPlaylist, name='addPlaylist'),
    url(r'updateLastFmData/$', views.updateLastFmData, name='updateLastFmData')
]