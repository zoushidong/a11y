"""
This module contains the definition of the test suite for Baobab testing.
"""
import ldtp, ooldtp
from .main import SingleApplicationTestSuite
from ..application.baobab import Application, Baobab

class BaobabTestSuite(SingleApplicationTestSuite):
    """
    Default test suite for Baobab
    """
    APPLICATION_FACTORY = Baobab

    def setup(self):
        self.application.open()

    def teardown(self):
        self.application.close()

    def cleanup(self):
        pass
