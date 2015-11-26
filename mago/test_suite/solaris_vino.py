"""
This module contains the definition of the test suite used for Solaris Remote Desktop testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_vino import Application, SolarisVino


class SolarisVinoTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisVino
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()
    def cleanup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()
    def teardown(self):
        if self.application.is_opened():
            self.application.close()
