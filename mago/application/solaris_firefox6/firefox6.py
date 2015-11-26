PACKAGE = "mago"

#-*- coding:utf-8 -*-
"""
This is the "firefox" module for firefox6 on Solaris.

The firefox6 module provides wrappers for LDTP to make writing firefox test cases easier.
"""

import ooldtp
import ldtp
from ..main import Application
from ...gconfwrapper import GConf
from ..solaris_firefox3.ff_event_listener import *
from ...cmd import globals
import time
import os
import gettext

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext


class Firefox(Application):
    """
    The Firefox class contains methods for exercising the firefox application
    """
    LAUNCHER             = "firefox"
    LAUNCHER_ARGS        = ["-new-window"]
    WINDOW               = "frm*MozillaFirefox"
    CLOSE_TYPE           = "menu"
    CLOSE_NAME           = _("mnuQuit")

    BTN_CLOSE = _("btnClose")
    BTN_RESTORETODEFAULT = _("btnRestoretoDefault")
    BTN_CLOSETABS = _("btnClosetabs")
    BTN_BACK = _("btnBack")
    BTN_FORWARD = _("btnForward")
    BTN_HOME = _("btnHome")
    BTN_SEARCH_ENG = _("btnSearch")
    BTN_SEARCH = _("btnSearch1")
    MNU_PREFERENCES = _("mnuPreferences")
    MNU_NEW_TAB = _("mnuNewTab")
    MNU_GOOGLE = _("mnuGoogle")
    MNU_YAHOO = _("mnuYahoo")
    MNU_BING = _("mnuBing")
    MNU_AMAZONCOM = _("mnuAmazoncom")
    MNU_EBAY = _("mnueBay")
    MNU_TWITTER = _("mnuTwitter")
    MNU_WIKIPEDIA = _("mnuWikipedia(en)")
    DLG_PREFERENCES = _("dlgFirefoxPreferences")
    DLG_CONFIRMCLOSE = _("dlgConfirmclose")
    PTAB = _("ptl0")
    LST_GENERAL = _("lstGeneral")
    LST_MAIN = _("lstMain")
    TXT_HOMEPAGE = _("txtHomePage")
    TXT_SEARCH = _("txtSearchusing")

    SEARCH = {"Google"   :  { "NAME": "Google",
                              "MENU": MNU_GOOGLE},
              "Yahoo"    :  { "NAME": "Yahoo",
                              "MENU": MNU_YAHOO},
              "Bing"     :  { "NAME": "Bing",
                              "MENU": MNU_BING},
              "Amazon"   :  { "NAME": "Amazoncom",
                              "MENU": MNU_AMAZONCOM},
              "eBay"     :  { "NAME": "eBay",
                              "MENU": MNU_EBAY},
              "Twitter"  :  { "NAME": "Twitter",
                              "MENU": MNU_TWITTER},
              "Wikipedia":  { "NAME": "Wikipedia(en)",
                              "MENU": MNU_WIKIPEDIA}}



    def __init__(self):
        Application.__init__(self)

    
    def open_with_url(self, site_url):
        """
        It starts firefox with prefered site_url in a new firefox window.
        """
        while ldtp.guiexist(self.name):
            ldtp.activatewindow(self.name)
            self.close()

        if site_url is not None:
            self.LAUNCHER_ARGS.append(site_url)

        self._enable_a11y(True)
        ldtp.launchapp(self.LAUNCHER, args=self.LAUNCHER_ARGS)
        self._enable_a11y(False)

        response = ldtp.waittillguiexist(self.name, '', 50)

        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."
            

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
	firefox = ooldtp.context(self.name)
	tab_count = firefox.gettabcount(self.PTAB)

	try:
       	    if firefox.selectmenuitem(self.MNU_NEW_TAB):
		tab_count_new = firefox.gettabcount(self.PTAB)
		if (tab_count_new - tab_count) == 1 and firefox.gettabname(self.PTAB,tab_count_new-2) == 'New Tab':
		    pass
	        else:
		    raise ldtp.LdtpExecutionError, "Failed to open a new blank tab"
	except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to select the New Tab menu item"


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
	    If there are several tabs opening, the Confirm close dialog will be popup
	    To make sure the firefox could be closed as expected, btnClosetabs should be clicked
	    """
            ldtp.wait()
            if ldtp.guiexist(self.DLG_CONFIRMCLOSE) == 1:
		try:
		    ldtp.mouseleftclick(self.DLG_CONFIRMCLOSE,self.BTN_CLOSETABS)
		except ldtp.LdtpExecutionError:
		    raise ldtp.LdtpExecutionError, "Could not click the Close tabs button in Quit Firefox dialog"
            
            response = ldtp.waittillguinotexist(self.name, '', 50)
            if response == 0:
                raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application."
        except ldtp.LdtpExecutionError, msg:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application: " + str(msg)


    def actions(self, action):
	"""
	To perform the action buttons in firefox toolbar, including Back, Forward, and Home.
        Stop, Reload actions were absent for the buttons have been removed from toolbar.
	"""
	firefox = ooldtp.context(self.name)

        if action == 'Back':
            action_widget = self.BTN_BACK
        elif action == 'Forward':
            action_widget = self.BTN_FORWARD
        elif action == 'Home':
            action_widget = self.BTN_HOME
        else:
            raise ldtp.LdtpExecutionError, "Incorrect action, please choose one action from Back, Forward and Home only."

        if firefox.getchild(action_widget).hasstate('ENABLED'):
            firefox.click(action_widget)
        else:
            raise ldtp.LdtpExecutionError, "The " + action + " button is not clickable/accessible"
	

    def chgHome(self, home_page):
	"""
	To change the home page to home_page for firefox.
	"""

	firefox = ooldtp.context(self.name)

	try:
	    if firefox.selectmenuitem(self.MNU_PREFERENCES) == 1:
	        Application.set_name(self,self.DLG_PREFERENCES)
		response = ldtp.waittillguiexist(self.name, '', 20)
		if response == 1:
		    ffPref = ooldtp.context(self.name)

		    try:
			listtab = [self.LST_GENERAL,self.LST_MAIN]
			listid = self.LST_MAIN
			for item in listtab:
			    if ffPref.hasstate(item, ldtp.state.SHOWING) == 1:
				listid = item
			    else:
			        continue
			ffPref.mouseleftclick(listid)
			ffPref.settextvalue(self.TXT_HOMEPAGE,home_page)
			ffPref.click(self.BTN_CLOSE)
	                Application.set_name(self,self.WINDOW)
		    except ldtp.LdtpExecutionError:
			raise ldtp.LdtpExecutionError, "Failed to set new homepage in firefox preferences main tab."
		else:
		    raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."
	except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Failed to open the Firefox Preferences window."


    def rstHome(self):
	"""
	To restore the default firefox home page
	"""

	firefox = ooldtp.context(self.name)

	try:
            if firefox.selectmenuitem(self.MNU_PREFERENCES) == 1:
		Application.set_name(self, self.DLG_PREFERENCES)
		response = ldtp.waittillguiexist(self.name,'',20)
		if response == 1:
		    ffPref = ooldtp.context(self.name)

		    try:
			listtab = [self.LST_GENERAL,self.LST_MAIN]
			listid = self.LST_MAIN
			for item in listtab:
			    if ffPref.hasstate(item, ldtp.state.SHOWING) == 1:
				listid = item
			    else:
				continue
			ffPref.mouseleftclick(listid)
			ffPref.click(self.BTN_RESTORETODEFAULT)
			ffPref.click(self.BTN_CLOSE)
	                Application.set_name(self,self.WINDOW)
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
	    title = firefox.gettabname(self.PTAB, index)
	    return title
        except ldtp.LdtpExecutionError:
	    raise ldtp.LdtpExecutionError, "Failed to get the specified No." + tab_index + " tab name."

    def search(self, search_eng, search_cont):
        """
        To search search_cont with selected search_eng within firefox
        """
        firefox = ooldtp.context(self.name)
        SearchResult = False

        if firefox.click(self.BTN_SEARCH_ENG) == 1:
            try:
                firefox.selectmenuitem(self.SEARCH[search_eng]["MENU"])
                SearchEntry = self.TXT_SEARCH + self.SEARCH[search_eng]["NAME"]
                firefox.settextvalue(SearchEntry, search_cont)
                firefox.click(self.BTN_SEARCH)
                if event_listener('document','document:load-complete'):
                    tab_num = firefox.gettabcount(self.PTAB) - 1
                    tab_title = []
                    for i in range(0, tab_num):
                        tab_title.append(firefox.gettabname(self.PTAB, i))

                    for n in range(len(tab_title)):
                        if tab_title[n].__contains__(search_eng) and tab_title[n].__contains__(search_cont):
                            SearchResult = True

                    if SearchResult == True:
                        pass
                    else:
                        raise ldtp.LdtpExecutionError, "Failed to get the " + search_eng + " search result in firefox."
                else:
                    raise ldtp.LdtpExecutionError, "Can't finish " + search_eng + " search result loading"
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "Failed to set the " + search_eng + " search engine in firefox search entry!"
        else:
            raise ldtp.LdtpExecutionError, "Failed to expand firefox search engine menu"

    def get_tab_count(self):
        """
        To get current firefox tab count
        """
        firefox = ooldtp.context(self.name)
        return firefox.gettabcount(self.PTAB)
