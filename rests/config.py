from django.conf import settings


# =================================
# Config Defaults
# ---------------------------------

DEFAULTS = {
    'TRANSPILE_DEST': '',
    'BASE_URL': 'http://localhost:5000/interface/',
    'POST_TRANSPILE_COMMAND': None,
    'INTERFACE_SRC': '.',
    'MODELS_FILENAME': 'models.ts',
    'AUTO_TRANSPILE': False,
    'AUTH_MIDDLEWARE': None,
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
MODELS_FILENAME = _config['MODELS_FILENAME']
AUTO_TRANSPILE = _config['AUTO_TRANSPILE']
