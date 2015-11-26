import os
from mago.test_suite.solaris_notification import SolarisNotificationTestSuite

class NotificationTest(SolarisNotificationTestSuite):
    def notif_test(self, theme=None, position=None):
        self.application.notification_preview(theme, position)

if __name__ == "__main__":
    solaris_notif_test = NotificationTest()
    solaris_notif_test.run()
