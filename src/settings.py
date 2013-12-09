from gi.repository import Gtk

class Settings:
  def __init__(self, app):
    self.app = app

    self.builder = Gtk.Builder()
    self.builder.add_from_file("data/ui/settings.glade")
    self.builder.connect_signals(self)

    self.window = self.builder.get_object("win_settings")
    self.window.set_application(self.app)

    ent_server = self.builder.get_object("entry_server")
    ent_server.set_text(self.app.mpd_server)
    ent_port = self.builder.get_object("entry_port")
    ent_port.set_text(str(self.app.mpd_port))
    ent_password = self.builder.get_object("entry_password")
    ent_password.set_text(self.app.mpd_pass)

    self.window.show_all()

  def on_btn_save_clicked(self, data):
    server = self.builder.get_object("entry_server").get_text()
    port = self.builder.get_object("entry_port").get_text()
    password = self.builder.get_object("entry_password").get_text()
    self.window.destroy()

    if len(server) == 0:
      server = 'localhost'
    if len(port) == 0:
      port = 6600

    self.app.mpd_server = server
    self.app.mpd_port = port
    self.app.mpd_pass = password
    self.app.reconnect()


  def on_btn_cancel_clicked(self, data):
    self.window.destroy()
