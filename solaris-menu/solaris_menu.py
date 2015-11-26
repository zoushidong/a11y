# -*- coding: utf-8 -*-


from mago.test_suite.solaris_menu import SolarisMenuTestSuite

class SolarisMenuTest(SolarisMenuTestSuite):
       
    def testOpenMenu(self, menuitem=None, windowname=None, closetype=None, closename=None):
        self.application.set_name(windowname)
        self.application.set_close_type(closetype)
        self.application.set_close_name(closename)
        self.application.open_and_check_menu_item(menuitem)
        
if __name__ == "__main__":
    solaris_menu_test = SolarisMenuTest()
    solaris_menu_test.run()
