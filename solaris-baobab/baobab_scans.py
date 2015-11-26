# -*- coding: utf-8 -*-
import os
from time import time, gmtime, strftime

from mago.test_suite.baobab import BaobabTestSuite 

class BaobabScans(BaobabTestSuite):
   
    def baobab_scan_folder(self):
        dir_path = ('%s/' % (os.path.join(self.get_test_dir())))
        self.application.baobab_scan_folder(dir_path)
    
    def baobab_scan_home_directory(self):
        self.application.baobab_scan_home()
          
    def baobab_scan_filesystem(self):
        self.application.baobab_scan_filesystem()
    
if __name__ == "__main__":
    baobab_test =  BaobabScans()
    baobab_test.run()
