from gi.repository import Gtk

class Settings:
  def __init__(self, app):
    self.app = app

    self.builder = Gtk.Builder()
    self.builder.add_from_file("settings.glade")
    self.builder.connect_signals(self)

    self.window = self.builder.get_object("win_settings")
    self.window.set_application(self.app)
    self.window.show_all()

  def on_btn_save_clicked(self, data):
    self.window.destroy()

  def on_btn_cancel_clicked(self, data):
    self.window.destroy()
