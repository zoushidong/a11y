import os
from mago.test_suite.solaris_vino import SolarisVinoTestSuite

class VinoTest(SolarisVinoTestSuite):
    def vino_test(self, status=None, display=None):
        self.application.toggle_vino(status, display)

if __name__ == "__main__":
    solaris_vino_test = VinoTest()
    solaris_vino_test.run()
