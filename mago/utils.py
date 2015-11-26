import os
import gtk, gobject, wnck
import subprocess
import re

def show_desktop(show):
    def _start_showing():
        screen.toggle_showing_desktop(show)

    screen = wnck.screen_get_default()
    gobject.idle_add(_start_showing)
    gobject.idle_add(gtk.main_quit)
    gtk.main()

def get_system_language():
    raise NotImplementedError, "not yet..."

def get_ldtp_version():
    script = subprocess.Popen(['ldtp', '--version'], stdout=subprocess.PIPE)
    version =  script.communicate()[0]
    pattern = re.compile("ldtp-(\d\.\d\.\d).*")
    m = pattern.match(version)
    version = m.group(1)
    return version


