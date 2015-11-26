# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_appearance import SolarisAppearanceTestSuite 

class SolarisThemeTests(SolarisAppearanceTestSuite):
    def change_gtk_theme(self, tab):
        self.application.change_appearance(tab)

    def change_window_border(self, tab):
	self.application.change_appearance(tab)
    
    def change_icon_theme(self, tab):
        self.application.change_appearance(tab)
    
    def change_pointer_theme(self, tab):
	self.application.change_appearance(tab)

if __name__ == "__main__":
    solaris_theme_test =  SolarisThemeTests()
    solaris_theme_test.run()
