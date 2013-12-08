#!/usr/bin/python3

import os, re, requests, threading, time
from gi.repository import Gtk, GLib, GObject
from gi.repository.GdkPixbuf import Pixbuf
from mpd import MPDClient
from xml.etree import ElementTree as ET

class App:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(Handler(self))

        self.window = self.builder.get_object("window1")

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

    def start(self):
        self.mpc.connect(self.mpd_server, self.mpd_port)
        if (len(self.mpd_pass) > 0):
            self.mpc.password(self.mpd_pass)

        self.update()
        threading.Thread(target=self.watch_status).start()

        print(self.mpc.mpd_version)
        self.window.show_all()

    def watch_status(self):
        while(True):
            self.update()
            time.sleep(1)

    def update(self):
        threading.Thread(target=self.update_info).start()

    def update_info(self):
        info = self.mpc.currentsong()
        print(info)

        lbl_title = self.builder.get_object('lbl_title')
        lbl_title.set_text(info['title'])
        lbl_artist = self.builder.get_object('lbl_artist')
        lbl_artist.set_text(info['albumartist'])
        lbl_album = self.builder.get_object('lbl_album')
        lbl_album.set_text(info['album'])

        self.update_cover(info)

    def update_cover(self, info):
        img_cover = self.builder.get_object('img_cover')
        params = { 
            'api_key': self.lastfm_key,
            'method': 'album.getinfo'
        }

        params['artist'] = info['artist']
        params['album'] = info['album']

        url = 'http://ws.audioscrobbler.com/2.0/?'
        for k in params:
            url += k + '=' + params[k] + '&'

        res = requests.get(url)
        xml = ET.fromstring(res.content.decode())
        cover_url = xml.find("*image[@size='extralarge']")
        if cover_url != None:
            img_res = self.fetch_image(cover_url.text)
            img_cover.set_from_pixbuf(img_res)

    def fetch_image(self, url):
        res = requests.get(url)
        basename = url.split("/")[-1]
        fname = os.path.join(self.cache_dir, basename)
        f = open(fname, "wb")
        f.write(res.content)
        f.close()
        res.close()
        return Pixbuf.new_from_file(fname)

class Handler:
    def __init__(self, app):
        self.app = app

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def on_btn_previous_clicked(self, *args):
        app.mpc.previous()
        app.update()

    def on_btn_playpause_clicked(self, *args):
        app.mpc.pause()
        app.update()

    def on_btn_next_clicked(self, *args):
        app.mpc.next()
        app.update()

GObject.threads_init()
app = App()
app.start()
Gtk.main()
