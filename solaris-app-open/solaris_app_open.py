# -*- coding: utf-8 -*-
""" It's in solaris/solaris_app_open/ """
import ldtp
from mago.test_suite.solaris_app_open import SolarisAppOpenTestSuite

class SolarisAppOpenTest(SolarisAppOpenTestSuite):
       
    def testOpenMenu(self, launchname=None, windowname=None):

        self.application.set_name(windowname)
        self.application.open_app(launchname)
        ldtp.wait(2)
        self.application.close_app(windowname)

if __name__ == "__main__":
    solaris_app_open_test = SolarisAppOpenTest()
    solaris_app_open_test.run()
