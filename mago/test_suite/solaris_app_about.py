"""
Solaris app help module contains the definition of the test suites used for solaris
application help testing
"""
from .main import SingleApplicationTestSuite
from ..application.solaris_app_about import AppAbout

class SolarisAppAboutTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = AppAbout
    def teardown(self):
        self.cleanup() 

    def cleanup(self):
        if self.application.is_opened() == 1:
            self.application.close()
        SingleApplicationTestSuite.cleanup(self)


