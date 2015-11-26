# -*- coding: utf-8 -*-

import os

from mago.test_suite.solaris_firefox6 import Firefox6TestSuite

class Firefox6SearchTest(Firefox6TestSuite):
    """
    search_eng: specified firefox buddled search engine
    search_cont:specified search keyword
    """
    def testsearch(self, search_eng=None, search_cont=None):
	self.application.search(search_eng, search_cont)

if __name__ == "__main__":
    firefox_test_search = Firefox6SearchTest()
    firefox_test_search.run()
