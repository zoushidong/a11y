"""
This module contains the definition of the test suite used for Gnome Screenshot
testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.gnome_screenshot import Application, GnomeScreenshot


class GnomeScreenshotTestSuite(SingleApplicationTestSuite):
    APPLICATION_FACTORY = GnomeScreenshot   
