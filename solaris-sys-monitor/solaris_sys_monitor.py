import os
from mago.test_suite.solaris_sys_monitor import SolarisSysMonitorTestSuite

class SysMonitorTest(SolarisSysMonitorTestSuite):
    def sys_info_test(self):
        self.application.verify_sysinfo()

    def processes_view_test(self, view=None):
        self.application.change_view(view)

    def resources_test(self):
        self.application.verify_resource_info()

    def pref_test(self):
        self.application.open_preferences()

if __name__ == "__main__":
    solaris_sys_monitor_test = SysMonitorTest()
    solaris_sys_monitor_test.run()
