"""
This module contains the definition of the test suite used for Solaris Screenshot
testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_screenshot import Application, SolarisScreenshot


class SolarisScreenshotTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisScreenshot
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()

    def teardown(self):
        if self.application.is_opened():
            self.application.close()
