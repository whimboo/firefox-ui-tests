# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from ..base import BaseLib


class Observer(BaseLib):
    """Class to handle observer notifications."""

    # needs clean-up code to remove registered topics
    def __init__(self, client_getter, *topics):
        BaseLib.__init__(self, client_getter)

        self.topics = topics
        self.register()

    def register(self):
        # needs check so we only register once

        """Registers the topics to receive notifications."""
        with self.client.using_context('chrome'):
            self.client.execute_script("""
                var topics = arguments;
                window.alert(topics);
            """, script_args=[self.topics])

    def waitFor(self):
        pass
