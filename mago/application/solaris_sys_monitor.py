PACKAGE = "solaris_sys_monitor"

#-*- coding:utf-8 -*-
"""
This is the "solaris_sys_monitor" module.

This module provides a wrapper for LDTP to make the writing of Solaris
System Monitor tests easier.
"""
import ooldtp
import ldtp
from .main import Application
from ..gconfwrapper import GConf
from ..cmd import globals
import gettext
import commands
import multiprocessing 


gettext.install (True)
gettext.bindtextdomain (PACKAGE, globals.LOCALE_SHARE)
gettext.textdomain (PACKAGE)
t = gettext.translation(PACKAGE, globals.LOCALE_SHARE, fallback = True)
_ = t.gettext


class SolarisSysMonitor(Application):
    """
    SolarisSysMonitor manages the solaris gnome-system-monitor application in interactive mode.
    """

    LAUNCHER = 'gnome-system-monitor'
    LAUNCHER_ARGS = []
    CLOSE_TYPE = 'menu'
    CLOSE_NAME = _('mnuQuit')

    WINDOW = _('frmSystemMonitor')
    DLG_PREFERENCES = _('dlgSystemMonitorPreferences')
    MNU_PREFERENCES = _('mnuPreferences')
    
    BTN_CLOSE = _('btnClose')
    MNU_ACTIVE = _('mnuActiveProcesses')
    MNU_ALL = _('mnuAllProcesses')
    MNU_MY = _('mnuMyProcesses')
    MNU_DEP = _('mnuDependencies')

    PTAB = _('ptl0')
    PTAB_SYSTEM = _('ptabSystem')
    PTAB_PROCESSES = _('ptabProcesses')
    PTAB_RESOURCES = _('ptabResources')
    PTAB_FILESYSTEMS = _('ptabFileSystems')

    FLR3 = _('flr3')
    LBL_SOLARIS = _('lblSolaris')
    LBL_HARDWARE = _('lblHardware')
    LBL_STATUS = _('lblSystemStatus')

    TBL_PROCESSES = _('ttbl0')
    TBL_FILESYSTEMS = _('tbl0')

    LBL_CPU_HISTORY = _('lblCPUHistory')
    LBL_MEM_SWAP = _('lblMemoryandSwapHistory')
    LBL_NETWORK_HISTORY = _('lblNetworkHistory')

    LBL_MEMORY = _('lblMemory')
    LBL_SWAP = _('lblSwap')
    LBL_RECEIVING = _('lblReceiving')
    LBL_TOTAL_RECEIVED = _('lblTotalReceived')
    LBL_SENDING = _('lblSending')
    LBL_TOTAL_SENT = _('lblTotalSent')
    LBL_CPU = _('lblCPU')

    def __init__(self):
        Application.__init__(self)

    def verify_sysinfo(self):
        """
        To verify the information listed in System tab
        """
        output = commands.getstatusoutput('uname -a')
        if output[0] != 0:
            raise ldtp.LdtpExecutionError, "Get a failure from uname command"

        result = output[1].split(' ')
        host = result[1]
        arc = result[5]
        release = result[3]
        OS = result[0]
        version = result[2]

        monitor = ooldtp.context(self.WINDOW)
        monitor.selecttab(self.PTAB,self.PTAB_SYSTEM)

        if monitor.guiexist(host) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find host name label"
        if monitor.guiexist('Kernel'+OS+version) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find OS and version label"
        if arc == 'sparc':
            cpu = 'SPARC'
        elif arc == 'i386' or arc == 'i86pc':
            cpu = 'X86'
        if monitor.guiexist('ReleaseOracleSolaris'+release+cpu) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find release and cpu label"
        if monitor.guiexist(self.LBL_SOLARIS) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find Solaris label"
        if monitor.guiexist(self.LBL_HARDWARE) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find Hardware label"
        if monitor.guiexist(self.LBL_STATUS) == 0:
            raise ldtp.LdtpExecutionError, "Failed to find System Status label"

    def change_view(self, view):
        """
        To verify the processes quantity will change after the process view is changed
        """
        monitor = ooldtp.context(self.WINDOW)
        monitor.selecttab(self.PTAB, self.PTAB_PROCESSES)
        """
        To get the current checked view menuitem and processes number
        """
        mnu = [self.MNU_ACTIVE, self.MNU_ALL, self.MNU_MY]
        for i in mnu:
            if monitor.getchild(i).hasstate('checked'):
                mnu_before = i
        tbl_count_bef = monitor.getchild(self.TBL_PROCESSES).getrowcount()

        if view == 'Active':
            mnu_select = self.MNU_ACTIVE
        elif view == 'All' :
            mnu_select = self.MNU_ALL
        elif view == 'My':
            mnu_select = self.MNU_MY

        #If the selected menu in test case is as same as the application menu which has checked stats, do nothing
        if mnu_select == mnu_before:
            pass
        else:
            monitor.getchild(mnu_select).selectmenuitem()
            ldtp.wait(2)
            tbl_count_aft = monitor.getchild(self.TBL_PROCESSES).getrowcount()
            if tbl_count_bef == tbl_count_aft:
                raise ldtp.LdtpExecutionError, "Processes number didn't change, there's something wrong while selecting " + mnu_select + " menu to change processes view."


    def verify_resource_info(self):
        """
        To verify the labels in Resources tab
        """
        monitor = ooldtp.context(self.WINDOW)
        monitor.selecttab(self.PTAB, self.PTAB_RESOURCES)
        status = ['enabled','visible','showing']
        
        #To verify the head labels
        tags = [self.LBL_CPU_HISTORY, self.LBL_MEM_SWAP, self.LBL_NETWORK_HISTORY]
        for i in tags:
            for j in status:
                if monitor.getchild(i).hasstate(j):
                    pass
                else:
                    raise ldtp.LdtpExecutionError, "The label " + i + " doesn't have status " + j + ", please verify it manually"

        #To verify other labels except head labels
        labels = [self.LBL_SWAP, self.LBL_RECEIVING, self.LBL_TOTAL_RECEIVED, self.LBL_SENDING, self.LBL_TOTAL_SENT, self.LBL_MEMORY]
        for label in labels:
            for stat in status:
                if monitor.getchild(label).hasstate(stat):
                    pass
                else:
                    raise ldtp.LdtpExecutionError, "The label " + label + " doesn't have status " + stat + ", please verify it manually"

        #To verify CPU info
        cpu_count = multiprocessing.cpu_count()
        for cpu in range(1, cpu_count+1):
            for cpu_stat in status:
                if cpu_count == 1:
                    cpu_tag = self.LBL_CPU
                else:
                    cpu_tag = self.LBL_CPU + str(cpu)
                if monitor.getchild(cpu_tag).hasstate(cpu_stat):
                    pass
                else:
                    raise ldtp.LdtpExecutionError, "The label " + self.LBL_CPU + str(cpu) + " doesn't have status " + cpu_stat + ", please verify it manually"

    def open_preferences(self):
        """
        To open the gnome-system-monitor preferences dialog and close it
        """
        monitor = ooldtp.context(self.WINDOW)
        monitor.getchild(self.MNU_PREFERENCES).selectmenuitem()
        pref = ooldtp.context(self.DLG_PREFERENCES)
        pref.getchild(self.BTN_CLOSE).click()
