"""
This module contains the functionality related to the discovery of the test suites
"""
import os, re, logging
import xml.etree.ElementTree as etree
import imp


class ApplicationData:
    """
    Application description data
    """
    name_pattern = r"[a-z0-9][-_a-z0-9+.]*"
    name_regex = re.compile(name_pattern)
    whitelist = None


    def __init__(self, path, filenames):
        self.path = path
        self.filenames = filenames

        self.name = os.path.basename(path)


    def __eq__(self, other):
        """
        Two applications are considered to be equal if they have the
        same name
        """
        return (type(self) == type(other)
                and self.name == other.name)


    def name_matches(self):
        """
        Return True if the application name
        honors the expected pattern
        """
        return self.name_regex.match(self.name)


    def suites(self):
        """
        Return a generator for all suites
        """
        return SuiteData.discover(self)


    def get_target_directory(self, base_target_directory):
        """
        Return application target_directory
        """
        return os.path.join(base_target_directory,
                            self.name)

    @classmethod
    def discover(cls, base_dirpaths):
        """
        Generator that discovers all applications under
        a list of top directories
        """
        discovered_applications = []
        for base_dirpath in base_dirpaths:
            dirpaths = [os.path.join(base_dirpath, d)
                        for d in os.listdir(base_dirpath)
                        if os.path.isdir(os.path.join(base_dirpath, d))]

            for dirpath in dirpaths:
                try:
                    filenames = [f
                                 for f in os.listdir(dirpath)
                                 if os.path.isfile(os.path.join(dirpath, f))]
                except OSError:
                    continue # Permission denied.

                # Application directories are expected to honor
                # the specified name pattern
                app = cls(dirpath, filenames)
                if not app.name_matches():
                    logging.debug("Application name %s does not match pattern: %s"
                                  % (app.name, app.name_pattern))
                    continue

                # This check makes sure that the same application
                # isn't discovered twice. That is to say, when discovering
                # applications from multiple directories, the test cases 
                # from the application that is first found will be
                # executed while the others will be discarded
                if app in discovered_applications:
                    logging.debug("Application name %s has been already discovered"
                                  % app.name)
                    continue

                # Return application only if there is no whitelist
                # or if it matches any of the whitelist names
                if cls.whitelist and not app.name in cls.whitelist:
                    logging.debug("Application name %s has not been whitelisted"
                                  % app.name)
                    continue

                # At least one '.xml' file with a 'suite' root tag
                # should be contained in the directory to be a valid application directory
                if not any(app.suites()):
                    logging.debug("Application directory %s does't seem to contain a valid suite file"
                                  % app.path)
                    continue

                discovered_applications.append(app)
                yield app


class XmlData:
    """
    Common methods for XML test data
    """
    @property
    def name(self):
        """
        Return suite name as written in the xml file
        """
        return self.root.attrib['name']


    @property
    def args(self):
        """
        Return suite arguments as a dictionary
        """
        def _parse_args(tag):
            if tag is None:
                return {}

            if len(tag) == 0:
                try:
                    return int(tag.text)
                except ValueError:
                    return tag.text
                except TypeError:
                    return tag.text

            rv = {}
            for child in tag:
                key = child.tag.encode('ascii')
                value = _parse_args(child)
                try:
                    rv[key].append(value)
                except AttributeError:
                    rv[key] = [rv[key], value]
                except KeyError:
                    rv[key] = value                        
            return rv
        
        return _parse_args(self.root.find('args'))
        
    @property
    def description(self):
        """
        Return suite description as written in the xml file
        """
        return self.root.find('description').text.strip()


    def add_results(self, results):
        """
        Add results to the xml data of the test case
        to generate later report easily
        """
        if not results:
            return

        result_tag = etree.SubElement(self.root, 'result')
        for key, values in results.items():
            for value in values:
                new_result_tag = etree.SubElement(result_tag, key)
                new_result_tag.text = str(value)


class SuiteData(XmlData):
    """
    Suite description data
    """
    name_whitelist = None
    filename_whitelist = None


    def __init__(self, application, filename):
        self.application = application
        self.filename = filename
        self.fullname = os.path.join(application.path,
                                     filename)

        try:
            self.tree = etree.parse(self.fullname)
            self.root = self.tree.getroot()
        except:
            self.tree = None
            self.root = None


    def get_class(self):
        """
        Return suite instance from the python module
        """
        module_name, class_name = self.root.find('class').text.rsplit('.', 1)
        logging.debug("Module name: %s", module_name)

        # Suite file and module are expected to be in the same directory
        load_args = imp.find_module(
            module_name, [os.path.dirname(self.fullname)])

        module = imp.load_module(module_name, *load_args)

        cls = getattr(module, class_name)
        return cls(**self.args)

    
    def get_log_filename(self, application_target_directory):
        """
        Return log filename under application target directory
        """
        return os.path.join(
            application_target_directory, 
            "%s.log" % os.path.basename(os.path.splitext(self.filename)[0]))

    def cases(self):
        """
        Generator for all test cases in the suite
        """
        return CaseData.discover(self)


    def __eq__(self, other):
        """
        A suite is compared against its filename
        or against its own name (useful for filtering)
        """
        if type(other) == str:
            other_filename, other_ext = os.path.splitext(other)
            
            if other_ext:
                return other == self.filename
            else:
                return other_filename == os.path.splitext(self.filename)[0]
        else:
            return self.filename == other.filename

    
    def has_valid_xml(self):
        """
        Return true if xml could be parsed
        and the root tag is 'suite'
        """
        return (self.tree
                and self.tree.getroot().tag == 'suite')

    @property
    def skip(self):
        """
        Return True if this case should not be run.
        """
        whitelisted = bool(self.name_whitelist and \
                               self.name in self.name_whitelist)

        whitelisted |= bool(self.filename_whitelist and \
                                self in self.filename_whitelist)

        skip = self.root.find('skip') is not None

        return skip and not whitelisted

    @classmethod
    def discover(cls, app):
        """
        Discover suites inside of an application
        """
        # All test suites will be defined by an xml file
        xml_filenames = (filename
                         for filename in app.filenames
                         if filename.endswith('xml'))

        # Discovered suites must contain a valid xml content
        # and at least one test cases
        suites = (suite for suite in (cls(app, filename)
                                      for filename in xml_filenames)
                  if suite.has_valid_xml() and any(suite.cases()))

        
        # Filter suites using the whitelists provided through the
        # command line
        if cls.name_whitelist or cls.filename_whitelist:
            suites = (suite for suite in suites
                      if suite.name in cls.name_whitelist
                      or suite in cls.filename_whitelist)

        return suites


class CaseData(XmlData):
    """
    Test case description data
    """
    whitelist = None

    def __init__(self, suite, root):
        self.suite = suite
        self.root = root


    @property
    def methodname(self):
        """
        Test method according to xml data
        """
        return self.root.find('method').text


    @property
    def skip(self):
        """
        Return True if this case should not be run.
        """
        whitelisted = bool(self.whitelist and self.name in self.whitelist)

        skip = self.root.find('skip') is not None

        return skip and not whitelisted

    @classmethod
    def discover(cls, suite):
        """
        Discover all test cases in a suite
        """
        cases = (cls(suite, tree)
                 for tree in suite.tree.findall('case'))

        if cls.whitelist:
            cases = (case for case in cases
                     if case.name in cls.whitelist)

        return cases


def discover_applications(top_directories,
                          filtering_applications,
                          filtering_suite_names,
                          filtering_suite_files,
                          filtering_cases):
    """
    Discover all applications and filter them properly
    """
    # Configure filtering options
    ApplicationData.whitelist = filtering_applications
    SuiteData.name_whitelist = filtering_suite_names
    SuiteData.filename_whitelist = filtering_suite_files
    CaseData.whitelist = filtering_cases

    # Discover all applications under top directories
    discovered_apps = ApplicationData.discover(top_directories)

    return discovered_apps
