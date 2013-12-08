import requests, os, threading, time
from gi.repository import Gtk, GObject
from gi.repository.GdkPixbuf import Pixbuf
from xml.etree import ElementTree as ET
from mpd import ConnectionError

class NowPlaying:
  UPDATE_INTERVAL = 1
  playstate = 'pause'

  def __init__(self, app):
    self.app = app
    self.builder = Gtk.Builder()
    self.builder.add_from_file("nowplaying.glade")
    self.builder.connect_signals(self)

    self.window = self.builder.get_object("win_now_playing")
    self.window.set_application(self.app)

    self.update()
    GObject.timeout_add(self.UPDATE_INTERVAL*1000, self.update)

    self.window.show_all()

  def watch_status(self):
    while(True):
      self.update()
      time.sleep(1)

  def update(self):
    t = threading.Thread(target=self.update_info)
    t.daemon = True
    t.start()
    return True

  def update_info(self):
    try:
      info = self.app.mpc.currentsong()
      status = self.app.mpc.status()
    except ConnectionError:
      info = {
      'title': 'Not Connected',
      'artist': '',
      'album': ''
      }
      status = { 'state': 'pause' }

    lbl_title = self.builder.get_object('lbl_title')
    lbl_title.set_text(info['title'])
    lbl_artist = self.builder.get_object('lbl_artist')
    lbl_artist.set_text(info['artist'])
    lbl_album = self.builder.get_object('lbl_album')
    lbl_album.set_text(info['album'])

    if self.playstate != status['state']:
      self.playstate = status['state']
      btn_playpause = self.builder.get_object('btn_playpause')
      if self.playstate == 'pause':
        btn_playpause.set_icon_name('media-playback-start')
      else:
        btn_playpause.set_icon_name('media-playback-pause')

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
        url += k + '=' + params[k] + '&'

      res = requests.get(url)
      xml = ET.fromstring(res.content.decode())
      cover_url = xml.find("*image[@size='extralarge']")
      if cover_url != None:
        img_res = self.fetch_image(cover_url.text)
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

  def on_btn_previous_clicked(self, *args):
    self.app.mpc.previous()
    self.update()

  def on_btn_playpause_clicked(self, *args):
    self.app.mpc.pause()
    self.update()

  def on_btn_next_clicked(self, *args):
    self.app.mpc.next()
    self.update()

