# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from ..base import BaseLib


class Observer(BaseLib):
    """Class to handle observer notifications."""

    def __init__(self, *topics):
        self.topics = topics


    def waitFor(self):
        pass
