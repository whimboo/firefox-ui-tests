# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait

from ..base import BaseLib


class Observer(BaseLib):
    """Class to handle observer notifications."""

    # needs clean-up code to remove registered topics
    def __init__(self, marionette_getter):
        print '***** init observer ********'
        BaseLib.__init__(self, marionette_getter)

    def register(self, topics):
        # needs check so we only register once

        self.topics = topics

        """Registers the topics to receive notifications."""
        with self.marionette.using_context('chrome'):
            self.marionette.execute_script("""
                Cu.import("resource://gre/modules/Services.jsm");

                function Observer(aTopics) {
                  this.topics = aTopics;
                  this.register();
                }

                Observer.prototype = {
                  /**
                   * Register all topics
                   */
                  register : function () {
                    this.topics.forEach(aTopic => {
                      Services.obs.addObserver(this, aTopic, false);
                    });
                  },

                  observe : function (aSubject, aTopic, aData) {
                    try {
                      Services.obs.removeObserver(this, aTopic);
                    }
                    catch (e) {}

                    window.alert(aTopic);
                  }
                };

                var observer = new Observer(arguments[0]);

            """, script_args=[self.topics])

    def completed(self):
        with self.marionette.using_context('chrome'):
            self.marionette.execute_script("""
              window.alert(observer);
            """, new_sandbox=False)

        return True
