"""
This module contains the definition of the test suite for GnomeAppearanceProperties testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_appearance import Application, SolarisAppearance

class SolarisAppearanceTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Solaris Gnome Appearance Properties
    """
    APPLICATION_FACTORY = SolarisAppearance
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
	pass
