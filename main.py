#!/usr/bin/python3

from gi.repository import Gtk

class App:

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("main.glade")
        builder.connect_signals(Handler())

        self.window = builder.get_object("window1")

    def start(self):
        self.window.show_all()

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

app = App()
app.start()
Gtk.main()

