"""
This module contains different kinds of runner classes needed to
execute test cases
"""
import os, traceback, logging
import xml.etree.ElementTree as etree
from time import time
import ldtp

from . import globals
from .result import ResultDict


class TestCaseRunner:
    """
    Class in charge of running  a single test case
    """

    def __init__(self, case_data, suite_class):
        self.case_data = case_data
        self.test_method = getattr(suite_class,
                                   case_data.methodname)
        self.results = ResultDict()

    def run(self, logger):
        """
        Run test case and gather results
        """
        if self.case_data.skip:
            logging.info("Skipping test case '%s'" % \
                             self.case_data.name)
            return

        logging.info("Running test case '%s' (%s)"
                     % (self.case_data.name,
                        self.case_data.methodname))
        starttime = time()
        try:
            rv = self.test_method(**self.case_data.args)
        except AssertionError, e:
            # The test failed.
            if len(e.args) > 1:
                self.results.append('message', e.args[0].encode("utf-8"))
                self.results.append_screenshot(e.args[1])
            else:
                self.results.append('message', e.args[0].encode("utf-8"))
                self.results.append_screenshot()
            self.results.append('stacktrace', traceback.format_exc())
            self.results['pass'] = 0
        except Exception, e:
            # There was an unrelated error.
            logging.warning(traceback.format_exc())
            if len(e.args) > 1 and os.path.exists(e.args[1]):
                self.results.append('message', e.args[0].encode("utf-8"))
                self.results.append_screenshot(e.args[1])
            else:
                self.results.append('message', e.args[0].encode("utf-8"))
                self.results.append_screenshot()
            self.results.append('stacktrace', traceback.format_exc())
            self.results['error'] = 1
        else:
            self.results['pass'] = 1
            try:
                message, screenshot = rv
            except:
                pass
            else:
                if message:
                    self.results.append('message', message)
                if screenshot:
                    self.results.append_screenshot(screenshot)
        finally:
            self.results['time'] = time() - starttime
        
        self.case_data.add_results(self.results)

        
class TestSuiteRunner:
    """
    Class in charge of running a whole test suite
    """

    def __init__(self, suite_data, loggerclass=None):
        self.suite_data = suite_data
        self.results = ResultDict()

        # Get the suite implementation
        # in order to be able to execute it's method
        if not self.suite_data.skip:
            self.suite = suite_data.get_class()

    
    def run(self, loggerclass=None, setup_once=True):
        """
        Run the test suite and return xml report
        """
        if self.suite_data.skip:
            logging.info("Skipping test suite '%s'" % \
                             self.suite_data.name)
            return etree.tostring(self.suite_data.root, "utf-8")

        logging.info("Running test suite '%s' (%s)"
                     % (self.suite_data.name,
                        self.suite_data.fullname))
        try:
            self._run(loggerclass, setup_once)
        except Exception, e:
            logging.warning(traceback.format_exc())
            # There was an unrelated error.
            self.results.append('message', e.args[0].encode("utf-8"))
            self.results.append('stacktrace', traceback.format_exc())
            self.results['error'] = 1
            try:
                self.suite.teardown()
            except:
                pass

        self.suite_data.add_results(self.results)
        return etree.tostring(self.suite_data.root, "utf-8")
 
           
    def _run(self, loggerclass, setup_once):
        """
        Run fixture methods and later the test cases in the test suite one by one
        """
        if loggerclass:
            logger = loggerclass()
        else:
            logger = ldtp

        if setup_once:
            # Set up the environment.
            self.suite.setup()

        firsttest = True

        case_runners = [TestCaseRunner(case_data, self.suite)
                        for case_data in self.suite_data.cases()]
        for case_runner in case_runners:
            if not setup_once:
                # Set up the app for each test, if requested.
                self.suite.setup()
            if not firsttest:
                # Clean up from previous run.
                self.suite.cleanup()
            firsttest = False
            case_runner.run(logger)
            if not setup_once:
                # Teardown upthe app for each test, if requested.
                self.suite.teardown()

        if setup_once:
            # Tear down after entire suite.
            self.suite.teardown()
