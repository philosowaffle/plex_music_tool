from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta

import logging
import requests
import collections
import time

logger = logging.getLogger(__name__)

lastfm_api_url = 'https://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={}&from={}&to={}&api_key={}&format=json'
epoch = datetime.utcfromtimestamp(0)

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

        from_time = time.time()
        to_time = None;
        logger.debug(time_frame)
        if time_frame == 'day':
            to_time = datetime.now() - timedelta(days=1)
            to_time = (to_time - epoch).total_seconds() * 1000.0
            logger.debug(to_time)

        lastfm_data = requests.get(lastfm_api_url.format(username, to_time, from_time, api_key)).json()
        logger.debug(lastfm_data)



