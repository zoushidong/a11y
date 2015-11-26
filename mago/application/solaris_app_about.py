"""
This is the solaris "app about" module.

The solaris app about module provides wrappers for LDTP to launch and
close app about window.

It verifies the application About function working well.
"""

import ldtp , ooldtp
import re

from .main import Application
from ..gconfwrapper import GConf

class AppAbout(Application):

    def __init__(self):
        Application.__init__(self)


    def start_about(self, app_name, about_widget, about_window):
        """
        It will try to open application about window after this application
        is started.
        about_widget: application about widget, it might be menu or push button 
        about_window: application about window name
        """

        ldtp.launchapp(app_name)
        ldtp.waittillguiexist(self.name)

        mnu = True
        app = ooldtp.context(self.name)

        if app.verifypushbutton(about_widget) == 1 and app.hasstate(about_widget, 'enabled') == 1:
            mnu = False

        if mnu == True:
            app.getchild(about_widget).selectmenuitem()
        else:
            app.getchild(about_widget).click()

        if ldtp.waittillguiexist(about_window) == 0:
            raise ldtp.LdtpExecutionError, "The " + about_window + " window was not found. "

    def close_about(self, about_window):
        """
        It tries to close the about window, which is invoked by start_about method.
        about_window: application about window name
        """
        CLOSE_NAME_1 = "btnClose"
        CLOSE_NAME_2 = "btnOK"

        aboutApp = ooldtp.context(about_window)

        if aboutApp.verifypushbutton(CLOSE_NAME_1) == 1 and aboutApp.hasstate(CLOSE_NAME_1, 'enabled'):
            CLOSE_WIDGET = CLOSE_NAME_1
        elif aboutApp.verifypushbutton(CLOSE_NAME_2) == 1 and aboutApp.hasstate(CLOSE_NAME_2, 'enabled'):
            CLOSE_WIDGET = CLOSE_NAME_2
        else:
            raise ldtp.LdtpExecutionError, "Can not find enabled Close/OK button in About dialog." 

        aboutApp.getchild(CLOSE_WIDGET).click()

        if ldtp.waittillguinotexist(about_window) == 0:
            raise ldtp.LdtpExecutionError, "The " + about_window + " does not quit as expected, there is something wrong..."
