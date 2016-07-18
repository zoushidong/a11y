# -*- coding: utf-8 -*-


from mago.test_suite.solaris_app_about import SolarisAppAboutTestSuite

class SolarisAppAboutTest(SolarisAppAboutTestSuite):
       
    def testAppAbout(self, appname=None, windowname=None, aboutwidget=None, aboutwindow=None, closetype=None, closename=None):
        """
        appname: application execution name
        windowname: application window name
        aboutwidget: the widget which will invoke application About dialog, such as mnuAbout, btnAbout
        aboutwindow: About window name, generally Aboutwindowname
        closetype: application close type, menuitem or pushbutton
        closename: application close widget name, such as mnuQuit, btnClose
        """
        self.application.set_name(windowname)
        self.application.set_close_type(closetype)
        self.application.set_close_name(closename)
        self.application.start_about(appname, aboutwidget, aboutwindow)
        self.application.close_about(aboutwindow)


if __name__ == "__main__":
    solaris_app_about_test = SolarisAppAboutTest()
    solaris_app_about_test.run()
