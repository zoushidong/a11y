PACKAGE = "mago"

"""
main module contains the definition of the main Application class
that is used to wrap applications functionality
"""
import ldtp, ooldtp
import os
from ..cmd import globals
import gettext

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext

class Application:
    """
    Superclass for the rest of the applications

    Constants that should be defined in the classes that inherit from this class
    LAUNCHER: Command to launching the application through ldtp.launchapp
    LAUNCHER_ARGS: Arguments to pass when launching the application through
                   ldtp.launchapp.
    WINDOW: Top application frame pattern using ldtp syntax
    CLOSE_TYPE: Close object type (one of 'menu' or 'button')
    CLOSE_NAME: Close object name
    """
    CLOSE_TYPE = 'menu'
    CLOSE_NAME = _('mnuQuit')
    LAUNCHER_ARGS = []
    WINDOW     = ''
    TOP_PANEL = _('frmTopExpandedEdgePanel')


    def __init__(self, name = None, close_type= None, close_name= None):
        """
        @type close_type: string
        @param close_type: The type of close widget of the application. Types: menu, button.
        @type close_name: string
        @param close_name: The name of the close widget of the application. If not mentioned the default will be used ("Quit")
        """
        if name:
            self.name = name
        else:
            self.name = self.WINDOW

        if close_type:
            self.close_type = close_type
        else:
            self.close_type = self.CLOSE_TYPE

        if close_name:
            self.close_name = close_name
        else:
            self.close_name = self.CLOSE_NAME


    def set_name(self, name):
        if name is not None:
            self.name = name

    def set_close_type(self, close_type):
        if close_type is not None:
            self.close_type = close_type

    def set_close_name(self, close_name):
        if close_name is not None:
            self.close_name = close_name

    def remap(self):
        """
        It reloads the application map for the given ooldtp.context.
        """
        ldtp.remap(self.name)

    def open(self):
        """
        Given an application, it tries to open it.
        """
        self._enable_a11y(True)
        ldtp.launchapp(self.LAUNCHER, args=self.LAUNCHER_ARGS)
        self._enable_a11y(False)

        ldtp.wait(2)
        response = ldtp.waittillguiexist(self.name, '', 20)

        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."

    def is_opened(self):
        """
        Returns 1, if the application is opened. 0, otherwise
        """
        return ldtp.guiexist(self.name)

    def close(self):
        """
        Given an application, it tries to close it.
        """
        app = ooldtp.context(self.name)
        close_widget = app.getchild(self.close_name)
        ldtp.wait(5)
        if self.close_type == 'menu':
            close_widget.selectmenuitem()
        elif self.close_type == 'button':
            close_widget.click()
        else:
            raise ldtp.LdtpExecutionError, "Wrong close item type."
        
        response = ldtp.waittillguinotexist(self.name, '', 20)
        if response == 0:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application."
        ldtp.wait(2)

    def save(self, save_menu=_('mnuSave')):
        """
        Given an application, it tries to save the current document.
        This method gives very basic functionality. Please, override this method in the subclasses for error checking.

        @type save_menu: string
        @param save_menu: The name of the Save menu of the application. If not mentioned the default will be used ("Save").
        """
        app = ooldtp.context(self.name)
        actualMenu = app.getchild(save_menu)

        actualMenu.selectmenuitem()

    def write_text(self, text, txt_field=''):
        """
        Given an application it tries to write text to its current buffer.
        """
        app = ooldtp.context(self.name)

        if txt_field == '':
            ldtp.enterstring(text)
        else:
            app_txt_fields = app.getchild(txt_field, "text")
            for field in app_txt_fields:
                field.settextvalue(text)

    def _enable_a11y(self, enable):
        os.environ['NO_GAIL'] = str(int(not enable))
        os.environ['NO_AT_BRIDGE'] = str(int(not enable))
