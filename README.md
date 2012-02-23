# Pianobar Growl & Scrobbling Script

This is a combined implementation of scrobbling to Last.fm and Growl notifications for Pianobar,
a console client for Pandora by Lars-Dominik Braun:
https://github.com/PromyLOPh/pianobar

The scrobbling portion of this is based on scrobble.py by Jon Pierce:
https://github.com/PromyLOPh/pianobar/blob/master/contrib/eventcmd-examples/scrobble.py

The growl notification portion using gtnp is based on the pianobar-growl project by Sorin Ionescu:
https://github.com/sorin-ionescu/pianobar-growl

This is handy for those who would rather not use the multi.sh method 
(https://github.com/PromyLOPh/pianobar/blob/master/contrib/eventcmd-examples/multi.sh)
for using multiple event_command scripts. This project also includes a an implementation for Growl
using growlnotify that parallels the features using gntp in pianobar-growl.

## Dependencies

- Python (http://python.org/)
- Pandora account
- Pianobar
- Growl
- growlnotify OR gntp python module (see installation)
- Last.fm account
- Last.fm API credentials (http://www.last.fm/api/account)
- pylast.py (http://code.google.com/p/pylast)

## Installation

1) Copy pylast.py to your Pianobar config directory:
`~/.config/pianobar`

2) Two versions of the script are included here.

- **gntp_scrobble.py:**
This uses the gntp protocol in Growl 1.3 and also requires the gntp python module.

Install the gntp python module:

    pip install gntp

*Note: Until retrieving images from urls is fixed in Growl 1.3, Growl notifications using this approach
will not display album art.*

Set the event_command variable in your Pianobar config file (e.g. `~/.config/pianobar`) to this
script's path:

    event_command = /Users/user/.config/pianobar/gntp_scrobble.py

###OR

- **growlnotify_scrobble.py:**
This is compatible with recent versions of Growl (tested with Growl 1.2 
and 1.3) and requires the installation of growlnotify (included in the Extras folder in the Growl
install package).

Set the event_command variable in your Pianobar config file (e.g. `~/.config/pianobar`) to this
script's path:

    event_command = /Users/user/.config/pianobar/growlnotify_scrobble.py

3) Supply your own Last.fm credentials in either the gntp_scrobble.py or growlnotify_scrobble.py scripts:

    API_KEY = "################################"
    API_SECRET = "################################"
    USERNAME = "########"
    PASSWORD = "########"

4) Save a default icon image for Growl notifications as 'pandora.png' in your Pianobar config directory
(for example, the pandora.png image by Ross A. Reyman included in Sorin Ionescu's pianobar-growl repo:
https://github.com/sorin-ionescu/pianobar-growl)

*Note: Make sure your .py scripts are executable!* `chmod +x`

##Settings

### Growl Settings:
See https://github.com/sorin-ionescu/pianobar-growl for Growl settings.

### Last.fm Settings:
`LASTFM_SCROBBLE`

Allow scrobbling to Last.fm. (**True**/False)

`LASTFM_NOW_PLAYING`

Update now playing on Last.fm with the current track. (**True**/False)

`LASTFM_BAN`

Ban tracks on Last.fm when they are banned on Pianobar. (**True**/False)

`LASTFM_LOVE`

Love tracks on Last.fm when they are loved on Pianobar. (**True**/False)

### Last.fm Scrobbling Rules:
`THRESHOLD`

The percentage of the song that must have been played to scrobble. (Default: **50**)

`PLAYED_ENOUGH`

Scrobble if the song has been played this many seconds. (Default: **240**)

`MIN_DURATION`

Minimum duration for a song (in seconds) in order to be scrobbled. (Default: **30**)

*Note: Unless a song is shorter than MIN_DURATION, a song will scrobble if either the THRESHOLD or PLAYED_ENOUGH 
conditions have been met.*

## Thanks

- Lars-Dominik Braun
- Jon Pierce
- Sorin Ionescu

## License

Copyright (c) 2012 by Michael Durnhofer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
