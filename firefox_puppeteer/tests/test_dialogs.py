# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from firefox_ui_harness.testcase import FirefoxTestCase

from firefox_puppeteer.ui.dialogs import BaseDialog


class TestBaseDialog(FirefoxTestCase):

    def tearDown(self):
        try:
            self.windows.close_all([self.browser])
        finally:
            FirefoxTestCase.tearDown(self)

    def test_basic(self):
        def opener(win):
            self.marionette.execute_script("""
              let updatePrompt = Components.classes["@mozilla.org/updates/update-prompt;1"]
                                 .createInstance(Components.interfaces.nsIUpdatePrompt);
              updatePrompt.checkForUpdates();
            """)

        dialog = self.browser.open_window(callback=opener, expected_window_class=BaseDialog)
        print dialog.title
        print dialog.accept
