"""
Export model functions to be used to get our lovely data.
"""

#example
from .gimme_data import get_test_data


from .user import model_user_login
from .user import model_user_create

from ._header import model_get_menu_options