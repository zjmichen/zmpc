from gi.repository import Gst

Gst.init(None)

class Stream:
  def __init__(self, host, port):
    self.pipe = Gst.Pipeline()
    tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
    self.pipe.add(tcpsrc)
    tcpsrc.set_property("host", host)
    tcpsrc.set_property("port", port)

    decode = Gst.ElementFactory.make("decodebin", "decode")
    decode.connect("pad-added", self.new_decode_pad)
    self.pipe.add(decode)
    tcpsrc.link(decode)

    convert = Gst.ElementFactory.make("audioconvert", "convert")
    self.pipe.add(convert)

    sink = Gst.ElementFactory.make("alsasink", "sink")
    self.pipe.add(sink)
    convert.link(sink)

  def new_decode_pad(dbin, pad, islast):
    pad.link(convert.get_pad("sink"))

  def start(self):
    self.pipe.set_state(Gst.State.PLAYING)

  def stop(self):
    self.pipe.set_state(Gst.State.PAUSED)

