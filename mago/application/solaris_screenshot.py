PACKAGE = "solaris-screenshot"

#-*- coding:utf-8 -*-
"""
This is the "solaris_screenshot" module.

This module provides a wrapper for LDTP to make the writing of Solaris
Screenshot tests easier.
"""
import ooldtp
import ldtp
from .main import Application
from ..gconfwrapper import GConf
import time
from ..cmd import globals
import gettext
import random

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext


class SolarisScreenshot(Application):
    """
    SolarisScreenshot manages the solaris gnome-screenshot application in interactive
    mode.
    """
    LAUNCHER = 'gnome-screenshot'
    LAUNCHER_ARGS = ['--interactive']
    CLOSE_TYPE = 'button'
    CLOSE_NAME = _('btnCancel')

    WINDOW = _('dlgTakeScreenshot')
    
    GRAB_AFTER_DELAY_FIELD = _('sbtnGrabafteradelayof')
    GRAB_THE_WHOLE_DESKTOP_RADIO = _('rbtnGrabthewholedesktop')
    GRAB_THE_CURRENT_WINDOW_RADIO = _('rbtnGrabthecurrentwindow')
    GRAB_A_SELECTED_AREA = _('rbtnSelectareatograb')
    CHK_INCLUDE_POINTER = _('chkIncludepointer')
    CHK_INCLUDE_THE_WINDOW_BORDER = _('chkIncludethewindowborder')
    CBO_APPLY_EFFECT = _('cboApplyeffect')

    TAKE_SCREENSHOT_BUTTON = _('btnTakeScreenshot')

    SAVE_FILE_WINDOW = _('dlgSaveScreenshot')
    SAVE_FILE_BUTTON = _('btnSave')
    SAVE_FILE_NAME_TEXT = _('txtName')
    CBO_SAVE = _('cbo#0')

    def __init__(self):
        Application.__init__(self)

    def take_screenshot(self, option, effects, delay):
        """
        Complete the "Take Screenshot" dialog box by choosing one option
        from whole desktop, current window and select area to grab,
        then clicking Take Screenshot.

        You must have started the application already.

        @type option: char
        @param option: the different name of the radio button
        @type effects: int 
        @param effects: 1 to set effects on, 0 to set effects off
        @type delay: int
        @param delay: The number of seconds to delay before taking the 
                      screenshot.
        """
        screenshot = ooldtp.context(self.WINDOW)

        """
        To choose the radio button according to test case
        """
        if option.__contains__('desktop'):
            radio_button = self.GRAB_THE_WHOLE_DESKTOP_RADIO
        elif option.__contains__('window'):
            radio_button = self.GRAB_THE_CURRENT_WINDOW_RADIO
        elif option.__contains__('area'):
            radio_button = self.GRAB_A_SELECTED_AREA

        #To click the radio button
        while screenshot.getchild(radio_button).verifyuncheck():
            screenshot.getchild(radio_button).click()

        #To set the effects on/off according to test case
        if option.__contains__('desktop'):
            if effects == 1:
                while screenshot.getchild(self.CHK_INCLUDE_POINTER).verifyuncheck():
                    screenshot.getchild(self.CHK_INCLUDE_POINTER).check()
            elif effects == 0:
                while screenshot.getchild(self.CHK_INCLUDE_POINTER).verifycheck():
                    screenshot.getchild(self.CHK_INCLUDE_POINTER).uncheck()
        elif option.__contains__('window'):
            if effects == 1:
                while screenshot.getchild(self.CHK_INCLUDE_POINTER).verifyuncheck():
                    screenshot.getchild(self.CHK_INCLUDE_POINTER).check()
                while screenshot.getchild(self.CHK_INCLUDE_THE_WINDOW_BORDER).verifyuncheck():
                    screenshot.getchild(self.CHK_INCLUDE_THE_WINDOW_BORDER).check()
                screenshot.getchild(self.CBO_APPLY_EFFECT).selectindex(random.randint(1,2))
            elif effects == 0:
                while screenshot.getchild(self.CHK_INCLUDE_POINTER).verifycheck():
                    screenshot.getchild(self.CHK_INCLUDE_POINTER).uncheck()
                while screenshot.getchild(self.CHK_INCLUDE_THE_WINDOW_BORDER).verifycheck():
                    screenshot.getchild(self.CHK_INCLUDE_THE_WINDOW_BORDER).uncheck()
                screenshot.getchild(self.CBO_APPLY_EFFECT).selectindex(0)

        #To set the delay seconds
        if screenshot.getchild(self.GRAB_AFTER_DELAY_FIELD).hasstate('enabled'):
            while int(screenshot.getchild(self.GRAB_AFTER_DELAY_FIELD).getvalue()) != delay:
                screenshot.getchild(self.GRAB_AFTER_DELAY_FIELD).setvalue(delay)


        screenshot.getchild(self.TAKE_SCREENSHOT_BUTTON).click()
        ldtp.waittillguinotexist(self.WINDOW)

        # Select the area of the screen for the screenshot.  As long as your screen is
        # larger than 200x200px this should work fine.
        if option.__contains__('area'):
            try:
                ldtp.generatemouseevent(100,100,'b1p') # button 1 press
                ldtp.generatemouseevent(200,200,'abs') # move mouse to 200,200
                ldtp.generatemouseevent(200,200,'b1r') # button 1 release
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "Error selecting screen area"
 
    
    def save_to_file(self, filename):
        """
        Complete the save to file dialog.  You must have completed a grab_* already

        @type filename: string
        @param filename: The name of the file to save.  This file will be saved 
                         into the current users home folder.  You cannot
                         specify a directory.
        """
        ldtp.wait()
        if ldtp.waittillguiexist(self.SAVE_FILE_WINDOW):
            save_dialog = ooldtp.context(self.SAVE_FILE_WINDOW)
        else:
            raise ldtp.LdtpExecutionError, "Failed to get " + self.SAVE_FILE_WINDOW + " dialog"
        #Set save file name
        save_dialog.getchild(self.SAVE_FILE_NAME_TEXT).settextvalue(filename)
        #Set save file directory to user's home
        save_dialog.getchild(self.CBO_SAVE).selectindex(0)
        save_dialog.getchild(self.SAVE_FILE_BUTTON).click()

        ldtp.waittillguinotexist(self.SAVE_FILE_WINDOW)
