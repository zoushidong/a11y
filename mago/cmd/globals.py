"""
This module just provides a namespace for global variables used across
multiple modules in the package
"""
import os

def _get_grandparent_dir(filename):
    return os.path.dirname(os.path.dirname(os.path.dirname(filename)))

def _get_share_dir():
    if os.path.exists(os.path.join(_get_grandparent_dir(__file__), 'setup.py')):
        # We are in the build directory.
        return _get_grandparent_dir(__file__)
    else:
        # We are in an installed prefix.
        prefix = os.path.dirname(__file__)
        while not os.path.exists(os.path.join(prefix, 'share', 'mago')):
            new_prefix = os.path.dirname(prefix)
            if new_prefix == prefix:
                return _get_grandparent_dir(__file__)
            prefix = new_prefix
        
        return os.path.join(prefix, 'share', 'mago')

def _get_locale_dir():
    if os.path.exists(os.path.join(_get_grandparent_dir(__file__), 'setup.py')):
        # We are in the build directory.
        return os.path.join(_get_grandparent_dir(__file__), 'build/mo')
    else:
        # We are in an installed prefix.
        prefix = os.path.dirname(__file__)
        while not os.path.exists(os.path.join(prefix, 'share', 'locale')):
            new_prefix = os.path.dirname(prefix)
            if new_prefix == prefix:
                return _get_grandparent_dir(__file__)
            prefix = new_prefix
        
        return os.path.join(prefix, 'share', 'locale')

MAGO_SHARE = os.environ.get('MAGO_SHARE', _get_share_dir())
LOCALE_SHARE = _get_locale_dir()
MAGO_PATH = [os.path.curdir, MAGO_SHARE]

if os.environ.get('MAGO_PATH', None):
    MAGO_PATH = os.environ['MAGO_PATH'].split(':')

SCREENSHOTS_SHARE = "/tmp/ldtp-screenshots"
