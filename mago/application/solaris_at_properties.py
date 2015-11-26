PACKAGE = "solaris-at-properties"

#-*- coding:utf-8 -*-

"""
This is the "solaris_at_properties" module.

This module provides a wrapper for LDTP to make writting of Solaris AT-Properties tests easier.
"""

import ooldtp
import ldtp
from .main import Application
from ..gconfwrapper import GConf
import time
from ..cmd import globals
import gettext

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext


class SolarisAtProperties(Application):
    """
    SolarisAtProperties manages the solaris gnome-at-properties application in active mode.
    """

    LAUNCHER = 'gnome-at-properties'
    LAUNCHER_ARGS = []
    CLOSE_TYPE = 'button'
    CLOSE_NAME = _('btnClose')

    WINDOW = _('dlgAssistiveTechnologiesPreferences')
    BTN_CLOSEANDLOGOUT = _('btnCloseandLogOut')
    BTN_MOUSEACCESSIBILITY = _('btnMouseAccessibility')
    BTN_HELP = _('btnHelp')
    BTN_KEYBOARDACCESSIBILITY = _('btnKeyboardAccessibility')
    BTN_CLOSE = _('btnClose')
    BTN_PREFERREDAPPLICATIONS = _('btnPreferredApplications')
    CHK_ENABLEASSISTIVETECHNOLOGIES = _('chkEnableassistivetechnologies')

    DLG_PREFERRED_APPLICATIONS = _('dlgPreferredApplications')
    DLG_KEYBOARD_PREFERENCES = _('dlgKeyboardPreferences')
    DLG_MOUSE_PREFERENCES = _('dlgMousePreferences')

    def __init__(self):
        Application.__init__(self)

    def chk_pref_app(self):
        """
        To check the Preferred Application feature
        """
        at = ooldtp.context(self.WINDOW)
        at.getchild(self.BTN_PREFERREDAPPLICATIONS).click()
        if ldtp.waittillguiexist(self.DLG_PREFERRED_APPLICATIONS) == 1:
            ldtp.click(self.DLG_PREFERRED_APPLICATIONS, self.BTN_CLOSE)
        else:
            raise ldtp.LdtpExecutionError, "Failed to check Preferred Applications"

        ldtp.wait(1)

    def chk_enable_a11y(self):
        """
        To check whether the Enable assistive technologies checkbox checked
        """
        at = ooldtp.context(self.WINDOW)
        if at.getchild(self.CHK_ENABLEASSISTIVETECHNOLOGIES).verifycheck() != 1:
            raise ldtp.LdtpExecutionError, "Something wrong with the session! Enable assistive technologies checkbox is not checked!"
        ldtp.wait(1)

    def chk_keyboard_a11y(self):
        """
        To check the Keyboard Accessibility feature.
        """
        at = ooldtp.context(self.WINDOW)
        at.getchild(self.BTN_KEYBOARDACCESSIBILITY).click()
        if ldtp.waittillguiexist(self.DLG_KEYBOARD_PREFERENCES) == 1:
            ldtp.click(self.DLG_KEYBOARD_PREFERENCES, self.BTN_CLOSE)
        else:
            raise ldtp.LdtpExecutionError, "Failed to check Keyboard Accessibility feature"
        ldtp.wait(1)

    def chk_mouse_a11y(self):
        """
        To check the Mouse Accessibility feature.
        """
        at = ooldtp.context(self.WINDOW)
        at.getchild(self.BTN_MOUSEACCESSIBILITY).click()
        if ldtp.waittillguiexist(self.DLG_MOUSE_PREFERENCES) == 1:
            ldtp.click(self.DLG_MOUSE_PREFERENCES, self.BTN_CLOSE)
        else:
            raise ldtp.LdtpExecutionError, "Failed to check Mouse Accessibility feature"
        ldtp.wait(1)

