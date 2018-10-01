from __future__ import unicode_literals, absolute_import

import sys

import django
from django.test.utils import get_runner


# =================================
# Run Tests
# ---------------------------------

def run_tests(*test_args):
    """
    Run `rests` tests. Use `test_args` to specify which tests to run,
    otherwise, all will be run.

    """
    from django.conf import settings

    # This tells django the settings to use for the tests - a stand-in
    # for using a `settings.py` file.
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    "debug": True,  # We want template errors to raise
                }
            },
        ],
        MIDDLEWARE=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',
            'rest_framework',
            'rest_framework.authtoken',
            'rests',
            'tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
    )

    if not test_args:
        test_args = ['tests']

    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(test_args)
    sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])