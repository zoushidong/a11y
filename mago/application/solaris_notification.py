PACKAGE = "solaris_notification"

#-*- coding:utf-8 -*-
"""
This is the "solaris_notification" module.

This module provides a wrapper for LDTP to make writing of Solaris 
Notification Properties tests easier.
"""

import ooldtp
import ldtp
from .main import Application
from ..gconfwrapper import GConf
import os
import sys
from subprocess import Popen, call, PIPE
from ..cmd import globals
import gettext

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext

class SolarisNotification(Application):
    """
    SolarisNotification manages the solaris notification properties
    (Pop-up Notifications) application in interactive mode.
    """

    LAUNCHER = 'notification-properties'
    LAUNCHER_ARGS = []
    CLOSE_TYPE = 'button'
    CLOSE_NAME = _('btnClose')

    WINDOW = _('dlgNotificationSettings')
    DLG_NOTIFICATION = _('dlgNotification')
    DLG_ERROR = _('dlgError')
    LBL_ERROR = _('lblErrorwhiledisplayingnotification*')
    BTN_CLOSE = _('btnClose')


    CBO_THEME = _('cboTheme')
    CBO_POSITION = _('cboPosition')
    MNU_STANDARDTHEME = _('mnuStandardtheme')
    MNU_TOPLEFT = _('mnuTopLeft')
    MNU_TOPRIGHT = _('mnuTopRight')
    MNU_BOTTOMLEFT = _('mnuBottomLeft')
    MNU_BOTTOMRIGHT = _('mnuBottomRight')
    BTN_PREVIEW = _('btnPreview')


    def __init__(self):
        Application.__init__(self)

    def notification_preview(self, theme, position):
        """
        This method invokes notification dialog according to preferred theme
        and position
        @theme: Standard theme
        @position: Top Left, Top Right, Bottom Left, Bottom Right
        """
        notif = ooldtp.context(self.WINDOW)
        mnu_theme = ldtp.getchild(self.WINDOW, theme, 'menu item')
        mnu_position = ldtp.getchild(self.WINDOW, position, 'menu item')

        notif.getchild(self.CBO_THEME).comboselect(mnu_theme)
        notif.getchild(self.CBO_POSITION).comboselect(mnu_position)
        if notif.getchild(self.CBO_THEME).verifyselect(theme) == 0:
            raise ldtp.LdtpExecutionError, "Failed to select " + theme + " on Theme combobox."
        if notif.getchild(self.CBO_POSITION).verifyselect(position) == 0:
            raise ldtp.LdtpExecutionError, "Failed to select " + position + " on Position combobox."

        shown = False 
        timer = 1
        ldtp.wait(1)
        while (not shown) and (timer < 3):
            notif.getchild(self.BTN_PREVIEW).click()
            ldtp.wait(1)
            if ldtp.guiexist(self.DLG_NOTIFICATION):
                shown = True
            else:
                ldtp.wait(8)
                if ldtp.guiexist(self.DLG_ERROR):
                    error = ooldtp.context(self.DLG_ERROR)
                    error.getchild(self.BTN_CLOSE).click()
                    if ldtp.guiexist(self.DLG_ERROR) == 0:
                        ldtp.wait(1)
                        timer = timer + 1
                    else:
                        raise ldtp.LdtpExecutionError, "Error dialog can't be dismissed, there is something wrong with the application."
                else:
                    raise ldtp.LdtpExecutionError, "Something wrong with the application, error dialog didn't popup, please check it manually."

        if (not shown) and timer >= 3:
            raise ldtp.LdtpExecutionError, "Notification dialog can't be popup, function fails."
