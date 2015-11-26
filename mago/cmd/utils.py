"""
This module contains utility functions for file management and command
execution
"""
import os, logging
from stat import ST_MODE, S_IMODE
from subprocess import Popen, PIPE
from ..gconfwrapper import GConf

def accessibility_enabled():
    """
    Check gconf key to determine if accessibility is enabled.
    
    @return: Value of accessibility key in gconf
    @rtype: bool
    """
    return GConf.get_item('/desktop/gnome/interface/accessibility')

def safe_change_mode(path, mode):
    """
    Set permissions to directory
    """
    if not os.path.exists(path):
        logging.error("Path does not exist: %s" % path)
        sys.exit(1)

    old_mode = os.stat(path)[ST_MODE]
    if mode != S_IMODE(old_mode):
        os.chmod(path, mode)


def safe_make_directory(path, mode=0755):
    """
    Create directory only if it doesn't exist
    """
    if os.path.exists(path):
        if not os.path.isdir(path):
            logging.error("Path is not a directory: %s" % path)
            sys.exit(1)

        safe_change_mode(path, mode)
    else:
        logging.debug("Creating directory: %s" % path)
        os.makedirs(path, mode)


def safe_run_command(command):
    """
    Run a shell command and capture its output
    """
    logging.debug("Running command: %s" % command)
    p = Popen(command, stdout=PIPE, shell=True)
    (pid, status) = os.waitpid(p.pid, 0)
    if status:
        logging.error("Command failed: %s" % command)

    return p.stdout.read()
