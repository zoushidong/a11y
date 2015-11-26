# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_appearance import SolarisAppearanceTestSuite 

class SolarisBackgroundTests(SolarisAppearanceTestSuite):
    def change_background_to_jpg(self, background_path):
        path = os.path.join(self.get_test_dir(),background_path)
        self.application.change_background(path)
        self.application.close()
        self.application.open()
        self.application.revert_background()

    def change_background_to_bmp(self, background_path):
        path = os.path.join(self.get_test_dir(),background_path)
        self.application.change_background(path)
        self.application.close()
        self.application.open()
        self.application.revert_background()

    def change_background_to_png(self, background_path):
        path = os.path.join(self.get_test_dir(), background_path)
        self.application.change_background(path)
        self.application.close()
        self.application.open()
        self.application.revert_background()

    def revert_background_to_default(self):
        self.application.revert_default()

if __name__ == "__main__":
    solaris_background_test =  SolarisBackgroundTests()
    solaris_background_test.run()
