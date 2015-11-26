PACKAGE = "mago"

#-*- coding:utf-8 -*-
"""
This is the "gnome-appearance-properties" test module for Solaris Desktop.

This module provides a wrapper for LDTP to make writing Gnome Appearance Properties tests easier.
"""
import ooldtp
import ldtp
import os
from .main import Application
from ..gconfwrapper import GConf
from ..cmd import globals
import time
import gettext
import platform

gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext

class SolarisAppearance(Application):
    """
    gnome_appearance_properties manages the Solaris Gnome Appearance Properties application.
    """

    LAUNCHER = 'gnome-appearance-properties'
    LAUNCHER_ARGS = []
    WINDOW = 'dlgAppearancePreferences'
    CLOSE_TYPE = 'button'
    CLOSE_NAME = _('btnClose')

    BTN_5 = _('btn5')
    BTN_6 = _('btn6')
    BTN_ADD = _('btnAdd')
    BTN_APPLICATIONFONT = _('btnApplicationfont')
    BTN_CLOSE = _('btnClose')
    BTN_CUSTOMIZE = _('btnCustomize')
    BTN_DELETE = _('btnDelete')
    BTN_DESKTOPFONT = _('btnDesktopfont')
    BTN_DETAILS = _('btnDetails')
    BTN_DOCUMENTFONT = _('btnDocumentfont')
    BTN_FIXEDWIDTHFONT = _('btnFixedwidthfont')
    BTN_GETMOREBACKGROUNDSONLINE = _('btnGetmorebackgroundsonline')
    BTN_GETMORETHEMESONLINE = _('btnGetmorethemesonline')
    BTN_HELP = _('btnHelp')
    BTN_INSTALL = _('btnInstall')
    BTN_PREFERENCES = _('btnPreferences')
    BTN_REMOVE = _('btnRemove')
    BTN_SAVEAS = _('btnSaveAs')
    BTN_WINDOWTITLEFONT = _('btnWindowtitlefont')
    BTN_OK = _('btnOK')
    BTN_OPEN = _('btnOpen')
    TBTN = _('tbtnTypeafilename')
    DLG_CUSTOMIZETHEME = _('dlgCustomizeTheme')
    DLG_ADDWALLPAPER = _('dlgAddWallpaper')
    DLG_PICKAFONT = _('dlgPickaFont')
    MNU_CENTER = _('mnuCenter')
    MNU_HORIZONTALGRADIENT = _('mnuHorizontalgradient')
    MNU_SCALE = _('mnuScale')
    MNU_SOLIDCOLOR = _('mnuSolidcolor')
    MNU_SPAN = _('mnuSpan')
    MNU_STRETCH = _('mnuStretch')
    MNU_TILE = _('mnuTile')
    MNU_VERTICALGRADIENT = _('mnuVerticalgradient')
    MNU_ZOOM = _('mnuZoom')
    TXT_LOCATION = _('txtLocation')
    TBL_CONTROLS = _('tbl0')
    TBL_WINDOWBORDER = _('tbl1')
    TBL_ICONS = _('tbl2')
    TBL_POINTER = _('tbl3')
    TBL_FAMILY = _('tblFamily')
    TBL_STYLE = _('tblStyle')
    TBL_SIZE = _('tblSize')
    PTAB_THEME = _('ptabTheme')
    PTAB_BACKGROUND = _('ptabBackground')
    PTAB_FONTS = _('ptabFonts')
    PTAB_CONTROLS = _('ptabControls')
    PTAB_WINDOWBORDER = _('ptabWindowBorder')
    PTAB_ICONS = _('ptabIcons')
    PTAB_POINTER = _('ptabPointer')
    PTABLE = _('ptl0')
    LP = _('pane1')
    APP_FAMILY = _('Clean')
    APP_STYLE = _('Italic')
    APP_SIZE = _('8')
    DOC_FAMILY = _('Newspaper')
    DOC_STYLE = _('Bold')
    DOC_SIZE = _('22')
    DT_FAMILY = _('Serif')
    DT_STYLE = _('Bold Italic')
    DT_SIZE = _('6')
    WIN_FAMILY = _('Monospace')
    WIN_STYLE = _('Regular')
    WIN_SIZE = _('28')
    FXD_FAMILY = _('Times')
    FXD_STYLE = _('Regular')
    FXD_SIZE = _('16')

    Default = '/usr/share/pixmaps/backgrounds/opensolaris/grid-blue.jpg'
    
    
    APPEARANCE_TABS = {"CONTROLS"       : {"TAB": PTAB_CONTROLS,
                                           "TABLE": TBL_CONTROLS},
                       "WINDOWBORDER"   : {"TAB": PTAB_WINDOWBORDER,
                                           "TABLE": TBL_WINDOWBORDER},
                       "ICONS"          : {"TAB": PTAB_ICONS,
                                           "TABLE": TBL_ICONS},
                       "POINTER"        : {"TAB": PTAB_POINTER,
                                           "TABLE": TBL_POINTER}}

    FONTS = {"APPLICATION"     : {"BTN"    : BTN_APPLICATIONFONT,
                                  "FAMILY" : APP_FAMILY,
                                  "STYLE"  : APP_STYLE,
                                  "SIZE"   : APP_SIZE},
            "DOCUMENT"         : {"BTN"    : BTN_DOCUMENTFONT,
                                  "FAMILY" : DOC_FAMILY,
                                  "STYLE"  : DOC_STYLE,
                                  "SIZE"   : DOC_SIZE},
            "DESKTOP"          : {"BTN"    : BTN_DESKTOPFONT,
                                  "FAMILY" : DT_FAMILY,
                                  "STYLE"  : DT_STYLE,
                                  "SIZE"   : DT_SIZE},
            "WINDOWTITLE"      : {"BTN"    : BTN_WINDOWTITLEFONT,
                                  "FAMILY" : WIN_FAMILY,
                                  "STYLE"  : WIN_STYLE,
                                  "SIZE"   : WIN_SIZE},
            "FIXEDWIDTH"       : {"BTN"    : BTN_FIXEDWIDTHFONT,
                                  "FAMILY" : FXD_FAMILY,
                                  "STYLE"  : FXD_STYLE,
                                  "SIZE"   : FXD_SIZE}}


    def change_appearance(self, tab):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_THEME)
        appearance.getchild(self.BTN_CUSTOMIZE).click()
        
        customizeTheme = ooldtp.context(self.DLG_CUSTOMIZETHEME)
        customizeTheme.getchild(self.PTABLE).selecttab(self.APPEARANCE_TABS[tab]["TAB"])
        self.change_elements(customizeTheme, self.APPEARANCE_TABS[tab]["TABLE"])
        
        customizeTheme.getchild(self.BTN_CLOSE).click()
        ldtp.waittillguiexist(self.name)
    
    def change_elements(self, dialog, table):
        row_count = dialog.getrowcount(table)
        row = 0
        while row < row_count:
            dialog.getcellvalue(table, row, 1)
            ldtp.wait(2)
            row+=1

    def change_background(self, background_path):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_BACKGROUND)
        appearance.remap()
        num = len(appearance.getchild(self.LP).getobjectproperty('children').split(' '))
        appearance.getchild(self.BTN_ADD).click()

        ldtp.waittillguiexist(self.DLG_ADDWALLPAPER)
        
        selectWallpaper = ooldtp.context(self.DLG_ADDWALLPAPER)
        while selectWallpaper.getchild(self.TBTN).press():
            if ldtp.hasstate(self.DLG_ADDWALLPAPER,self.TXT_LOCATION,'SHOWING'):
                selectWallpaper.settextvalue(self.TXT_LOCATION, background_path)
                break

        selectWallpaper.getchild(self.BTN_OPEN).click()
        ldtp.waittillguinotexist(self.DLG_ADDWALLPAPER)

        appearance.remap()
        num_aft = len(appearance.getchild(self.LP).getobjectproperty('children').split(' '))
        if (num_aft - num) != 1:
            raise ldtp.LdtpExecutionError, "Failed to add new background"

    def revert_default(self):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_BACKGROUND)
        appearance.getchild(self.BTN_ADD).click()

        ldtp.waittillguiexist(self.DLG_ADDWALLPAPER)

        selectWallpaper = ooldtp.context(self.DLG_ADDWALLPAPER)
        while selectWallpaper.getchild(self.TBTN).press():
            if ldtp.hasstate(self.DLG_ADDWALLPAPER,self.TXT_LOCATION,'SHOWING'):
                selectWallpaper.settextvalue(self.TXT_LOCATION, self.Default)
                break

        selectWallpaper.getchild(self.BTN_OPEN).click()
        ldtp.wait(2)
        ldtp.waittillguinotexist(self.DLG_ADDWALLPAPER)
        ldtp.waittillguiexist(self.WINDOW)

    def revert_background(self):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_BACKGROUND)
        appearance.remap()
        num = len(appearance.getchild(self.LP).getobjectproperty('children').split(' '))
        appearance.getchild(self.BTN_REMOVE).click()

        appearance.remap()
        num_aft = len(appearance.getchild(self.LP).getobjectproperty('children').split(' '))
        if (num - num_aft) != 1:
            raise ldtp.LdtpExecutionError, "Failed to remove selected background"

    def change_font(self, category):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_FONTS)
        appearance.getchild(self.FONTS[category]["BTN"]).click()
        ldtp.wait(2)

        if (ldtp.guiexist(self.DLG_PICKAFONT)):
            pickaFont = ooldtp.context(self.DLG_PICKAFONT)
            pickaFont.getchild(self.TBL_FAMILY).selectrow(self.FONTS[category]["FAMILY"])
            pickaFont.getchild(self.TBL_STYLE).selectrow(self.FONTS[category]["STYLE"])
            pickaFont.getchild(self.TBL_SIZE).selectrow(self.FONTS[category]["SIZE"])
            pickaFont.getchild(self.BTN_OK).click()
        else:
            raise ldtp.LdtpExecutionError, "Failed to setup font properties"

        ldtp.waittillguiexist(self.WINDOW)

        #To check the change has been made as expected
        font_prop = appearance.getchild(self.FONTS[category]["BTN"]).getobjectproperty('children').split(' ')
        for i in range(len(font_prop)):
            if (font_prop[i].__contains__(self.FONTS[category]["FAMILY"]) and \
               font_prop[i].__contains__(self.FONTS[category]["STYLE"].replace(' ',''))) or \
               (font_prop[i] == ('lbl' + self.FONTS[category]["FAMILY"] + self.FONTS[category]["STYLE"].replace(' ',''))) or \
               (font_prop[i] == ('lbl' + self.FONTS[category]["FAMILY"])) or \
               (font_prop[i].__contains__(self.FONTS[category]["FAMILY"])) or \
               (font_prop[i].__contains__(self.FONTS[category]["SIZE"])):
                pass
            else:
                raise ldtp.LdtpExecutionError, "Font properties not changed correctly"

    def revert_font(self):
        appearance = ooldtp.context(self.name)
        appearance.getchild(self.PTABLE).selecttab(self.PTAB_FONTS)
       
        font_btn = [self.BTN_APPLICATIONFONT, self.BTN_DOCUMENTFONT, self.BTN_DESKTOPFONT, self.BTN_WINDOWTITLEFONT, self.BTN_FIXEDWIDTHFONT]
        for btn in font_btn:
            appearance.getchild(btn).click()
            ldtp.wait()

            if ldtp.guiexist(self.DLG_PICKAFONT):
                pickaFont = ooldtp.context(self.DLG_PICKAFONT)
                if btn == self.BTN_WINDOWTITLEFONT:
                    pickaFont.getchild(self.TBL_FAMILY).selectrow('Sans')
                    pickaFont.getchild(self.TBL_STYLE).selectrow('Bold')
                elif btn == self.BTN_FIXEDWIDTHFONT:
                    pickaFont.getchild(self.TBL_FAMILY).selectrow('Monospace')
                    pickaFont.getchild(self.TBL_STYLE).selectrow('Regular')
                else:
                    pickaFont.getchild(self.TBL_FAMILY).selectrow('Sans')
                    pickaFont.getchild(self.TBL_STYLE).selectrow('Regular')
                pickaFont.getchild(self.TBL_SIZE).selectrow('10')
                pickaFont.getchild(self.BTN_OK).click()
                if platform.processor() == 'sparc':
                    ldtp.waittillguiexist(self.WINDOW, 30)
                else:
                    ldtp.waittillguiexist(self.WINDOW, 10)
            else:
                raise ldtp.LdtpExecutionError, "Failed to restore the default font settings"

   
    def __init__(self):
        Application.__init__(self)
