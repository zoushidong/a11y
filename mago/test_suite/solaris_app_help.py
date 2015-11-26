"""
Solaris app help module contains the definition of the test suites used for solaris
application help testing
"""
from .main import SingleApplicationTestSuite
from ..application.solaris_app_help import AppHelp

class SolarisAppHelpTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = AppHelp
    def teardown(self):
        self.cleanup() 

    def cleanup(self):
        if self.application.is_opened() == 1:
            self.application.close()
        SingleApplicationTestSuite.cleanup(self)


