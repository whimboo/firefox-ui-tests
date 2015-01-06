# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from ..base import BaseLib


class Observer(BaseLib):
    """Class to handle observer notifications."""

    def register(self, topics):
        # needs check so we only register once

        if not isinstance(topics, list):
            self.topics = [topics]
        else:
            self.topics = topics

        """Registers the topics to receive notifications."""
        with self.marionette.using_context('chrome'):
            self.marionette.execute_script("""
                Cu.import("resource://gre/modules/Services.jsm");

                function Observer() {}

                Observer.prototype = {
                  /**
                   * Callback for registered observer topics
                   */
                  observe : function (aSubject, aTopic, aData) {
                    try {
                      Services.obs.removeObserver(this, aTopic);
                    }
                    catch (e) {}

                    log('Observed topic: ' + aTopic)
                    // Save off additional data for topic e.g. window id
                  },

                  /**
                   * Register observer topics
                   */
                  register : function (aTopics) {
                    // Remove any old registered topic first
                    this.remove(this.topics);

                    // Register new topics
                    this.topics = aTopics;
                    this.topics.forEach(aTopic => {
                      Services.obs.addObserver(this, aTopic, false);
                    });
                  },

                  /**
                   * Remove observer topics
                   */
                  remove : function (aTopics) {
                    if (!aTopics) {
                      return;
                    }

                    aTopics.forEach(aTopic => {
                      try {
                        Services.obs.removeObserver(this, aTopic);
                      }
                      catch (e) {}
                    });
                  }
                };

                if (!this.observer) {
                  this.observer = new Observer();
                }

                this.observer.register(arguments[0]);
            """, script_args=[self.topics], new_sandbox=False)

    def wait(self, condition):
        with self.marionette.using_context('chrome'):
            return self.marionette.execute_async_script("""
              setTimeout(function () {
                marionetteScriptFinished(true);
              }, 500);
            """, script_args=[condition], new_sandbox=False)
