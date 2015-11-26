"""
This module contains the definition of the test suite for GEdit testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_gedit import Application, GEdit

class GEditTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for GEdit
    """
    APPLICATION_FACTORY = GEdit
    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        # Exit using the Quit menu 
        gedit = ooldtp.context(self.application.name)
        quit_menu = gedit.getchild(self.application.MNU_CLOSE)
        quit_menu.selectmenuitem()

        result = ldtp.waittillguiexist(self.application.QUESTION_DLG,
                                       guiTimeOut = 2)

        if result == 1:
            question_dialog = ooldtp.context(self.application.QUESTION_DLG)
            question_dlg_btn_close = question_dialog.getchild(self.application.QUESTION_DLG_BTN_CLOSE)
            question_dlg_btn_close.click()
        
        gedit = ooldtp.context(self.application.name)
        new_menu = gedit.getchild(self.application.MNU_NEW)
        new_menu.selectmenuitem()

        result = ldtp.waittillguiexist(
            self.application.name, self.application.TXT_FIELD)
        if result != 1:
            raise ldtp.LdtpExecutionError, "Failed to set up new document."
