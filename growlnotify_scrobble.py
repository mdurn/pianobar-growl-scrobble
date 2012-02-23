#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sends Growl notications on behalf of Pianobar.
   Scrobbles to Last.fm"""

# Notify when a song starts.
NOTIFY_SONG_START = True

# Notify when a song ends.
NOTIFY_SONG_END = False

# Notify when a song is loved.
NOTIFY_SONG_LOVE = True

# Notify when a song is banned.
NOTIFY_SONG_BAN = True

# Notify when a song is shelved.
NOTIFY_SONG_SHELVE = True

# Notify when a song is bookmarked.
NOTIFY_SONG_BOOKMARK = True

# Notify when an artist is bookmarked.
NOTIFY_ARTIST_BOOKMARK = True

# Notify on program error.
NOTIFY_PROGRAM_ERROR = True

# Notify on network error.
NOTIFY_NETWORK_ERROR = True

# Last.fm Scrobble
LASTFM_SCROBBLE = True

# Last.fm now playing
LASTFM_NOW_PLAYING = True

# Last.fm Ban
LASTFM_BAN = True

# Last.fm Love
LASTFM_LOVE = True

# Last.fm variables
API_KEY = "################################"
API_SECRET = "################################"
USERNAME = "########"
PASSWORD = "########"

# When is a scrobble a scrobble?
# See http://www.last.fm/api/scrobbling#when-is-a-scrobble-a-scrobble
THRESHOLD = 50 # the percentage of the song that must have been played to scrobble
PLAYED_ENOUGH = 240 # or if it has played for this many seconds
MIN_DURATION = 30 # minimum duration for a song to be "scrobblable"

# Imports
import socket
import os
import sys
import subprocess
import urllib
import time #lastfm
import pylast #lastfm

# Script Arguments
argv = os.sys.argv
argc = len(argv)

event = argv[1]

# Last.fm network
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = USERNAME, password_hash = pylast.md5(PASSWORD))

# Stores Pianobar information.
info = {}

# Parse stdin into the dictionary.
for line in sys.stdin:
    key, delimiter, value = unicode(line).strip().partition(u'=')
    if value.isdigit():
        info[key] = int(value)
    else:
        info[key] = value

# fields: title, artist, album, songDuration, songPlayed, rating, stationName, pRet, pRetStr, wRet, wRetStr
album = info[u'album']
artist = info[u'artist']
loved_icon = u''
rating = info[u'rating']
pret = info[u'pRet']
pret_str = info[u'pRetStr']
wret = info[u'wRet']
wret_str = info[u'wRetStr']
title = info[u'title']
song_duration = int(info[u'songDuration'])
song_played = int(info[u'songPlayed'])

# The icon will be used when song cover art is missing.
program_icon = u'{0}/pandora.png'.format(
    os.path.dirname(argv[0]))

# Show a heart next to a loved song title.
if rating == 1:
    loved_icon = u' ♥'

# Set the cover art to the program icon when it's missing.
cover_art = program_icon
art_path = u'{0}/cover_art'.format(
             os.path.dirname(argv[0]))
if len(info['coverArt']) > 0:
    cover_art = art_path
try:
    if argc < 1:
        sys.exit(1)
    elif event == u'songstart':
        # Download cover art if there is any
        if len(info['coverArt']) > 0:
            image_binary = urllib.urlopen(info['coverArt'])
            art_file = open(art_path, "wb")
            art_file.write(image_binary.read())
            art_file.close()
        if LASTFM_NOW_PLAYING:
            network.update_now_playing(artist = artist, album = album, title = title, duration = song_duration)
        if NOTIFY_SONG_START:
            p1 = subprocess.Popen(['echo', u'{0}\n{1}'.format(artist, album)], stdout=subprocess.PIPE)
            subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
                u'{0}{1}'.format(title, loved_icon)], stdin=p1.stdout)
            p1.stdout.close()
    elif event == u'songfinish':
        if LASTFM_SCROBBLE and song_duration > 1000*MIN_DURATION and (100.0 * song_played / song_duration > THRESHOLD or song_played > 1000*PLAYED_ENOUGH):
            song_started = int(time.time() - song_played / 1000.0)
            network.scrobble(artist = artist, title = title, timestamp = song_started)
        if (LASTFM_LOVE or LASTFM_BAN) and rating > 0:
            track = network.get_track(artist, title)
            if LASTFM_LOVE and rating == 1:
                track.love()
            elif LASTFM_BAN and rating == 2:
                track.ban() 
        if NOTIFY_SONG_END:
            p1 = subprocess.Popen(['echo', u'{0}\n{1}'.format(artist, album)], stdout=subprocess.PIPE)
            subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
                u'{0}{1}'.format(title, loved_icon)], stdin=p1.stdout)
            p1.stdout.close()
    elif event == u'songlove' and NOTIFY_SONG_LOVE:
        p1 = subprocess.Popen(['echo', u'{0}\n{1}\n{2}'.format(title, artist, album)], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
            u'Song Loved'], stdin=p1.stdout)
        p1.stdout.close()
    elif event == u'songban' and NOTIFY_SONG_BAN:
        p1 = subprocess.Popen(['echo', u'{0}\n{1}\n{2}'.format(title, artist, album)], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
            u'Song Banned'], stdin=p1.stdout)
        p1.stdout.close()
    elif event == u'songshelf' and NOTIFY_SONG_SHELVE:
        p1 = subprocess.Popen(['echo', u'{0}\n{1}\n{2}'.format(title, artist, album)], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
            u'Song Shelved'], stdin=p1.stdout)
        p1.stdout.close()
    elif event == u'songbookmark' and NOTIFY_SONG_BOOKMARK:
        p1 = subprocess.Popen(['echo', u'{0}\n{1}\n{2}'.format(title, artist, album)], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
            u'Song Bookmarked'], stdin=p1.stdout)
        p1.stdout.close()
    elif event == u'artistbookmark' and NOTIFY_ARTIST_BOOKMARK:
        p1 = subprocess.Popen(['echo', artist], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', cover_art, '-d', '12',
            u'Artist Bookmarked'], stdin=p1.stdout)
        p1.stdout.close()
    elif pret != 1 and NOTIFY_PROGRAM_ERROR:
        p1 = subprocess.Popen(['echo', pret_str], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', program_icon, '-d', '12',
            u'Pianobar Failed'], stdin=p1.stdout)
        p1.stdout.close()
    elif wret != 1 and NOTIFY_NETWORK_ERROR:
        p1 = subprocess.Popen(['echo', wret_str], stdout=subprocess.PIPE)
        subprocess.Popen(['growlnotify', '--image', program_icon, '-d', '12',
            u'Network Failed'], stdin=p1.stdout)
        p1.stdout.close()
except socket.error:
    # Be silent.
    pass
