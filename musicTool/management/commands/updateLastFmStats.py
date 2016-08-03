from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

import logging
import requests
import collections
import time

logger = logging.getLogger(__name__)

lastfm_api_url = 'https://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={}&from={}&to={}&api_key={}&format=json'
epoch = datetime.utcfromtimestamp(0)

query_builder = "UPDATE metadata_item_settings SET view_count={} WHERE guid IN (SELECT guid FROM metadata_items WHERE metadata_type = 10 AND UPPER(\'title\') = UPPER({}); "

def flatten(d, parent_key=''):
    """From http://stackoverflow.com/a/6027615/254187. Modified to strip # symbols from dict keys."""
    items = []
    for k, v in d.items():
        new_key = parent_key + '_' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key).items())
        else:
            new_key = new_key.replace('#', '')  # Strip pound symbols from column names
            items.append((new_key, v))
    return dict(items)

def process_track(track):
    """Removes `image` keys from track data. Replaces empty strings for values with None."""
    if 'image' in track:
        del track['image']
    flattened = flatten(track)
    for key, val in flattened.iteritems():
        if val == '':
            flattened[key] = None
    return flattened

class Command(BaseCommand):
    help = 'Gets play count and last played data from LastFm and updates Plex music stats.'

    def add_arguments(self, parser):
        parser.add_argument('time_frame')
        parser.add_argument('username')
        parser.add_argument('api_key')
        parser.add_argument('db_path')

    def handle(self, *args, **options):
        time_frame = options['time_frame']
        username = options['username']
        api_key = options['api_key']
        db_path = options['db_path']

        logger.debug('Time Frame: {} Username: {} API Key: {}'.format(time_frame, username, api_key))

        if time_frame is None:
            raise CommandError('Must provide a time frame.')
        if username is None:
            raise CommandError('Must provide LastFm username.')
        if api_key is None:
            raise CommandError('Must provide API Key.')
        if db_path is None:
            raise CommandError('Must provide Plex Database path.')

        to_time = time.time()
        from_time = None;
        logger.debug(time_frame)
        if time_frame == 'day':
            from_time = datetime.now() - timedelta(days=1)
            from_time = (from_time - epoch).total_seconds()
            logger.debug(from_time)
            logger.debug(to_time)

        lastfm_data = requests.get(lastfm_api_url.format(username, from_time, to_time, api_key)).json()
        lastfm_data = lastfm_data['weeklytrackchart']['track']

        query = ""

        for item in enumerate(lastfm_data):
            try:

                song = item[1]
                song_name = song['name']
                song_name = song_name.replace('\"','\"\"')
                song_artist = song['artist']['#text']
                song_playcount = song['playcount']

                query = query + query_builder.format(song_playcount, song_name)
            except:
                # TODO: Deal with songs that send unicode exception
                logger.error("Failed to update data for: {}".format(item))
                pass
        logger.debug(query)



