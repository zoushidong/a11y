PACKAGE = "mago"

#-*- coding:utf-8 -*-
"""
This is the "gnome_about_me" module for Solaris desktop.

This module provides a wrapper for LDTP to make writing Gnome_about_me tests on Solaris easier.
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


class GnomeAboutMe(Application):
    """
    gnome_about_me manages the Gnome_about_me application.
    """

    LAUNCHER = 'gnome-about-me'
    LAUNCHER_ARGS = []
    WINDOW = 'dlgAbout*'
    CLOSE_TYPE = 'button'
    CLOSE_NAME = 'btnClose'

    BTN_0 = _('btn0')
    BTN_CLOSE = _('btnClose')
    BTN_NOIMAGE = _('btnNoImage')
    BTN_OPEN = _('btnOpen')
    TBTN = _('tbtnTypeafilename')
    DLG_SELECTIMAGE = _('dlgSelectImage')
    TXT_AIM_ICHAT = _('txtAIM/iChat')
    TXT_ADDRESS = _('txtAddress')
    TXT_ADDRESS1 = _('txtAddress1')
    TXT_ASSISTANT = _('txtAssistant')
    TXT_CALENDAR = _('txtCalendar')
    TXT_CITY = _('txtCity')
    TXT_CITY1 = _('txtCity1')
    TXT_COMPANY = _('txtCompany')
    TXT_COUNTRY = _('txtCountry')
    TXT_COUNTRY1 = _('txtCountry1')
    TXT_DEPARTMENT = _('txtDepartment')
    TXT_GROUPWISE = _('txtGroupWise')
    TXT_HOME = _('txtHome')
    TXT_HOME1 = _('txtHome1')
    TXT_HOMEPAGE = _('txtHomepage')
    TXT_ICQ = _('txtICQ')
    TXT_MSN = _('txtMSN')
    TXT_MANAGER = _('txtManager')
    TXT_MOBILE = _('txtMobile')
    TXT_POBOX = _('txtPObox')
    TXT_POBOX1 = _('txtPObox1')
    TXT_PROFESSION = _('txtProfession')
    TXT_STATE_PROVINCE = _('txtState/Province')
    TXT_STATE_PROVINCE1 = _('txtState/Province1')
    TXT_TITLE = _('txtTitle')
    TXT_WEBLOG = _('txtWeblog')
    TXT_WORK = _('txtWork')
    TXT_WORK1 = _('txtWork1')
    TXT_WORKFAX = _('txtWorkfax')
    TXT_JABBER = _('txtJabber')
    TXT_YAHOO = _('txtYahoo')
    TXT_ZIP_POSTALCODE = _('txtZIP/Postalcode')
    TXT_ZIP_POSTALCODE1 = _('txtZIP/Postalcode1')
    TXT_LOCATION = _('txtLocation')
    PTAB_CONTACT = _('ptabContact')
    PTAB_ADDRESS = _('ptabAddress')
    PTAB_PERSONAL = _('ptabPersonalInfo')
    PTAB = _('ptl0')

    def select_tab(self, tab):
        if tab == 'Contact':
            tab_name = self.PTAB_CONTACT
        elif tab == 'Address':
            tab_name = self.PTAB_ADDRESS
        elif tab == 'PersonalInfo':
            tab_name = self.PTAB_PERSONAL
        else:
            raise AssertionError("Wrong tab name was given")

        about_me = ooldtp.context(self.WINDOW)
        if about_me.getchild(self.PTAB).selecttab(tab_name) != 1 :
            raise ldtp.LdtpExecutionError, "Failed to select the " + tab + " page tab!"

    def file_values(self, values):
        about_me = ooldtp.context(self.WINDOW)
	for widget, text in values.iteritems():
		textWidget = about_me.getchild(widget)
                textWidget.settextvalue(text)	

    def check_values(self, new_values):
        ldtp.waittillguiexist(self.WINDOW)
        about_me = ooldtp.context(self.WINDOW)
        
        for widget, text in new_values.iteritems():
            saved_text = about_me.gettextvalue(widget)
            if not text == saved_text:
                raise AssertionError('entered text wasn\'t saved correctly, entered: %s saved: %s' 
                                     % (text, saved_text))

    def change_picture(self, photo_path):
        about_me = ooldtp.context(self.WINDOW)
        
        about_me.getchild(self.BTN_0).click()
        
        ldtp.wait(2)

        if (ldtp.guiexist(self.DLG_SELECTIMAGE)):
            selectImage = ooldtp.context(self.DLG_SELECTIMAGE)
            while selectImage.getchild(self.TBTN).press():
                if ldtp.hasstate(self.DLG_SELECTIMAGE,self.TXT_LOCATION,'SHOWING'):
                    break
            else:
                raise ldtp.LdtpExecutionError, "Failed to toggle the Location button"
 
            selectImage.settextvalue(self.TXT_LOCATION, photo_path)
            ldtp.wait(2)
            selectImage.getchild(self.BTN_OPEN).click()
            ldtp.wait(2)
        ldtp.waittillguiexist(self.WINDOW)

    def change_picture_to_default(self):
        about_me = ooldtp.context(self.WINDOW)
        
        #set the photo to no image
        about_me.getchild(self.BTN_0).click()
        ldtp.wait(2)
        selectImage = ooldtp.context(self.DLG_SELECTIMAGE)
        selectImage.getchild(self.BTN_NOIMAGE).click()

    def clean_up_text_values(self, values):
        about_me = ooldtp.context(self.WINDOW)
        #clean up all the fields on the 
        for widget, text in values.iteritems():
            about_me.settextvalue(widget, '')
            #there's probably a bug in evolution-data-server or about-me
            #but if we don't wait to remove another field one of those might not get removed.
            ldtp.wait(1)
        ldtp.wait(3)
        
        #check that the values were cleaned, otherwise raise an error.
        for widget, text in values.iteritems():
            saved_text = about_me.gettextvalue(widget)
            if not '' == saved_text:
                raise AssertionError('the text: %s in widget: %s was not removed'
                                     % (saved_text, widget))


    def __init__(self):
        Application.__init__(self)
        self.main_window = ooldtp.context(self.WINDOW)
