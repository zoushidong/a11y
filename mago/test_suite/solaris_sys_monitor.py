"""
This module contains the definition of the test suite used for Solaris Gnome-System-Monitor testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_sys_monitor import Application, SolarisSysMonitor


class SolarisSysMonitorTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = SolarisSysMonitor
    def setup(self):
        if self.application.is_opened():
            self.application.close()
        self.application.open()

    def teardown(self):
        if self.application.is_opened():
            self.application.close()
