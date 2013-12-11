from gi.repository import GObject, Gst

Gst.init(None)

class Stream:
  def __init__(self, uri):
    self.streaming = False
    self.pipe = self.getPipeline(uri)

  def getPipeline(self, uri):
    pipe = Gst.Pipeline()
    playbin = Gst.ElementFactory.make("playbin", None)
    pipe.add(playbin)
    playbin.set_property('uri', uri)
    return pipe

  def start(self):
    self.pipe.set_state(Gst.State.PLAYING)
    self.streaming = True

  def pause(self):
    self.pipe.set_state(Gst.State.PAUSED)
    self.streaming = False

  def stop(self):
    self.pipe.set_state(Gst.State.NULL)
    self.streaming = False

