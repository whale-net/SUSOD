"""
Export view for each indvidual page.

Usually populates a templated HTML web page with session data.
Could also call model functions and populate data.
Really the world is your oyster here but this module 
is intended to serve your view pages.
"""

from .index import * # these probably shouldn't be * or we need to define __all__
from .user import *