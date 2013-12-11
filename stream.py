from gi.repository import GObject, Gst

Gst.init(None)

class Stream:
  def __init__(self, host, port):
    self.streaming = False
    self.pipe = self.getPipeline(host, port)

  def getPipeline(self, host, port):
    pipe = Gst.Pipeline()
    playbin = Gst.ElementFactory.make("playbin", None)
    pipe.add(playbin)
    playbin.set_property('uri', 'http://' + host + ':' + str(port))
    return pipe

  def start(self):
    print("Starting stream...")
    self.pipe.set_state(Gst.State.PLAYING)
    self.streaming = True

  def stop(self):
    self.pipe.set_state(Gst.State.PAUSED)
    self.streaming = False

