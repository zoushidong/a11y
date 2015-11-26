"""
This module contains the definition of the test suite used for Solaris Archive Manager testing.
"""

import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_archive_manager import Application, SolarisArchiveManager
import os

class SolarisArchiveManagerTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisArchiveManager
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()

    def teardown(self):
        if self.application.is_opened():
            self.application.close()

    def cleanup(self):
        file_path = os.getenv('HOME') + '/' + self.application.ARCH_NAME
        if os.access(file_path, os.F_OK):
            os.remove(file_path)
