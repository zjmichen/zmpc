import requests, os, threading, time, urllib.parse
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from xml.etree import ElementTree as ET
from mpd import ConnectionError, CommandError

class NowPlaying:
  UPDATE_INTERVAL = 0.5
  playing = False
  shuffle = False
  repeat = False

  def __init__(self, app):
    self.app = app
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.app.appdir + "/data/ui/nowplaying.glade")
    self.builder.connect_signals(self)

    self.window = self.builder.get_object("win_now_playing")
    self.window.set_application(self.app)

    self.update()
    GObject.timeout_add(self.UPDATE_INTERVAL*1000, self.update)

    self.window.show_all()

  def update(self):
    t = threading.Thread(target=self.update_info)
    t.daemon = True
    t.start()
    return True

  def update_info(self):
    info = {}
    status = {}

    try:
      info = self.app.mpc.currentsong()
      status = self.app.mpc.status()
    except ConnectionError:
      pass
    except ProtocolError:
      sleep(2)

    info['title'] = 'Not Connected' if ('title' not in info) else info['title']
    info['artist'] = '' if ('artist' not in info) else info['artist']
    info['album'] = '' if ('album' not in info) else info['album']

    status['state'] = 'pause' if ('state' not in status) else status['state']
    status['random'] = '0'    if ('random' not in status) else status['random']
    status['repeat'] = '0'    if ('repeat' not in status) else status['repeat']

    lbl_title = self.builder.get_object('lbl_title')
    lbl_title.set_text(info['title'])
    lbl_artist = self.builder.get_object('lbl_artist')
    lbl_artist.set_text(info['artist'])
    lbl_album = self.builder.get_object('lbl_album')
    lbl_album.set_text(info['album'])

    playing = True if status['state'] == 'play' else False
    if playing != self.playing:
      self.playing = playing
      tog_play = self.builder.get_object('tog_play')
      tog_play.set_active(playing)

    shuffle = bool(int(status['random']))
    if shuffle != self.shuffle:
      self.shuffle = shuffle
      tog_shuffle = self.builder.get_object('tog_shuffle')
      tog_shuffle.set_active(shuffle)

    repeat = bool(int(status['repeat']))
    if repeat != self.repeat:
      self.repeat = repeat
      tog_repeat = self.builder.get_object('tog_repeat')
      tog_repeat.set_active(repeat)

    self.update_cover(info)

  def update_cover(self, info):
    img_cover = self.builder.get_object('img_cover')

    if len(info['album']) > 0:
      params = {
        'api_key': self.app.lastfm_key,
        'method': 'album.getinfo'
      }

      params['artist'] = info['artist']
      params['album'] = info['album']

      url = 'http://ws.audioscrobbler.com/2.0/?'
      for k in params:
        url += k + '=' + urllib.parse.quote(params[k]) + '&'

      res = requests.get(url)
      xml = ET.fromstring(res.content.decode())
      cover_url = xml.find("*image[@size='extralarge']").text

      if cover_url != None:
        img_res = self.fetch_image(cover_url)
        img_cover.set_from_pixbuf(img_res)
    else:
      img_cover.set_from_icon_name('gtk-missing-image', Gtk.IconSize.BUTTON)

  def fetch_image(self, url):
    basename = url.split("/")[-1]
    fname = os.path.join(self.app.cache_dir, basename)

    if not os.path.exists(fname):
      res = requests.get(url)
      f = open(fname, "wb")
      f.write(res.content)
      f.close()
      res.close()

    return Pixbuf.new_from_file(fname)

  def on_btn_previous_clicked(self, data):
    try:
      self.app.mpc.previous()
    except ConnectionError:
      pass
    except CommandError:
      pass

    self.update()

  def on_tog_play_toggled(self, data):
    do_play = data.get_active()
    if do_play:
      self.app.play()
    else:
      self.app.pause()

    self.update()

  def on_btn_next_clicked(self, data):
    try:
      self.app.mpc.next()
    except ConnectionError:
      pass
    except CommandError:
      pass

    self.update()

  def on_tog_shuffle_toggled(self, data):
    do_random = data.get_active()
    try:
      self.app.mpc.random(int(do_random))
    except ConnectionError:
      pass
    except CommandError:
      pass

    self.update()

  def on_tog_repeat_toggled(self, data):
    do_repeat = self.builder.get_object('tog_repeat').get_active()
    try:
      self.app.mpc.repeat(int(do_repeat))
    except ConnectionError:
      pass
    except CommandError:
      pass

    self.update()
