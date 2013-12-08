#!/usr/bin/python3

import os, re, sys
from gi.repository import Gtk, GLib, GObject
from mpd import MPDClient

from nowplaying import NowPlaying
from settings import Settings

class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id='com.zackmichener.zmpc')

        mpd_host = os.getenv('MPD_HOST', 'localhost')
        parts = re.split('@', mpd_host, 2)

        if (len(parts) > 1):
            self.mpd_pass = parts[0]
            self.mpd_server = parts[1]
        else:
            self.mpd_pass = ''
            self.mpd_server = parts[0]

        self.mpd_port = os.getenv('MPD_PORT', 6600)

        self.mpc = MPDClient()
        self.mpc.timeout = 10

        self.lastfm_key = os.getenv('LASTFM_KEY', '')
        self.lastfm_secret = os.getenv('LASTFM_SECRET', '')

        self.cache_dir = os.path.join(GLib.get_user_cache_dir(), 'zmpc')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def do_activate(self):
        nowplaying = NowPlaying(self)
        settings = Settings(self)

    def do_startup(self):
        Gtk.Application.do_startup(self)

if __name__ == "__main__":
    GObject.threads_init()
    app = App()
    status = app.run(None)
    sys.exit(status)
