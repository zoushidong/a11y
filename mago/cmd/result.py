"""
This module provides a class to easily store test results
"""
from time import strftime
from shutil import move
import ldtputils

from . import globals
from .utils import safe_make_directory

class ResultDict(dict):
    """
    Dictionary-like class to store test case results
    """
    def __setitem__(self, key, value):
        """
        Set value as a one element list using key
        """
        dict.__setitem__(self, key, [value])


    def append(self, key, value):
        """
        Append a result using key
        """
        values = self.get(key, None)
        if not values:
            self[key] = value
        else:
            values.append(value)


    def append_screenshot(self, screenshot_file=None):
        """
        Take screenshot and append the filename to screenshot results
        """
        _logFile = "%s/screenshot-%s.png" % (globals.SCREENSHOTS_SHARE,
                                             strftime ("%m-%d-%Y-%H-%M-%s"))
        safe_make_directory(globals.SCREENSHOTS_SHARE)
        if not screenshot_file:
            ldtputils.imagecapture(out_file = _logFile)
        else:
            move(screenshot_file, _logFile)
        self.append('screenshot', _logFile)
