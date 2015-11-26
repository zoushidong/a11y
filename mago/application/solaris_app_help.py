"""
This is the solaris "app help" module.

The solaris app help module provides wrappers for LDTP to test app help function.

This method only works on gnome-help application, for other help applications, say

firefox online help, please do not use this module.
"""

import ldtp , ooldtp
import re
import platform

from .main import Application
from ..gconfwrapper import GConf


class AppHelp(Application):

    def __init__(self):
        Application.__init__(self)


    def start_help(self, app_name, help_widget, help_window):
        """
        It will try to launch the application, and then open application content help 
        window after application is invoked
        help_widget: application help widget, which includes menuitem and pushbutton
        help_window: application help window name

        """

        ldtp.launchapp(app_name)
        ldtp.waittillguiexist(self.name)

        app = ooldtp.context(self.name)
        mnu = True

        if app.verifypushbutton(help_widget) == 1 and app.hasstate(help_widget, 'enabled') == 1:
            mnu = False

        if mnu == True:
            app.getchild(help_widget).selectmenuitem()
        else:
            app.getchild(help_widget).click()

        if platform.processor() == 'sparc':
            ldtp.wait(45)
        else:
            ldtp.wait(30)

        if ldtp.guiexist(help_window) == 0:
            raise ldtp.LdtpExecutionError, "The help window " + help_window + " can't be invoked, something wrong with the application help."

    def close_help(self, help_window):
        """
        It tries to close the help window(gnome-help), which is invoked by start_help method.
        help_window: application help window name
        """
        helpApp = ooldtp.context(help_window)
        helpApp.getchild('mnuCloseWindow').selectmenuitem()

        if ldtp.waittillguinotexist(help_window) == 0:
            raise ldtp.LdtpExecutionError, "The " + help_window + " does not quit as expected, there is something wrong..."

