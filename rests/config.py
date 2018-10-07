from django.conf import settings


# =================================
# Config Defaults
# ---------------------------------

DEFAULTS = {
    'TRANSPILE_DEST': '',
    'BASE_URL': 'http://localhost:5000/interface/',
    'POST_TRANSPILE_COMMAND': None,
    'INTERFACE_SRC': '.',
    'DATETIME_TYPE': 'moment'
}


# =================================
# Config Values
# ---------------------------------

_config = {**DEFAULTS, **getattr(settings, 'RESTS', {})}


TRANSPILE_DEST = _config['TRANSPILE_DEST']
BASE_URL = _config['BASE_URL']
POST_TRANSPILE_COMMAND = _config['POST_TRANSPILE_COMMAND']
INTERFACE_SRC = _config['INTERFACE_SRC']
