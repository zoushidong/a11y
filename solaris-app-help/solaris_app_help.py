# -*- coding: utf-8 -*-


from mago.test_suite.solaris_app_help import SolarisAppHelpTestSuite

class SolarisAppHelpTest(SolarisAppHelpTestSuite):
       
    def testAppHelp(self, appname=None, windowname=None, helpwidget=None, helpwindow=None, closetype=None, closename=None):
        """
        appname: application execution name
        windowname: application window name
        helpwidget: the widget which will invoke application Help, such as mnuContents, btnHelp
        helpwindow: Help window name, generally windownameManual
        closetype: application close type, menuitem or pushbutton
        closename: application close widget name, such as mnuQuit, btnClose
        """
        self.application.set_name(windowname)
        self.application.start_help(appname, helpwidget, helpwindow)
        self.application.close_help(helpwindow)
        self.application.set_name(windowname)
        self.application.set_close_type(closetype)
        self.application.set_close_name(closename)

if __name__ == "__main__":
    solaris_app_help_test = SolarisAppHelpTest()
    solaris_app_help_test.run()
