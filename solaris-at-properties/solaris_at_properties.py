import os
from mago.test_suite.solaris_at_properties import SolarisAtPropertiesTestSuite

class VerifyAtProperties(SolarisAtPropertiesTestSuite):
    def verify_pref_app(self):
        self.application.chk_pref_app()

    def verify_keyboard_a11y(self):
        self.application.chk_keyboard_a11y()

    def verify_a11y_enabled(self):
        self.application.chk_enable_a11y()

    def verify_mouse_a11y(self):
        self.application.chk_mouse_a11y()


if __name__ == "__main__":
    solaris_at_properties_test = VerifyAtProperties()
    solaris_at_properties_test.run()
