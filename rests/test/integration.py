import subprocess
import os
import shutil
import tempfile
import json
import contextlib

from django.test import override_settings
from django.test import LiveServerTestCase

from rests.test import ava


# =================================
# Source File Paths
# ---------------------------------

PACKAGE_SRC_DIR = os.path.join(os.path.dirname(__file__), 'package_src')
PACKAGE_JSON = os.path.join(PACKAGE_SRC_DIR, 'package.json')
TSCONFIG_JSON = os.path.join(PACKAGE_SRC_DIR, 'tsconfig.json')
TSCONFIG_MODULE_JSON = os.path.join(PACKAGE_SRC_DIR, 'tsconfig.module.json')
INDEX_JS = os.path.join(PACKAGE_SRC_DIR, 'index.js')


# =================================
# Integration Test Case
# ---------------------------------

class IntegrationTestCase(LiveServerTestCase):

    """
    Subclass of LiveServerTestCase for running TypeScript `ava` tests that
    interact with `rests` interface endpoints.

    """

    ROOT_URL_CONF = None

    # Temporary directory containing test TypeScript package source.
    temp_dir: tempfile.TemporaryDirectory = None
    # Path to test app source.
    app_src_path = None

    @classmethod
    def setUpClass(cls):
        """
        Creates a temporary directory containing TypeScript package source files,
        and then runs `npm install`.


        """
        LiveServerTestCase.setUpClass()
        cls.temp_dir = tempfile.TemporaryDirectory()
        # Setup the TypeScript package files.
        shutil.copy2(PACKAGE_JSON, cls.temp_dir.name)
        shutil.copy2(TSCONFIG_JSON, cls.temp_dir.name)
        shutil.copy2(TSCONFIG_MODULE_JSON, cls.temp_dir.name)
        # Make the source directory and create 'index.js'.
        cls.app_src_path = os.path.join(cls.temp_dir.name, 'src')
        os.mkdir(cls.app_src_path)
        shutil.copy2(INDEX_JS, cls.app_src_path)
        # Install the package
        subprocess.check_call(['npm', 'install'], cwd=cls.temp_dir.name)

    @classmethod
    def tearDownClass(cls):
        """
        Remove the temporary directory.

        """
        cls.temp_dir.cleanup()
        LiveServerTestCase.tearDownClass()

    def _write_ava_test(self, ava_test: ava.Test):
        test_file = open(os.path.join(self.app_src_path, 'test.ts'), "w+")
        test_file.write(ava_test.source())
        test_file.close()

    def _run_ava_test(self, ava_test: ava.Test):
        self._write_ava_test(ava_test=ava_test)

        with override_settings(RESTS={
            'TRANSPILE_DEST': self.app_src_path,
            'BASE_URL': self.live_server_url,
            'POST_TRANSPILE_COMMAND': None,
            'INTERFACE_SRC': 'tests.test_integration',
        },
                ROOT_URLCONF=self.ROOT_URL_CONF):
            from django.core.management import call_command
            call_command('transpile')
            try:
                subprocess.check_call(['npm', 'test'], cwd=self.temp_dir.name,
                                      env={'TEST_SERVER_PORT': self.live_server_url.split(':')[-1], **os.environ})
            except subprocess.CalledProcessError:
                self.fail(msg="Typescript test `{test_name}` failed.".format(test_name=ava_test.name))

    def assertAvaTestPassed(self, ava_test: ava.Test):
        self._run_ava_test(ava_test=ava_test)