# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_appearance import SolarisAppearanceTestSuite 

class SolarisFontTests(SolarisAppearanceTestSuite):
    def test_font_change(self, category):
        self.application.change_font(category)

    def test_font_revert(self):
        self.application.revert_font()


if __name__ == "__main__":
    solaris_font_test =  SolarisFontTests()
    solaris_font_test.run()
