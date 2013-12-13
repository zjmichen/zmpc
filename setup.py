from distutils.core import setup

setup(
  name = 'zmpc',
  version = '0.2.0',
  package_dir = {'' : 'src'},
  packages = ['zmpc'],
  package_data = {'zmpc' : ['data/img/*.png', 'data/ui/*.glade']},

  author = 'Zack Michener',
  author_email = 'zack@zackmichener.net',
  description = 'A GTK+3 MPD client',
  url = 'http://www.github.com/zjmichen/zmpc',
)
