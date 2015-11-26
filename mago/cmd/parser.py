"""
This module contains the code needed to parse all the options
"""
import os
from copy import copy
from optparse import OptionParser, OptionGroup, OptionValueError
from optparse import Option as OldOption

from . import globals

def check_dir(option, opt, value):
    """
    Check if an dir option string contains a real directory
    """
    value = os.path.realpath(os.path.expanduser(value))
    if not os.path.isdir(value):
        raise OptionValueError("option %s: "
                               "Directory '%s' doesn't exist"
                               % (opt, value))
    return value

        
def check_dirname(option, opt, value):
    """
    Check if an dirname option string contains a valid directory name
    """
    value = os.path.realpath(os.path.expanduser(value))
    if os.path.exists(value) and not os.path.isdir(value):
        raise OptionValueError("option %s: "
                               "Directory '%s' exists, but isn't a directory"
                               % (opt, value))
    return value

class Option(OldOption):
    """
    Extended option class that adds two directory types:
    - dirname: Valid directory name that isn't required to exist
    - dir: Valid directory name that must exist
    """
    TYPES = OldOption.TYPES + ("dir", "dirname")
    TYPE_CHECKER = copy(OldOption.TYPE_CHECKER)
    TYPE_CHECKER["dir"] = check_dir
    TYPE_CHECKER["dirname"] = check_dirname


def parse_options(args):
    """
    Parse options passed through the command line
    """
    default_target = "~/.mago"
    default_log_level = "critical"

    parser = OptionParser(description="Execute automated tests",
                          option_class=Option)

    parser.add_option('-i', '--info',
                      action="store_true",
                      help=("Display information about test cases "
                            "without executing them"))

    parser.add_option('--noa11y',
                      action="store_true",
                      help=("Do not check if the accessibility "
                            "information is enabled"))
    
    group = OptionGroup(parser, "Test selection options")
    group.add_option("-a", "--application",
                     dest="applications",
                     metavar="APPLICATION",
                     action="append",
                     type="string",
                     default=[],
                     help=("Application name to test. Option can be repeated "
                           "and defaults to all applications"))
    group.add_option("-n", "--suite_name",
                     dest="suite_names",
                     metavar="NAME",
                     action="append",
                     type="string",
                     default=[],
                     help=("Suite name to test within applications. Option "
                           "can be repeated and default to all suites "
                           "unless suite name or suite file filtering "
                           "has been enabled"))
    group.add_option("-f", "--suite_file",
                     dest="suite_files",
                     metavar="FILE",
                     action="append",
                     type="string",
                     default=[],
                     help=("Suite file to test within applications. Option "
                           "can be repeated and default to all suites "
                           "unless suite name or suite file filtering "
                           "has been enabled"))
    group.add_option("-c", "--case",
                     dest="cases",
                     metavar="CASE",
                     action="append",
                     type="string",
                     default=[],
                     help="Test cases to run (all, if not specified).")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Logging options")
    group.add_option("-l", "--log",
                     metavar="FILE",
                     help="The file to write the log to.")
    group.add_option("--log-level",
                     default=default_log_level,
                     help="One of debug, info, warning, error or critical.")
    group.add_option("-t", "--target",
                     metavar="DIR",
                     type="dirname",
                     default=default_target,
                     help=("Target directory for logs and reports. Defaults "
                           "to: %default"))
    parser.add_option_group(group)

    (options, args) = parser.parse_args(args[1:])

    return options
