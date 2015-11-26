"""
This module provides the main entry point for the execution automated
desktop test cases
"""

import os, re, sys, logging
import logging
from logging import StreamHandler, FileHandler, Formatter
from itertools import chain
import ldtp

from . import globals
from .runner import TestSuiteRunner
from .parser import parse_options
from .utils import safe_make_directory, safe_run_command, accessibility_enabled
from .discovery import discover_applications

def validate_environment():
    """
    Check environmental settings and ensure that the system is setup for mago
    """
    if not accessibility_enabled():
        raise Exception, ("Accessibility must be enabled to use mago. "
            "Enable it in the assisstive technologies panel and restart X.")

def process_application(app_data, target_directory):
    """
    Process all test suites in an application
    """
    logging.debug("Processing application '%s' (%s)"
                  % (app_data.name, app_data.path))
    application_target = app_data.get_target_directory(target_directory)
    safe_make_directory(application_target)

    for suite_data in app_data.suites():
        process_suite(suite_data, application_target)


def process_suite(suite_data, application_target):
    """
    Run the suite test cases, make sure that the logs are stored
    in the correct directory and generate html report from them
    """
    runner = TestSuiteRunner(suite_data)
    results = runner.run()

    log_file = suite_data.get_log_filename(application_target)
    with open(log_file, 'w') as f:
        f.write(results)
    convert_log_file(log_file)


def convert_log_file(log_file):
    """
    Transform xml log format into html report
    """
    if os.path.exists(globals.SCREENSHOTS_SHARE):
        screenshot_dir = os.path.join(os.path.dirname(log_file),
                                      "screenshots")

        if not os.path.exists(screenshot_dir):            
            safe_make_directory(screenshot_dir)

        if len(os.listdir(globals.SCREENSHOTS_SHARE)) > 0:
            command = "mv " + globals.SCREENSHOTS_SHARE + "/* " + screenshot_dir
            safe_run_command(command)

    log_file_tmp = log_file + ".tmp"
    o = open(log_file_tmp, "w")
    data = open(log_file).read()
    o.write(re.sub(globals.SCREENSHOTS_SHARE, "screenshots", data))
    o.flush()
    o.close()
    
    os.remove(log_file)
    os.rename(log_file_tmp, log_file)

    xsl_file = os.path.join(globals.MAGO_SHARE, "report.xsl")
    if not os.path.exists(xsl_file):
        logging.error("XSL file `%s' does not exist." % xsl_file)
        sys.exit(1)

    html_file = log_file.replace(".log", ".html")

    command = "xsltproc -o %s %s %s" \
        % (html_file, xsl_file, log_file)
    safe_run_command(command)
 

def configure_logging(log_level_str, log_filename):
    """
    Configure log handlers
    """
    log_level = logging.getLevelName(log_level_str.upper())
    log_handlers = []
    log_handlers.append(StreamHandler())
    if log_filename:
        log_handlers.append(FileHandler(log_filename))

    format = ("%(asctime)s %(levelname)-8s %(message)s")
    if log_handlers:
        for handler in log_handlers:
            handler.setFormatter(Formatter(format))
            logging.getLogger().addHandler(handler)
        if log_level:
            logging.getLogger().setLevel(log_level)
    elif not logging.getLogger().handlers:
        logging.disable(logging.CRITICAL)


def main(args=sys.argv):
    """
    Execute automated tests
    """
    # For the moment, all applications should be running in English
    ldtp.setlocale("C")

    # Get shared directory based on the directory in which binary is located
    options = parse_options(args)
    configure_logging(options.log_level, options.log)

    if not options.noa11y:
        validate_environment()

    logging.debug('MAGO_SHARE: %s' % globals.MAGO_SHARE)
    logging.debug('MAGO_PATH: %s' % ':'.join(globals.MAGO_PATH))
    logging.debug('SCREENSHOTS_SHARE: %s' % globals.SCREENSHOTS_SHARE)

    apps = discover_applications(globals.MAGO_PATH,
                                 options.applications,
                                 options.suite_names,
                                 options.suite_files,
                                 options.cases)

    # Execute test cases
    if not apps:
        logging.warning("No test applications found")
    else:
        if not options.info:
            for app in apps:
                process_application(app, options.target)
        else:
            for app in apps:
                print "Application: %s - %s" % (app.name, app.path)
                for suite in app.suites():
                    print "- Suite: %s - %s%s" % \
                        (suite.name, suite.filename, 
                         ' SKIP' if suite.skip else '')
                    for case in suite.cases():
                        print " - Case: %s%s" % \
                            (case.name, ' SKIP' if case.skip else '')

    return 0


if __name__ == "__main__":
    sys.exit(main())
