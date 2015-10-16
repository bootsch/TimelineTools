#
# Setup.py file to build distribution for Python access to Cinemalib C functions
#
# Author: Paul Boots
# Email: bootsch@acm.org
# Date: 2015-10-12

from distutils.core import setup, Extension

setup (name = 'TimelineTools',
       version = '1.0.0',
       description = 'This package provides EDL and Timecode functionality',
       author = 'Paul Boots',
       author_email = 'bootsch@acm.org',
       packages = ['timeline']
       )


