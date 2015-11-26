PACKAGE = "solaris_vino"

#-*- coding:utf-8 -*-
"""
This is the "solaris_vino" module.

This module provides a wrapper for LDTP to make writing of Solaris Vino
tests easier.
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

class SolarisVino(Application):
    """
    SolarisVino manages the solaris desktop sharing(vino preferences) 
    application in interactive mode.
    """

    LAUNCHER = 'vino-preferences'
    LAUNCHER_ARGS = []
    CLOSE_TYPE = 'button'
    CLOSE_NAME = _('btnClose')

    WINDOW = _('dlgRemoteDesktopPreferences')

    CHK_ENABLE_VIEW = _('chkAllowotheruserstoviewyourdesktop')
    CHK_ENABLE_CTRL = _('chkAllowotheruserstocontrolyourdesktop')
    LBL_DISABLE = _('lblNobodycanaccessyourdesktop')
    LBL_CHECKING = _('lblCheckingtheconnectivityofthismachine*')
    LBL_RESULT = _('lblOtherscanaccessyourcomputerusingtheaddress*5800')
    RBTN_ALWAYS = _('rbtnAlwaysdisplayanicon')
    RBTN_ONLY = _('rbtnOnlydisplayaniconwhenthereissomeoneconnected')
    RBTN_NEVER = _('rbtnNeverdisplayanicon')

    FRM_TOP = _('frmTopExpandedEdgePanel')
    EMB_PANEL = _('embPanelNotificationArea')

    def __init__(self):
        Application.__init__(self)

    def get_status_from_process(self):
        """
        This method gets the vino-server status from system process.
        It parses the output of bash command 'ps -ef | grep vino-server'
        to see whether vino-server is running or not.
        1: vino-server is running
        0: vino-server is not running
        """
        try:
            p1 = Popen(["ps", "-ef"], stdout=PIPE)
            p2 = Popen(["grep", "vino-server"], stdin=p1.stdout, stdout=PIPE)
            output = p2.communicate()[0]
            if output.__contains__("/usr/lib/vino-server"):
                return 1
            else:
                return 0
        except Exception, e:
            print >> sys.stderr, "Execution failed:", e
            return 0

    def get_icon_num(self):
        """
        This method gets the number of icon in top panel notification area.
        It returns the icon number.
        """

        top = ooldtp.context(self.FRM_TOP)
        top.remap()
        key = top.getobjectproperty(self.EMB_PANEL, 'children')
        while len(key.split(' ')) == 1:
            key_save = key
            key = top.getobjectproperty(key, 'children')

        return len(top.getobjectproperty(key_save, 'children').split(' '))

    def toggle_vino(self, status, display):
        """
        This method toggles vino status according to required status and
        display.
        @type status: int
        @type display: int
        @param status: 0 to disable
                       1 to enable
        @param display: 0 to Never display an icon
                        1 to Always display an icon
                        2 to Only display an icon when there is someone
                          connected
        """
        remot = ooldtp.context(self.WINDOW)

        if status == 0:
            if remot.getchild(self.CHK_ENABLE_VIEW).verifycheck() == 1:
                remot.getchild(self.CHK_ENABLE_VIEW).click()
            if self.get_status_from_process() == 0:
                pass
            else:
                raise ldtp.LdtpExecutionError, "Disable the vino-server from vino-preferences dialog doesn't work, please verify it manually!"

        elif status == 1:
            if remot.getchild(self.CHK_ENABLE_VIEW).verifycheck() == 0:
                remot.getchild(self.CHK_ENABLE_VIEW).click()
            if remot.getchild(self.CHK_ENABLE_CTRL).verifycheck() == 0:
                remot.getchild(self.CHK_ENABLE_CTRL).click()
            remot.waittillguiexist(self.LBL_RESULT, 40)
            if self.get_status_from_process() == 0:
                raise ldtp.LdtpExecutionError, "Enable the vino-server from vino-preferences dialgo doesn't work, please verify it manually!"


            remot.getchild(self.RBTN_ALWAYS).click()
            icon_count = self.get_icon_num()
            if display == 0:
                remot.getchild(self.RBTN_NEVER).click()
                icon_count_n = self.get_icon_num()
                if (icon_count - icon_count_n) != 1:
                    raise ldtp.LdtpExecutionError, "Hide icon in notification area failed!"
            elif display == 1:
                icon_count_a = self.get_icon_num()
                if icon_count != icon_count_a:
                    raise ldtp.LdtpExecutionError, "Show icon in notification"
            elif display == 2:
                remot.getchild(self.RBTN_ONLY).click()
                if remot.getchild(self.RBTN_ONLY).verifycheck() == 0:
                    raise ldtp.LdtpExecutionError, "Failed to check the radio button to set 'ONLY connected to show'."
