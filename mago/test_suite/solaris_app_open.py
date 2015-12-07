"""
Opensolaris module contains the definition of the test suites used for opensolaris
applications. It's in solaris/mago/test_suit/
"""
from .main import SingleApplicationTestSuite
from ..application.solaris_app_open import SolarisAppOpen

class SolarisAppOpenTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisAppOpen
    def teardown(self):
        self.cleanup()
#        SingleApplicationTestSuite.cleanup(self)
    def cleanup(self):
#    	SolarisAppOpen.close_app(self)
        print " "
