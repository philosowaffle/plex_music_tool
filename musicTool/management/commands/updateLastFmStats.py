from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from musicTool.models import Task, Async

import musicTool.async_runner as async_runner

import logging
import requests
import collections
import time
import sqlite3
import thread

logger = logging.getLogger(__name__)

lastfm_api_url = 'https://ws.audioscrobbler.com/2.0/?method=user.getweeklytrackchart&user={}&from={}&to={}&api_key={}&format=json'
epoch = datetime.utcfromtimestamp(0)

script = """
conn = sqlite3.connect(\'{}\')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

query = {}

try:
    cursor.executescript(query)
    conn.commit()
except Exception as e:
    if cursor:
        conn.rollback()
        cursor.close()
        self.log_error("Failed to run query against the database: " + query, e)
    raise e

if cursor:
    cursor.close()

                """

def update_lastfm(options):
    logger.debug(options)
    username = options['username']
    api_key = options['api_key']
    db_path = options['db_path']
    plex_username = options['plex_username']

    # TODO: Remove
    Task.objects.all().delete()
    Async.objects.all().delete()



    if username is None:
        raise CommandError('Must provide LastFm username.')
    if api_key is None:
        raise CommandError('Must provide API Key.')
    if db_path is None:
        raise CommandError('Must provide Plex Database path.')
    if plex_username is None:
        raise CommandError('Must provide Plex Username.')

    conn = None
    cursor = None
    plex_user_id = None

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM accounts WHERE accounts.name='{}'".format(plex_username))
        plex_user_id = cursor.fetchone()["id"]
    except OperationalException as e:
        if cursor:
            cursor.close()
        self.log_error("Failed to find plex user with username: {}".format(plex_username), e)
        return
    except Exception as e:
        if cursor:
            cursor.close()
        self.log_error("Failed to find plex user with username: {}".format(plex_username), e)
        raise e

    to_time = time.time()
    query = ""

    from_time = datetime.now() - relativedelta(years=30)
    from_time = (from_time - epoch).total_seconds()

    logger.debug("Querying LastFm for user {} using API Key {} and will insert into database {}".format(username, api_key, db_path))

    lastfm_data = requests.get(lastfm_api_url.format(username, from_time, to_time, api_key)).json()
    lastfm_data = lastfm_data['weeklytrackchart']['track']

    # whether or not we should kick off a runner
    start_runner = False

    # for performance will build Tasks with a set of 100 queries
    set_counter = 0
    set_max = 500

    for item in enumerate(lastfm_data):
        try:
            song = item[1]
            song_name = song['name']
            song_name = clean_song_name(song_name)
            song_artist = song['artist']['#text']
            song_playcount = song['playcount']

            single_query = """\"\"\"
                                UPDATE metadata_item_settings SET view_count={0} WHERE guid IN (SELECT guid FROM metadata_items WHERE metadata_type = 10 AND account_id = {2} AND UPPER(title) = UPPER({1}));

                                INSERT INTO metadata_item_settings (guid, account_id, view_count)  SELECT guid, {2}, {0} FROM metadata_items WHERE metadata_type = 10 AND UPPER(title) = UPPER({1}) AND changes() = 0;

                            \"\"\"
                        """.format(song_playcount, song_name, plex_user_id)

            if set_counter is 0:
                query = single_query
                set_counter = set_counter + 1
            elif set_counter < set_max:
                query = query + "\n\n" + single_query
                set_counter = set_counter + 1
            else:
                query = query + "\n\n" + single_query
                task = Task()
                task.script = script.format(db_path, query)
                task.save()
                set_counter = 0
                start_runner = True

        except Exception as e:
            log_error("Failed to update data for: {}".format(item), e)
            pass

    # Check one last time becuase we may not have an even split or a min size of 100
    if set_counter < set_max or set_counter is set_max:
        task = Task()
        task.script = script.format(db_path, query)
        task.save()
        start_runner = True

    # Start async runner
    if start_runner:
        logger.debug("Starting async runner.")
        async_runner.start()

    if cursor:
        cursor.close()

def clean_song_name(song_name):
    # Escape "
    song_name = song_name.replace('\"','\"\"')

    # Escape '
    song_name = song_name.replace('\'', "''")

    # Escape \u2019 and others
    song_name = song_name.replace(u"\u2019", "''")
    song_name = song_name.replace(u"\u2010", "-")
    song_name = song_name.replace(u"\u2013", "-")
    song_name = song_name.replace(u"\xe1", "a")
    song_name = song_name.replace(u"\xe0", "a")
    song_name = song_name.replace(u"\xe9", "e")
    song_name = song_name.replace(u"\xea", "e")
    song_name = song_name.replace(u"\xc9", "E")
    song_name = song_name.replace(u"\xf6", "o")
    song_name = song_name.replace(u"\xf3", "o")
    song_name = song_name.replace(u"\xed", "i")
    song_name = song_name.replace(u"\xec", "i")
    song_name = song_name.replace(u"\xfa", "u")
    song_name = song_name.replace(u"\xfc", "u")
    song_name = song_name.replace(u"\xdc", "U")
    song_name = song_name.replace(u"\xf1", "n")
    song_name = song_name.replace(u"\u2026", "...")
    song_name = song_name.replace(u"\xbf", "")

    # Add surrounding quotes
    song_name = "'" + song_name + "'"

    return song_name

def log_error(msg, e):
    logger.error(msg + "\n" \
                 + str(e))

class Command(BaseCommand):
    help = 'Gets play count and last played data from LastFm and updates Plex music stats.'

    def add_arguments(self, parser):
        parser.add_argument('username')
        parser.add_argument('api_key')
        parser.add_argument('db_path')
        parser.add_argument('plex_username')

    def handle(self, *args, **options):

        thread.start_new_thread(update_lastfm, (options, ))
