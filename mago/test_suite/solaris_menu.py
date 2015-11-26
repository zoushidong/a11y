"""
Opensolaris module contains the definition of the test suites used for opensolaris
applications
"""
from .main import SingleApplicationTestSuite
from ..application.solaris_menu import SolarisMenu

class SolarisMenuTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisMenu
    def teardown(self):
        self.cleanup() 

    def cleanup(self):
        if self.application.is_opened() == 1:
            self.application.close()
        SingleApplicationTestSuite.cleanup(self)


