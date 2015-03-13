# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By

from windows import BaseWindow


class BaseDialog(BaseWindow):
    """Base class for any kind of chrome dialog."""

    def __init__(self, *args, **kwargs):
        BaseWindow.__init__(self, *args, **kwargs)

    @property
    def title(self):
        """Gets the title of the dialog.

        :returns: Title of the dialog.
        """
        return BaseWindow.title.fget(self)
        # this.getElement({type: "info_title"}).getNode().textContent;

    @property
    def accept(self):
        return self.marionette.find_element(By.ANON_ATTRIBUTE, {'dlgtype': 'accept'})
