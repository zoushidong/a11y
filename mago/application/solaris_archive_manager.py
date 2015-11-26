PACKAGE = "solaris_archive_manager"

#-*- coding:utf-8 -*-
"""
This is the "solaris_archive_manager" module.

This module provides a wrapper for LDTP to make the writing of Solaris
Archive Manager tests easier.
"""
import ooldtp
import ldtp
from .main import Application
from ..gconfwrapper import GConf
import time
from ..cmd import globals
import gettext
import os

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext

class SolarisArchiveManager(Application):
    """
    SolarisArchiveManager manages the solaris file-roller application in interactive mode.
    """

    LAUNCHER = 'file-roller'
    LAUNCHER_ARGS = []
    CLOSE_TYPE = 'menu'
    CLOSE_NAME = _('mnuClose')

    WINDOW = _('frmArchiveManager')

    BTN_NEW = _('btnNew')
    BTN_OPEN = _('btnOpen')
    BTN_EXTRACT = _('btnExtract')
    BTN_ADDFILES = _('btnAddFiles')
    BTN_ADDFOLDER = _('btnAddFolder')
    MNU_LASTOUTPUT = _('mnuLastOutput')

    DLG_NEW = _('dlgNew')
    ARCH_NAME = _('test_archive_file.tar.gz')
    TXT_NAME = _('txtName')
    CBO_SAVE_IN_FOLDER = _('cboSaveinfolder')
    BTN_CREATE = _('btnCreate')

    DLG_ADD_FILES = _('dlgAddFiles')
    DLG_ADD_A_FOLDER = _('dlgAddaFolder')
    TBTN_TYPE_A_FILE_NAME = _('tbtnTypeafilename')
    TXT_LOCATION = _('txtLocation')
    BTN_ADD = _('btnAdd')
    TBTN_FILESYSTEMROOT = _('tbtnFileSystemRoot')

    DLG_OPEN = _('dlgOpen')
    BTN_OPEN = _('btnOpen')

    DLG_EXTRACT = _('dlgExtract')
    BTN_EXTRACT = _('btnExtract')
    FILE_NAME = _('archive.tar.gz')
    EXTRACT_PATH = _('/tmp/')
    DLG_EXTRACTING_FILES_FROM_ARCHIVE = _('dlgExtractingfilesfromarchive')
    BTN_CLOSE = _('btnClose')
    LBL_EXTRACTION = _('lblExtractioncompletedsuccessfully')

    DLG_LASTOUTPUT = _('dlgLastOutput')
    TXT_0 = _('txt0')

    def __init__(self):
        Application.__init__(self)

    def create_archive(self, src_path, tag):
        """
        To create a new archive file in user's home directory

        @type src_path: char
        @param src_path: source file/folder path
        @type tag: int
        @param tag: 0 for folder, 1 for file
        """
        archive = ooldtp.context(self.WINDOW)

        archive.getchild(self.BTN_NEW).click()

        ldtp.waittillguiexist(self.DLG_NEW)

        """
        Remove the file which might have same file name
        A workaround to the bug #7151417
        """
        exist_file_path = os.getenv('HOME') + '/' + self.ARCH_NAME
        if os.access(exist_file_path, os.F_OK):
            os.remove(exist_file_path)

        """
        Give a archive file name, then create this file.
        """
        new = ooldtp.context(self.DLG_NEW)
        new.getchild(self.TXT_NAME).settextvalue(self.ARCH_NAME)
        new.getchild(self.CBO_SAVE_IN_FOLDER).selectindex(0)
        new.getchild(self.BTN_CREATE).click()
        ldtp.waittillguinotexist(self.DLG_NEW)
        """
        If tag == 1, add a file to archive file
        If tag == 0, add a folder to archive file
        """
        if tag == 1:
            btn = self.BTN_ADDFILES
            window = self.DLG_ADD_FILES
        elif tag == 0:
            btn = self.BTN_ADDFOLDER
            window = self.DLG_ADD_A_FOLDER
        else:
            raise ldtp.LdtpExecutionError, "Wrong file tag given"

        win_name = 'frm' + self.ARCH_NAME
        archive = ooldtp.context(win_name)
        archive.getchild(btn).click()

        ldtp.waittillguiexist(window)
        add = ooldtp.context(window)
        """
        Add file/folder to the archive file
        """
        while add.getchild(self.TBTN_TYPE_A_FILE_NAME).press():
            if ldtp.hasstate(window, self.TXT_LOCATION, 'SHOWING'):
                break
        else:
            raise ldtp.LdtpExecutionError, "Failed to toggle the " + window + " dialog Location button"

        if tag == 0:
            while add.getchild(self.TBTN_FILESYSTEMROOT).verifytoggled() == 0:
                add.getchild(self.TBTN_FILESYSTEMROOT).click()
        add.settextvalue(self.TXT_LOCATION,src_path)
        add.enterstring(self.TXT_LOCATION,'<enter>')
        ldtp.waittillguinotexist(window)
        """
        Verify filed added
        """
        if archive.getchild(self.MNU_LASTOUTPUT).hasstate('enabled'):
            archive.getchild(self.MNU_LASTOUTPUT).selectmenuitem()
            ldtp.waittillguiexist(self.DLG_LASTOUTPUT)
            output = ooldtp.context(self.DLG_LASTOUTPUT)
            if output.getchild(self.TXT_0).gettextvalue() == None:
                raise ldtp.LdtpExecutionError, "None file was added!"
            else:
                output.getchild(self.BTN_CLOSE).click()
        else:
            raise ldtp.LdtpExecutionError, "Nothing added, last output menu is not enabled!"



    def open_archive(self, file_path):
        """
        To test open the archive file and extract files to /tmp folder

        @type file_path: char
        @param file_path: the archive file path
        """
        archive = ooldtp.context(self.WINDOW)
        archive.getchild(self.BTN_OPEN).click()
        ldtp.waittillguiexist(self.DLG_OPEN)
        open_dlg = ooldtp.context(self.DLG_OPEN)
        while open_dlg.getchild(self.TBTN_TYPE_A_FILE_NAME).press():
            if ldtp.hasstate(self.DLG_OPEN, self.TXT_LOCATION, 'SHOWING'):
                break
        else:
            raise ldtp.LdtpExecutionError, "Failed to toggle the " + self.DLG_OPEN + " dialog Location button"
        open_dlg.settextvalue(self.TXT_LOCATION,file_path)
        open_dlg.enterstring(self.TXT_LOCATION, '<enter>')
        ldtp.waittillguinotexist(self.DLG_OPEN)

        win_name = 'frm' + self.FILE_NAME + '*'
        ldtp.waittillguiexist(win_name)
        archive = ooldtp.context(win_name)
        archive.getchild(self.BTN_EXTRACT).click()
        ldtp.waittillguiexist(self.DLG_EXTRACT)
        extract = ooldtp.context(self.DLG_EXTRACT)
        while extract.getchild(self.TBTN_TYPE_A_FILE_NAME).press():
            if ldtp.hasstate(self.DLG_EXTRACT, self.TXT_LOCATION, 'SHOWING'):
                break
        else:
            raise ldtp.LdtpExecutionError, "Failed to toggle the " + self.DLG_EXTRACT + " dialog Location button"
        extract.settextvalue(self.TXT_LOCATION,self.EXTRACT_PATH)
        extract.enterstring(self.TXT_LOCATION, '<enter>')
        ldtp.waittillguinotexist(self.DLG_EXTRACT)

        ldtp.waittillguiexist(self.DLG_EXTRACTING_FILES_FROM_ARCHIVE)
        finish = ooldtp.context(self.DLG_EXTRACTING_FILES_FROM_ARCHIVE)
        if finish.getchild(self.LBL_EXTRACTION).hasstate('SHOWING') != 1:
            raise ldtp.LdtpExecutionError, "Failed to extract the archive file"
        finish.getchild(self.BTN_CLOSE).click()
        ldtp.waittillguinotexist(self.DLG_EXTRACTING_FILES_FROM_ARCHIVE)
        """
        Verify the extract action does have outputs
        """
        if archive.getchild(self.MNU_LASTOUTPUT).hasstate('enabled'):
            archive.getchild(self.MNU_LASTOUTPUT).selectmenuitem()
            ldtp.waittillguiexist(self.DLG_LASTOUTPUT) 
            output = ooldtp.context(self.DLG_LASTOUTPUT)
            if output.getchild(self.TXT_0).gettextvalue() == None:
                raise ldtp.LdtpExecutionError, "Last output is none!"
            else:
                output.getchild(self.BTN_CLOSE).click()
        else:
            raise ldtp.LdtpExecutionError, "Nothing output after extraction!"
            

