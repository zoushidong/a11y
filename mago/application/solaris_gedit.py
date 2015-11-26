PACKAGE = "mago"

#-*- coding:utf-8 -*-
"""
This is the "gedit" module.

This module provides a wrapper for LDTP to make writing GEdit tests easier.
"""
import ooldtp
import ldtp
import os
from .main import Application
from ..gconfwrapper import GConf
from ..cmd import globals
import time
import gettext

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext


class GEdit(Application):
    """
    GEdit manages the Gedit application.
    """
    LAUNCHER   = "gedit"
    WINDOW     = _("frm*gedit")
    TXT_FIELD  = "txt*"
    LAUNCHER   = "gedit"
    SAVE_DLG   = _("dlgSave*")
    SAVE_DLG_TXT_NAME = _("txtName")
    SAVE_DLG_BTN_SAVE = _("btnSave")
    OPEN_DLG = _("dlgOpenFiles")
    QUESTION_DLG = _("dlgQuestion")
    QUESTION_DLG_BTN_SAVE = _("btnSave")
    QUESTION_DLG_BTN_SAVE_AS = _("btnSaveAs")
    QUESTION_DLG_BTN_CLOSE = _("btnClosewithoutSaving")
    MNU_QUIT = _("mnuQuit")
    MNU_CLOSE = _("mnuClose")
    MNU_NEW = _("mnuNew")
    MNU_SAVE = _("mnuSave")
    MNU_OPEN = _("mnuOpen")
    OPENFILE_DLG_BTN_TYPEFILENAME=_("tbtnTypeafilename")
    def __init__(self):
        Application.__init__(self)


    def write_text(self, text):
        """
        It writes text to the current buffer of the Gedit window.

        @type text: string
        @param text: The text string to be written to the current buffer.
        """
        Application.write_text(self, text, self.TXT_FIELD)

    def open_file(self,filename):
        gedit = ooldtp.context(self.name)
        gedit.selectmenuitem(self.MNU_OPEN)
        response = ldtp.waittillguiexist(self.OPEN_DLG)
        if not response:
            raise "can not open the dialog of open-a-file."
        openfile_dialog = ooldtp.context(self.OPEN_DLG)
        if not openfile_dialog.objectexist('txtLocation'): 
             print "Location text exist"
             openfile_dialog.click('btnOpen')
        openfile_dialog.settextvalue('txtLocation',filename)
        openfile_dialog.click('btnOpen')

        response = ldtp.waittillguinotexist('dlgOpenaFile','',30)
        if not response:
            raise "can not open the dialog of open-a-file."

    def open_files(self,filename1,filename2,filename3):
        self.open_file(filename1)
        self.open_file(filename2)
        self.open_file(filename3)
        if ldtp.gettabcount(self.name,'ptl1') != 3:
            raise "gedit open multiply file failed."
        
    def save(self, filename):
        """
        It tries to save the current opened buffer to the filename passed as parameter.

        TODO: It does not manage the overwrite dialog yet.

        @type filename: string
        @param filename: The name of the file to save the buffer to.
        """
        Application.save(self, self.MNU_SAVE)
        ooldtp.context(self.name)

        ldtp.waittillguiexist(self.SAVE_DLG)
        save_dialog = ooldtp.context(self.SAVE_DLG)
        
        save_dlg_txt_filename = save_dialog.getchild(self.SAVE_DLG_TXT_NAME)
        ldtp.wait(2)
        save_dlg_txt_filename.settextvalue(filename)

        save_dlg_btn_save = save_dialog.getchild(self.SAVE_DLG_BTN_SAVE)
        
        save_dlg_btn_save.click()

        ldtp.waittillguinotexist(self.SAVE_DLG)
        ldtp.wait(1)

    def close(self, save=False, filename=''):
        """
        Given a gedit window, it tries to close the application.
        By default, it closes without saving. This behaviour can be changed to save (or save as) on close.
         
        @type save: boolean
        @param save: If True, the edited file will be saved on close.

        @type filename: string
        @param filename: The file name to save the buffer to 
        """

        # Exit using the Quit menu 
        gedit = ooldtp.context(self.name)
        quit_menu = gedit.getchild(self.MNU_QUIT)
        quit_menu.selectmenuitem()

        question_dialog = None
        count = 0
        while not gedit.waittillguinotexist(guiTimeOut=1) and \
                count < 10:
            try:
                question_dialog = ooldtp.context(self.QUESTION_DLG)
            except:
                count += 1
            else:
                break

        # If the text has changed, the save dialog will appear
        if question_dialog:
            # Test if the file needs to be saved
            if save:
                try:
                    question_dlg_btn_save = question_dialog.getchild(self.QUESTION_DLG_BTN_SAVE)
                    question_dlg_btn_save.click()
                except ldtp.LdtpExecutionError:
                    # If the Save button was not found, we will try to find the Save As
                    question_dlg_btn_save = question_dialog.getchild(self.QUESTION_DLG_BTN_SAVE_AS)
                    question_dlg_btn_save.click()

                    ldtp.waittillguiexist(self.SAVE_DLG)
                    save_dialog = ooldtp.context(self.SAVE_DLG)
                    
                    save_dlg_txt_filename = save_dialog.getchild(self.SAVE_DLG_TXT_NAME)
                    ldtp.wait(2)
                    save_dlg_txt_filename.settextvalue(filename)

                    save_dlg_btn_save = save_dialog.getchild(self.SAVE_DLG_BTN_SAVE)
                    save_dlg_btn_save.click()

                    ldtp.waittillguinotexist(self.SAVE_DLG)
            
            else:
                question_dlg_btn_close = question_dialog.getchild(self.QUESTION_DLG_BTN_CLOSE)
                question_dlg_btn_close.click()

            gedit.waittillguinotexist(guiTimeOut=20)

