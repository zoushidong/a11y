"""
This is the "firefox" module.

The firefox module provides wrappers for LDTP to make writing firefox test cases easier.
"""

import ooldtp
import ldtp
from ..main import Application
from ...gconfwrapper import GConf
from .ff_event_listener import *
import time
import os


class Firefox(Application):
    """
    The Firefox class contains methods for exercising the firefox application
    """
    LAUNCHER             = "firefox"
    LAUNCHER_ARGS        = ["-P"]
    WINDOW               = "frm*MozillaFirefox"
    CLOSE_TYPE           = "menu"
    CLOSE_NAME           = "mnuQuit"

    def __init__(self):
        Application.__init__(self)

    def open_link(self, site_url):
	"""
	Open the given site url in firefox.
	"""
        BUTTON = ["btnGototheaddressintheLocationBar", "btnLocation1"]
        URL_TXT_FIELD = "txtSearchBookmarksandHistory"
	
	firefox = ooldtp.context(self.name)

	try:
            firefox.activatetext(URL_TXT_FIELD)
	    firefox.mouseleftclick(URL_TXT_FIELD)
	    firefox.settextvalue(URL_TXT_FIELD, site_url)
	    for btn in BUTTON:
		if firefox.objectexist(btn) == 1 and firefox.hasstate(btn, ldtp.state.ENABLED) == 1:
 	            if firefox.mouseleftclick(btn) and event_listener('document','document:load-complete'):
			pass
		    else:
	                raise ldtp.LdtpExecutionError, "Failed to open the given site url in firefox"
	except ldtp.LdtpExecutionError:
           raise ldtp.LdtpExecutionError, "Failed to activate firefox url entry"

    
    def open(self):
        """
	Open the firefox with a new profile.
	"""
	Application.set_name(self,'dlgFirefox-ChooseUserProfile')
        Application.open(self)

	"""
	To create a new profile before testing
	"""

	"""
	clicking Create Profile button in Choose User Profile dialog
	"""
	response = ldtp.waittillguiexist(self.name,'',20)
	if response == 1:
	    try:
                ldtp.mouseleftclick(self.name,'*btnCreateProfile*')
	    except ldtp.LdtpExecutionError:
	        raise ldtp.LdtpExecutionError, "Failed to click Create New Profile button"

            """
	    clicking Next button in Create Profile Wizard dialog
	    """
    
            Application.set_name(self,'dlgCreateProfileWizard')
	    resps = ldtp.waittillguiexist(self.name,'',20)
	    if resps == 1:
	        try:
		    ldtp.mouseleftclick(self.name,'btnNext')
	        except ldtp.LdtpExecutionError:
	            raise ldtp.LdtpExecutionError, "Failed to click Next button"

                """
	        Create new profile with profile name ff_testing
	        """
	        ldtp.remap(self.name)
		try:
                    ldtp.settextvalue(self.name,'txt0','ff_testing')
                    ldtp.mouseleftclick(self.name, 'btnFinish')
                except ldtp.LdtpExecutionError:
	            raise ldtp.LdtpExecutionError, "Failed to set profile name and click Finish button"

         	"""
	        Start firefox with new create profile
	        """
	        Application.set_name(self,'dlgFirefox-ChooseUserProfile')
		rsps = ldtp.waittillguiexist(self.name,'',20)
		if rsps == 1:
		    try:
			ldtp.mouseleftclick(self.name, 'ff_testing')
		        ldtp.mouseleftclick(self.name, 'btnStartFirefox')
	            except ldtp.LdtpExecutionError:
	                raise ldtp.LdtpExecutionError, "Failed to click ff_testing profile or start firefox button"
        
	            Application.set_name(self,'frm*MozillaFirefox')
	            responseresult = ldtp.waittillguiexist(self.name, '', 20)

	            if responseresult ==  0:
	                raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."
		else:
		    raise ldtp.LdtpExecutionError, "Failed to quit profile create wizard window with clicking Finish button"
	    else:
		raise ldtp.LdtpExecutionError, "Failed to start profile create wizard window"
	else:
	    raise ldtp.LdtpExecutionError, "firefox -P failed to bring Firefox profile dialog up"

    def cl_profile(self):
	"""
	It cleans up the profile created when open a new firefox window.
	"""
        """
	Start the firefox with "-P" profile manager, choose the ff_testing profile and destroy it
	"""
	Application.set_name(self,'dlgFirefox-ChooseUserProfile')
	Application.open(self)

        response = ldtp.waittillguiexist(self.name,'',20)
	if response == 1:
	    try:
	        ldtp.mouseleftclick(self.name,'ff_testing')
		ldtp.mouseleftclick(self.name,'*btnDeleteProfile*')
            except ldtp.LdtpExecutionError:
	        raise ldtp.LdtpExecutionError, "Failed to select the ff_testing profile or failed to click delete button"
        
        
	    Application.set_name(self,'dlgDeleteProfile')
	    resp = ldtp.waittillguiexist(self.name,'',20)
	    if resp == 1:
		try:
		    ldtp.mouseleftclick(self.name,'btnDeleteFiles')
	        except ldtp.LdtpExecutionError:
	            raise ldtp.LdtpExecutionError, "Failed to click Delete Files button"

	        Application.set_name(self,'dlgFirefox-ChooseUserProfile')
	        rsps = ldtp.waittillguiexist(self.name,'',20)
		if rsps == 1:
		    try:
		        ldtp.mouseleftclick(self.name,'btnExit')
	            except ldtp.LdtpExecutionError:
	                raise ldtp.LdtpExecutionError, "Failed to exit the firefox choose user profile dialog"
		else:
		    raise ldtp.LdtpExecutionError, "Cannot dismiss delete profile dialog"
	    else:
		raise ldtp.LdtpExecutionError, "delete profile dialog cannot be start up by clicking delete profile button"
	else:
	    raise ldtp.LdtpExecutionError, "could not start firefox profile manager dialog"
    
    def load_cmplt(self):
	"""
	Catch the event "document:load-complete" to verify the firefox finishes the page loading.
	"""
        load_result = False 
	load_result = event_listener('document','document:load-complete')
	return load_result

    def open_tab(self):
	"""
	To open a new tab in current active firefox window
	"""
        MNU_NEW_TAB = "mnuNewTab"
	firefox = ooldtp.context(self.name)
	tab_count = firefox.gettabcount('ptl0')

	try:
       	    if firefox.selectmenuitem(MNU_NEW_TAB):
		tab_count_new = firefox.gettabcount('ptl0')
		if (tab_count_new - tab_count) == 1 and firefox.gettabname('ptl0',tab_count_new-3) == '(Untitled)':
		    pass
	        else:
		    raise ldtp.LdtpExecutionError, "Failed to open a new blank tab"
	except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to select the New Tab menu item"


    def close_tab(self,tab_to_close):
	"""
	To close a preferred tab in active firefox window
	"""
        MNU_CLOSE_TAB = "mnuCloseTab"
	firefox = ooldtp.context(self.name)
        tab_count = firefox.gettabcount('ptl0') 

	try:
            if firefox.selecttab('ptl0',tab_to_close) == 1:
		try:
	       	    firefox.selectmenuitem(MNU_CLOSE_TAB)
		    tab_count_new = firefox.gettabcount('ptl0')
		    if (tab_count - tab_count_new) == 1:
			pass
		    else:
			raise ldtp.LdtpExecutionError, "Something goes wrong when closing the tab"
		except ldtp.LdtpExecutionError:
		    raise ldtp.LdtpExecutionError, "Failed to select Close Tab menu item"
	except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to select the tab to be closed"


    def close(self):
	"""
	To quit the firefox main window
	"""
        try:
            firefox = ooldtp.context(self.name)
            try:
                close_widget = firefox.getchild(self.close_name)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The " + self.close_name + " widget was not found."

            if self.close_type == 'menu':
                close_widget.selectmenuitem()
            elif self.close_type == 'button':
                close_widget.mouseleftclick()
            else:
                raise ldtp.LdtpExecutionError, "Wrong close item type."
            """
	    If there are several tabs opening, the Quit Firefox dialog will be popup
	    To make sure the firefox could be closed as expected, btnQuit should be clicked
	    """
            ldtp.wait()
            if ldtp.guiexist('dlgQuitFirefox') == 1:
		try:
		    ldtp.mouseleftclick('dlgQuitFirefox','btnQuit')
		except ldtp.LdtpExecutionError:
		    raise ldtp.LdtpExecutionError, "Could not click the Quit button in Quit Firefox dialog"
            
            response = ldtp.waittillguinotexist(self.name, '', 20)
            if response == 0:
                raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application."
        except ldtp.LdtpExecutionError, msg:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application: " + str(msg)

    def refresh(self):
        """
	To refresh the current loaded page in firefox window
	"""
	firefox = ooldtp.context(self.name)
	refresh_btn = firefox.getchild('Reload','push button')
	for btn in refresh_btn:
	    btnName = btn.getName()
	    if firefox.hasstate(btnName, ldtp.state.ENABLED):
		refresh = btnName
		firefox.mouseleftclick(refresh)
	    else:
		continue



    def actions(self, action):
	"""
	To perform the action buttons in firefox toolbar, including Back, Forward, Reload, Stop and Home.
	"""
	firefox = ooldtp.context(self.name)

        if action == 'Reload':
	    try:
	        action_widget = firefox.getchild(action,'push button')
		for btn in action_widget:
		    btnName = btn.getName()
		    if firefox.hasstate(btnName,ldtp.state.ENABLED):
			act_btn = btnName
			if firefox.mouseleftclick(act_btn) and \
		           event_listener('document','document:reload') and \
		           event_listener('document','document:load-complete'):
                            pass
	                else:
                            raise ldtp.LdtpExecutionError, "Failed to finish Reload action"
	    except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "Failed to click the Reload button"
	elif action == 'Stop':
	    try:
                action_widget = firefox.getchild(action, 'push button')
		for btn in action_widget:
		    btnName = btn.getName()
		    if firefox.hasstate(btnName, ldtp.state.ENABLED):
			act_btn = btnName
			if firefox.mouseleftclick(act_btn) and \
		           event_listener('document','document:load-stopped'):
			    pass
		        else:
			    raise ldtp.LdtpExecutionError, "Failed to finish Stop action"
	    except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "Failed to click the Stop button"
	else:
	    try:
                action_widget = firefox.getchild(action, 'push button')
		for btn in action_widget:
	            btnName = btn.getName()
		    if firefox.hasstate(btnName, ldtp.state.ENABLED):
			act_btn = btnName
			if firefox.mouseleftclick(act_btn):
			    pass
		        else:
		            raise ldtp.LdtpExecutionError, "Failed to finish " + action + " action"
	    except ldtp.LdtpExecutionError:
		raise ldtp.LdtpExecutionError, "Failed to click the action " + action + " button"

    def chgHome(self, home_page):
	"""
	To change the home page to home_page for firefox.
	"""

	firefox = ooldtp.context(self.name)

	try:
	    if firefox.selectmenuitem('mnuPreferences') == 1:
	        Application.set_name(self,'frmFirefoxPreferences')
		response = ldtp.waittillguiexist(self.name, '', 20)
		if response == 1:
		    ffPref = ooldtp.context(self.name)

		    try:
			listtab = ['lstGeneral','lstMain']
			listid = 'lstMain'
			for item in listtab:
			    if ffPref.hasstate(item, ldtp.state.SHOWING) == 1:
				listid = item
			    else:
			        continue
			ffPref.mouseleftclick(listid)
			ffPref.settextvalue('txtHomePage',home_page)
			ffPref.mouseleftclick('btnClose')
	                Application.set_name(self,'frm*MozillaFirefox')
		    except ldtp.LdtpExecutionError:
			raise ldtp.LdtpExecutionError, "Failed to set new homepage in firefox preferences main tab."
		else:
		    raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."
	except ldtp.LdtpExecutioinError:
            raise ldtp.LdtpExecutionError, "Failed to open the Firefox Preferences window."


    def rstHome(self):
	"""
	To restore the default firefox home page
	"""

	firefox = ooldtp.context(self.name)

	try:
            if firefox.selectmenuitem('mnuPreferences') == 1:
		Application.set_name(self, 'frmFirefoxPreferences')
		response = ldtp.waittillguiexist(self.name,'',20)
		if response == 1:
		    ffPref = ooldtp.context(self.name)

		    try:
			listtab = ['lstGeneral','lstMain']
			listid = 'lstMain'
			for item in listtab:
			    if ffPref.hasstate(item, ldtp.state.SHOWING) == 1:
				listid = item
			    else:
				continue
			ffPref.mouseleftclick(listid)
			ffPref.mouseleftclick('btnRestoretoDefault')
			ffPref.mouseleftclick('btnClose')
	                Application.set_name(self,'frm*MozillaFirefox')
		    except ldtp.LdtpExecutionError:
			raise ldtp.LdtpExecutionError, "Failed to restore to default home page"
		else:
		    raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."
	except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to open the Firefox Preferences window."


    def getTitle(self, tab_index):
	"""
	To get the specified tab_index firefox tab title. tab_index >= 1.
	"""

	firefox = ooldtp.context(self.name)
	index = tab_index - 1

	try:
	    title = firefox.gettabname('ptl0', index)
	    return title
        except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to get the specified No." + tab_index + " tab name."
