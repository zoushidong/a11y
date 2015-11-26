"""
This module contains the definition of the test suite for Gnome_about_me testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.solaris_gnome_about_me import Application, GnomeAboutMe

class GnomeAboutMeTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Gnome_about_me
    """
    APPLICATION_FACTORY = GnomeAboutMe
    def setup(self):
        self.application.open()

    
    def teardown(self):
        self.application.close()

    def cleanup(self):
	pass
