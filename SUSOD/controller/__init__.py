"""
Export controller(api) functions so we can have our flask app 
do something useful that isn't just pretty pages.
"""

#example
from .example import insert_to_test_table

from .user import *

from ._header import *

#from SUSOD.controller.play import play_next