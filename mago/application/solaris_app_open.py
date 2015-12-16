
"""
This is the "solaris app open" module. It's in soalris/mago/application/

The solaris menu module provides wrappers for LDTP to make the write of Solaris tests easier. 
"""
import ldtp , ooldtp
import re

from .main import Application

class SolarisAppOpen(Application):
    def __init__(self):
        Application.__init__(self)

    def open_app(self, app_launchname):
        """
        Given an application, it tries to open it
        """
        self._enable_a11y(True)

        try:
            ldtp.launchapp(app_launchname)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError,"Something went wrong when opening the application"
#       print "The"+ self.name + "is open"
        self._enable_a11y(False)
        
        ldtp.wait(10) 
        response = ldtp.waittillguiexist(self.name, '', 100)
#        print app_launchname,"\n"
# 	 print ldtp.getwindowlist(),"\n"

        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."  

 
    def close_app(self, app_windowname):
        """
        It tries to close the appliation
        """
        app = ooldtp.context(app_windowname)
          
        app.closewindow()

        ldtp.wait(2)
       	
        response = ldtp.waittillguinotexist(self.name, '', 100)    
        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not closed." 

        	  
    
