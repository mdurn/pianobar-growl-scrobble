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
from gntp.notifier import GrowlNotifier
import socket
import os
import sys
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

# Initalize a new Growl object (localhost does not require a password).
growl = GrowlNotifier(
    applicationName=u'Pianobar',
    notifications=[
        u'Song Start',
        u'Song End',
        u'Song Love',
        u'Song Ban',
        u'Song Shelve',
        u'Song Bookmark',
        u'Artist Bookmark',
        u'Program Error',
        u'Network Error'])

# Register Pianobar with Growl.
try:
    growl.register()
except socket.error:
    # Be silent.
    pass

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
program_icon = u'file://{0}/pandora.png'.format(
    os.path.dirname(argv[0]))

# Show a heart next to a loved song title.
if rating == 1:
    loved_icon = u' ♥'

# Set the cover art to the program icon when it's missing.
cover_art = program_icon
if len(info['coverArt']) > 0:
    cover_art = info[u'coverArt']

try:
    if argc < 1:
        sys.exit(1)
    elif event == u'songstart':
        if LASTFM_NOW_PLAYING:
            network.update_now_playing(artist = artist, album = album, title = title, duration = song_duration)
        if NOTIFY_SONG_START:
            growl.notify(
                noteType=u'Song Start',
                icon=cover_art,
                title=u'{0}{1}'.format(
                    title,
                    loved_icon),
                description=u'{0}\n{1}'.format(
                    artist,
                    album))
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
            growl.notify(
                noteType=u'Song End',
                icon=cover_art,
                title=u'{0}{1}'.format(
                    title,
                    loved_icon),
                description=u'{0}\n{1}'.format(
                    artist,
                    album))
    elif event == u'songlove' and NOTIFY_SONG_LOVE:
        growl.notify(
            noteType='Song Love',
            icon=cover_art,
            title=u'Song Loved',
            description=u'{0}\n{1}\n{2}'.format(
                title,
                artist,
                album))
    elif event == u'songban' and NOTIFY_SONG_BAN:
        growl.notify(
            noteType='Song Ban',
            icon=cover_art,
            title=u'Song Banned',
            description=u'{0}\n{1}\n{2}'.format(
                title,
                artist,
                album))
    elif event == u'songshelf' and NOTIFY_SONG_SHELVE:
        growl.notify(
            noteType='Song Shelve',
            icon=cover_art,
            title=u'Song Shelved',
            description=u'{0}\n{1}\n{2}'.format(
                title,
                artist,
                album))
    elif event == u'songbookmark' and NOTIFY_SONG_BOOKMARK:
        growl.notify(
            noteType='Song Bookmark',
            icon=cover_art,
            title=u'Song Bookmarked',
            description=u'{0}\n{1}\n{2}'.format(
                title,
                artist,
                album))
    elif event == u'artistbookmark' and NOTIFY_ARTIST_BOOKMARK:
        growl.notify(
            noteType='Artist Bookmark',
            icon=cover_art,
            title=u'Artist Bookmarked',
            description=artist)
    elif pret != 1 and NOTIFY_PROGRAM_ERROR:
        growl.notify(
            noteType=u'Program Error',
            icon=program_icon,
            title=u'Pianobar Failed',
            description=pret_str)
    elif wret != 1 and NOTIFY_NETWORK_ERROR:
        growl.notify(
            noteType=u'Network Error',
            icon=program_icon,
            title=u'Network Failed',
            description=wret_str)
except socket.error:
    # Be silent.
    pass
