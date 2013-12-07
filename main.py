#!/usr/bin/python3

import os, re
from gi.repository import Gtk
from mpd import MPDClient

class App:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("main.glade")
        builder.connect_signals(Handler())

        self.window = builder.get_object("window1")

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
            
        print(self.mpc.mpd_version)
        self.window.show_all()

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

app = App()
app.start()
Gtk.main()

