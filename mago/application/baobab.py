PACKAGE = "mago"

#-*- coding:utf-8 -*-
"""
This is the "baobab" module.

This module provides a wrapper for LDTP to make writing Baobab tests easier.
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


class Baobab(Application):
    """
    baobab manages the Baobab application.
    """
    CLOSE_TYPE = 'menu'
    CLOSE_NAME = _('mnuQuit')
    LAUNCHER = 'baobab'
    LAUNCHER_ARGS = []
    WINDOW = 'frmDiskUsageAnalyzer'
    
    DLG_SELECTFOLDER = _('dlgSelectFolder')
    BTN_REFRESH = _('btnRefresh')
    BTN_SCANFILESYSTEM = _('btnScanFilesystem')
    BTN_SCANFOLDER = _('btnScanFolder')
    BTN_SCANHOME = _('btnScanHome')
    BTN_SCANREMOTEFOLDER = _('btnScanRemoteFolder')
    BTN_STOP = _('btnStop')
    BTN_TYPEAFILENAME = _('tbtnTypeafilename')
    MNU_ABOUT = _('mnuAbout')
    MNU_COLLAPSEALL = _('mnuCollapseAll')
    MNU_CONTENTS = _('mnuContents')
    MNU_EMPTY = _('mnuEmpty')
    MNU_EMPTY1 = _('mnuEmpty1')
    MNU_EMPTY2 = _('mnuEmpty2')
    MNU_EMPTY3 = _('mnuEmpty3')
    MNU_EXPANDALL = _('mnuExpandAll')
    MNU_PREFERENCES = _('mnuPreferences')
    MNU_QUIT = _('mnuQuit')
    MNU_REFRESH = _('mnuRefresh')
    MNU_SCANFILESYSTEM = _('mnuScanFilesystem')
    MNU_SCANFOLDER = _('mnuScanFolder')
    MNU_SCANHOMEFOLDER = _('mnuScanHomeFolder')
    MNU_SCANREMOTEFOLDER = _('mnuScanRemoteFolder')
    MNU_STOP = _('mnuStop')
    MNU_VIEWASRINGSCHART = _('mnuViewasRingsChart')
    MNU_VIEWASTREEMAPCHART = _('mnuViewasTreemapChart')
    TXT_LOCATION = _('txtLocation')
    CBO_VIEWAS = _('cboViewas*')
    
    
    def baobab_scan_home(self):
        baobab = ooldtp.context(self.name)
        
        #Scan the home folder and wait till the end of the scan.
        baobab.getchild(self.MNU_SCANHOMEFOLDER).selectmenuitem()
        buttonStop = baobab.getchild(self.BTN_STOP)
        
        while buttonStop.stateenabled():
            ldtp.wait()
        
        self.baobab_change_views()	
        #Scan the home again now this time using the button in the toolbar.
        baobab.getchild(self.BTN_SCANHOME).click()
             
        while buttonStop.stateenabled(): 
            ldtp.wait()
        
        self.baobab_change_views()
                
    def baobab_scan_folder(self, path):
        baobab = ooldtp.context(self.name)
        
        baobab.getchild(self.BTN_SCANFOLDER).click()

        ldtp.waittillguiexist(self.DLG_SELECTFOLDER)
        
        if (ldtp.guiexist(self.DLG_SELECTFOLDER)):
            selectFiles = ooldtp.context(self.DLG_SELECTFOLDER)
            if not (selectFiles.getchild(self.TXT_LOCATION)):
                ldtp.generatekeyevent('<ctrl>l')
            textLocation = selectFiles.getchild(self.TXT_LOCATION)
            textLocation.settextvalue(path)
            ldtp.generatekeyevent('<return>')
        ldtp.wait(2)
                
        buttonStop = baobab.getchild(self.BTN_STOP)
        
        while buttonStop.stateenabled():
            ldtp.wait()
        
        self.baobab_change_views()
    	
    def baobab_scan_filesystem(self):
    	baobab = ooldtp.context(self.name)
    	
    	#Scan the filesystem 
    	baobab.getchild(self.MNU_SCANFILESYSTEM).selectmenuitem()
    	buttonStop = baobab.getchild(self.BTN_STOP)
        
        while buttonStop.stateenabled():
            ldtp.wait(2)
    	
    	#Change the views again to see if that works and we don't get any crash.
    	self.baobab_change_views()
    	
    def baobab_change_views(self):
        baobab = ooldtp.context(self.name)
        
        #Change the graph view.               
        if baobab.guiexist('cboViewasRingsChart'):
            baobab.comboselect('cboViewasRingsChart', 'mnuViewasTreemapChart')
        else:
            baobab.comboselect('cboViewasTreemapChart', 'mnuViewasRingsChart') 

        #Collapse and expand the tree
        baobab.getchild(self.MNU_EXPANDALL).selectmenuitem()
        ldtp.wait(2)
        baobab.getchild(self.MNU_COLLAPSEALL).selectmenuitem()
    
    def __init__(self):
        Application.__init__(self)
