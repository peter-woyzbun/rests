import pathlib


DEBUG = True
SECRET_KEY = '4l0ngs3cr3tstr1ngw3lln0ts0l0ngw41tn0w1tsl0ng3n0ugh'
ROOT_URLCONF = 'example.urls'

DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        }

INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework.authtoken',
            'rests',
            'example'
        )


# =================================
# RESTS Config
# ---------------------------------

ROOT_DIR = pathlib.Path(__file__).parent.parent


RESTS = {
    'TRANSPILE_DEST': ROOT_DIR / 'ts',
    'BASE_URL': 'http://localhost:5000/interface/',
    'POST_TRANSPILE_COMMAND': None,
    'INTERFACE_SRC': 'example.interface',
    'MODELS_FILENAME': 'models.ts'
}
