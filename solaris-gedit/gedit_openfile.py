# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_gedit import GEditTestSuite
from mago.check import FileComparison, FAIL

class GEditOpenfile(GEditTestSuite):
    def testOpenfile(self, oracle=None, filename=None):
        self.application.open_file(filename)

    def testOpenfiles(self, oracle=None, filename1=None,filename2=None,filename3=None):
        self.application.open_files(filename1,filename2,filename3)
if __name__ == "__main__":
    solaris_gedit_test = GEditOpenfile()
    solaris_gedit_test.run()
