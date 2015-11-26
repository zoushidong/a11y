# -*- coding: utf-8 -*-

import os

from mago.test_suite.solaris_firefox6 import Firefox6TestSuite

class Firefox6HomeTest(Firefox6TestSuite):
    """
    home_page: specified home page
    title:     specified home page title
    """
    def testhome(self, home_page=None, title=None):
	self.application.actions('Home')
	self.application.chgHome(home_page)
	self.application.actions('Home')
        if self.application.load_cmplt():
            tab_index = self.application.get_tab_count() - 1 
            if self.application.getTitle(tab_index) == title:
	        self.application.rstHome()
	        self.application.actions('Home')
	        if self.application.load_cmplt() and self.application.getTitle(tab_index) != title:
	       	    pass
	        else:
		    raise AssertionError,  "Failed to restore homepage to default one."
	    else:
                raise AssertionError, "Failed to change the home page to specified: " + title +"."
        else:
            raise AssertionError, "Failed to load the home page " + home_page + "."

if __name__ == "__main__":
    firefox_test_home = Firefox6HomeTest()
    firefox_test_home.run()
