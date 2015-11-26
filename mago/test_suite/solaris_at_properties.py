"""
This module contains the definition of the test suite used for Solaris At-Properties testing.
"""

import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_at_properties import Application, SolarisAtProperties

class SolarisAtPropertiesTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisAtProperties
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()

    def teardown(self):
        if self.application.is_opened():
            self.application.close()
