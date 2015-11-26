"""
This module contains the definition of the test suite used for Solaris Popup Notification preferences testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_notification import Application, SolarisNotification

class SolarisNotificationTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisNotification
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

