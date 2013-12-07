#!/usr/bin/python3

import os, re
from gi.repository import Gtk
from mpd import MPDClient

class App:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(Handler())

        self.window = self.builder.get_object("window1")

        mpd_host = os.getenv('MPD_HOST_TEST', 'localhost')
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

    def start(self):
        self.mpc.connect(self.mpd_server, self.mpd_port)
        if (len(self.mpd_pass) > 0):
            self.mpc.password(self.mpd_pass)

        self.update_info()

        print(self.mpc.mpd_version)
        self.window.show_all()

    def update_info(self):
        lbl_title = self.builder.get_object('lbl_title')
        lbl_artist = self.builder.get_object('lbl_artist')
        lbl_album = self.builder.get_object('lbl_album')

        info = self.mpc.currentsong()

        lbl_title.set_text(info['title'])
        lbl_artist.set_text(info['albumartist'])
        lbl_album.set_text(info['album'])


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

app = App()
app.start()
Gtk.main()

