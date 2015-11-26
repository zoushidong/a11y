"""
This is the "solaris menu" module.

The solaris menu module provides wrappers for LDTP to make the write of Solaris tests easier. 
"""
import ldtp , ooldtp
import re

from .main import Application

class SolarisMenu(Application):
    def open_and_check_menu_item(self, menu_item_txt):
        """
        Given a menu item, it tries to open the application associated with it.
         
        @type menu_item_txt: string
        @param menu_item_txt: The name of the menu item that the user wants to open.
        
            The naming convention is the following:
            
            E{-} Prepend 'mnu' to the menu item
            
            E{-} Append the menu item with no spaces.
                 
            Example: For the menu Disk Usage Analyzer, the menu name would be mnuDiskUsageAnalyzer.
            
        """
       
#        topPanel = ooldtp.context(self.__class__.TOP_PANEL)
        topPanel = ooldtp.context('frmTopExpandedEdgePanel')
        
        try:
            actualMenu = topPanel.getchild(menu_item_txt)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The " + menu_item_txt + " menu was not found. " 
      
        actualMenu.selectmenuitem()
        response = ldtp.waittillguiexist(self.name, '', 50)
        
        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."    

 
