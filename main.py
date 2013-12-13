#!/usr/bin/python3

import os, re, sys, threading
from gi.repository import Gtk, GLib, GObject, Gio
from mpd import MPDClient

from nowplaying import NowPlaying
from settings import Settings
from stream import Stream

class App(Gtk.Application):
  def __init__(self):
    Gtk.Application.__init__(self, application_id='com.zackmichener.zmpc', register_session=True)
    self.connected = False;

  def connect(self):
    try:
      self.mpc.connect(self.mpd_server, self.mpd_port)
      if (len(self.mpd_pass) > 0):
        self.mpc.password(self.mpd_pass)
      self.connected = True
    except ConnectionRefusedError:
      self.connected = False

  def reconnect(self):
    if self.connected:
      self.mpc.disconnect()
    self.connect()

    do_stream = self.stream.streaming
    self.stream.stop()
    self.stream = Stream(self.mpd_stream_uri)
    if (do_stream):
      self.stream.play()

  def play(self):
    try:
      self.mpc.play()
    except ConnectionError:
      pass
    except CommandError:
      pass

  def pause(self):
    try:
      self.mpc.pause()
    except ConnectionError:
      pass
    except CommandError:
      pass

  def do_activate(self):
    nowplaying = NowPlaying(self)

  def do_startup(self):
    Gtk.Application.do_startup(self)
    self.create_menu()

    mpd_host = os.getenv('MPD_HOST', 'localhost')
    parts = re.split('@', mpd_host, 2)

    if (len(parts) > 1):
      self.mpd_pass = parts[0]
      self.mpd_server = parts[1]
    else:
      self.mpd_pass = ''
      self.mpd_server = parts[0]

    self.mpd_port = os.getenv('MPD_PORT', 6600)
    self.mpd_stream_uri = 'http://' + self.mpd_server + ':' + str(self.mpd_port) + '/'

    self.mpc = MPDClient()
    self.mpc.timeout = 10
    threading.Thread(target=self.connect).start()

    self.lastfm_key = os.getenv('LASTFM_KEY', 'e4dffe2a256bbd37e24ad001c36836a2')
    self.lastfm_secret = os.getenv('LASTFM_SECRET', '')

    self.cache_dir = os.path.join(GLib.get_user_cache_dir(), 'zmpc')
    if not os.path.exists(self.cache_dir):
      os.makedirs(self.cache_dir)

    self.mpd_stream_uri = 'http://pi.zackmichener.net:8004/'
    self.stream = Stream(self.mpd_stream_uri)

  def create_menu(self):
    menu = Gio.Menu()
    menu.append("Settings", "app.settings")
    menu.append("Quit", "app.quit")

    stream_item = Gio.MenuItem.new("Stream", "app.stream")
    stream_item.set_action_and_target_value("app.stream", GLib.Variant.new_boolean(False))

    menu.prepend_item(stream_item)
    self.set_app_menu(menu)

    stream_action = Gio.SimpleAction.new_stateful("stream",
        GLib.VariantType.new('b'),
        GLib.Variant.new_boolean(False))

    stream_action.connect("activate", self.toggle_stream)
    self.add_action(stream_action)

    settings_action = Gio.SimpleAction.new("settings", None)
    settings_action.connect("activate", self.menu_settings)
    self.add_action(settings_action)

    quit_action = Gio.SimpleAction.new("quit", None)
    quit_action.connect("activate", self.menu_quit)
    self.add_action(quit_action)

  def toggle_stream(self, action, parameter):
    if (self.stream.streaming):
      action.change_state(GLib.Variant.new_boolean(True))
      self.stream.stop()
    else:
      action.change_state(GLib.Variant.new_boolean(False))
      self.stream.play()

  def menu_settings(self, action, parameter):
    settings = Settings(self)

  def menu_quit(self, action, parameter):
    self.quit()

  def quit(self):
    self.stream.stop()
    super.quit()

if __name__ == "__main__":
  GObject.threads_init()
  app = App()
  status = app.run(None)
  sys.exit(status)
