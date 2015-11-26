"""
Firefox module contains the definition of the test suites used for firefox application
"""

import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.main import Application
from ..application.solaris_firefox6.firefox6 import Firefox

class Firefox6TestSuite(SingleApplicationTestSuite):
    """
    Default test suite for firefox
    """
    APPLICATION_FACTORY = Firefox
    def setup(self):
	self.application.set_name(self.application.WINDOW)
        if self.application.is_opened() == 0:
            self.application.open_with_url('about:blank')
        else:
            pass

        ff=ooldtp.context(self.application.WINDOW)
        if ff.getchild('mnuFile').selectmenuitem() and \
           ff.getchild('mnuFile').selectmenuitem() and \
           ff.getchild('mnuEdit').selectmenuitem() and \
           ff.getchild('mnuEdit').selectmenuitem() and \
           ff.getchild('mnuView').selectmenuitem() and \
           ff.getchild('mnuView').selectmenuitem() and \
           ff.getchild('mnuHistory').selectmenuitem() and \
           ff.getchild('mnuHistory').selectmenuitem() and \
           ff.getchild('mnuBookmarks').selectmenuitem() and \
           ff.getchild('mnuBookmarks').selectmenuitem() and \
           ff.getchild('mnuTools').selectmenuitem() and \
           ff.getchild('mnuTools').selectmenuitem() and \
           ff.getchild('mnuHelp').selectmenuitem() and \
           ff.getchild('mnuHelp').selectmenuitem():
            pass
        else:
            raise ldtp.LdtpExecutionError, "Setting up firefox failed, exiting!"
    def teardown(self):
	self.application.set_name(self.application.WINDOW)
	if self.application.is_opened():
	    self.application.close()
    def cleanup(self):
	pass
