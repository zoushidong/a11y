# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.solaris_archive_manager import SolarisArchiveManagerTestSuite

class SolarisArchiveManagerTests(SolarisArchiveManagerTestSuite):
    def test_archive(self, file_path, tag):
        path = os.path.join(self.get_test_dir(), file_path)
        self.application.create_archive(path, tag)
        self.application.set_name('frm' + self.application.ARCH_NAME)
        self.application.close()
        """
        Remove the archive file created in previous method
        """
        filepath = os.getenv('HOME') + '/' + self.application.ARCH_NAME
        if os.access(filepath, os.F_OK):
            os.remove(filepath)
        else:
            raise AssertionError('Archive file ' + self.application.ARCH_NAME + ' was not created')
        self.application.set_name(self.application.WINDOW)
        self.application.open()

    def test_extraction(self, file_path):
        path = os.path.join(self.get_test_dir(), file_path)
        self.application.open_archive(path)
        self.application.set_name('frm' + self.application.FILE_NAME + '*')
        self.application.close()
        self.application.set_name(self.application.WINDOW)
        self.application.open()

if __name__ == "__main__":
    solaris_archivemanager_test = SolarisArchiveManagerTests()
    solaris_archivemanager_test.run()
