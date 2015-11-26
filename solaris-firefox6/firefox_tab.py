# -*- coding: utf-8 -*-

import os

from mago.test_suite.solaris_firefox6 import Firefox6TestSuite

class Firefox6TabTest(Firefox6TestSuite):
    """
    new_tab: specified web page opened in new tab
    title:   new tab page title
    """
    def testtab(self, new_tab=None, title=None):
	self.application.open_tab()
	self.application.chgHome(new_tab)
	self.application.actions('Home')
        if self.application.load_cmplt():
            tab_index = self.application.get_tab_count() - 1
            if self.application.getTitle(tab_index) == title:
	        pass
	    else:
                raise AssertionError, "Failed to open " + title + " page in new tab!"
        else:
            raise AssertionError, "Failed to finish load homepage " + title + "."

if __name__ == "__main__":
    firefox_test_tab = Firefox6TabTest()
    firefox_test_tab.run()
