from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
import requests
import collections
import time
import sqlite3

logger = logging.getLogger(__name__)

lastfm_api_url = 'https://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={}&from={}&to={}&api_key={}&format=json'
epoch = datetime.utcfromtimestamp(0)

initialize_query_builder = "UPDATE metadata_item_settings SET view_count={} WHERE guid IN (SELECT guid FROM metadata_items WHERE metadata_type = 10 AND UPPER(title) = UPPER({})); "
update_query_builder = "UPDATE metadata_item_settings SET view_count=view_count + {} WHERE guid IN (SELECT guid FROM metadata_items WHERE metadata_type = 10 AND UPPER(title) = UPPER({})); "
check_changes_query = "SELECT changes();"

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
        from_time = None
        query_builder = ""

        if time_frame == 'day':
            from_time = datetime.now() - timedelta(days=1)
            from_time = (from_time - epoch).total_seconds()
            query_builder = update_query_builder
        elif time_frame  == 'all':
            from_time = datetime.now() - relativedelta(years=20)
            from_time = (from_time - epoch).total_seconds()
            query_builder = initialize_query_builder

        # TODO: add support for other timeframes

        logger.debug("Querying LastFm for user {} over timeframe {} using API Key {} and will insert into database {}".format(username, time_frame, api_key, db_path))
        lastfm_data = requests.get(lastfm_api_url.format(username, from_time, to_time, api_key)).json()
        lastfm_data = lastfm_data['weeklytrackchart']['track']

        query = ""

        for item in enumerate(lastfm_data):
            try:
                song = item[1]
                song_name = song['name']
                song_name = self.clean_song_name(song_name)
                song_artist = song['artist']['#text']
                song_playcount = song['playcount']

                query = query + query_builder.format(song_playcount, song_name)
            except Exception as e:
                # TODO: Deal with songs that send unicode exception
                self.log_error("Failed to update data for: {}".format(item), e)
                pass

        try:
            logger.debug(query)
            conn = sqlite3.connect(db_path)
            conn.executescript(query)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            self.log_error("Failed to query the database.", e)
            pass

    def clean_song_name(self, song_name):
        # Escape "
        song_name = song_name.replace('\"','\"\"')

        # Escape '
        song_name = song_name.replace('\'', "''")

        # Add surrounding quotes
        song_name = "'" + song_name + "'"

        return song_name

    def log_error(self, msg, e):
        logger.error(msg + "\n" \
                     + str(type(e)) + "\n" \
                     + str(e.args) + "\n" \
                     + str(e))



