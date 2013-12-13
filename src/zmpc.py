import sys
from gi.repository import GObject
from zmpc.app import App

if __name__ == '__main__':
  GObject.threads_init()
  app = App()
  try:
    status = app.run(sys.argv)
    sys.exit(status)
  except:
    sys.exit(1)
