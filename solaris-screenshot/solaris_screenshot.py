import os
from mago.test_suite.solaris_screenshot import SolarisScreenshotTestSuite

class TakeScreenshot(SolarisScreenshotTestSuite):
    def solaris_screenshot(self, option=None, effect=None, delay=None, filename=None):
        self.application.take_screenshot(option,effect,delay)
        self.application.save_to_file(filename)

        file_path = os.getenv('HOME') + '/' + filename
        
        if os.access(file_path, os.F_OK):
            os.remove(file_path) 
        else:
            raise AssertionError('Screenshot ' + file_path + ' was not created')

        self.application.open()

if __name__ == "__main__":
    solaris_screenshot_test = TakeScreenshot()
    solaris_screenshot_test.run()
