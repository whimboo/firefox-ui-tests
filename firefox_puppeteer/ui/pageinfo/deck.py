# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette_driver import By, Wait

from ...base import UIBaseLib


class Deck(UIBaseLib):

    def _create_panel_for_id(self, panel_id):
        """Creates an instance of :class:`Panel` for the specified panel id.

        :param panel_id: The ID of the panel to create an instance of.

        :returns: :class:`Panel` instance
        """
        mapping = {'feedPanel': FeedPanel,
                   'generalPanel': GeneralPanel,
                   'mediaPanel': MediaPanel,
                   'permPanel': PermissionsPanel,
                   'securityPanel': SecurityPanel
                   }

        panel = self.element.find_element(By.ID, panel_id)
        return mapping.get(panel_id, Panel)(lambda: self.marionette, self.window, panel)

    # Properties for visual elements of the deck #

    @property
    def feed(self):
        """The :class:`FeedPanel` instance for the feed panel.

        :returns: :class:`FeedPanel` instance.
        """
        return self._create_panel_for_id('feedPanel')

    @property
    def general(self):
        """The :class:`GeneralPanel` instance for the general panel.

        :returns: :class:`GeneralPanel` instance.
        """
        return self._create_panel_for_id('generalPanel')

    @property
    def media(self):
        """The :class:`MediaPanel` instance for the media panel.

        :returns: :class:`MediaPanel` instance.
        """
        return self._create_panel_for_id('mediaPanel')

    @property
    def panels(self):
        """List of all the :class:`Panel` instances of the current deck.

        :returns: List of :class:`Panel` instances.
        """
        panels = self.marionette.execute_script("""
          let deck = arguments[0];
          let panels = [];

          for (let index = 0; index < deck.children.length; index++) {
            panels.push(deck.children[index].id);
          }

          return panels;
        """, script_args=[self.element])

        return [self._create_panel_for_id(panel) for panel in panels]

    @property
    def permissions(self):
        """The :class:`PermissionsPanel` instance for the permissions panel.

        :returns: :class:`PermissionsPanel` instance.
        """
        return self._create_panel_for_id('permPanel')

    @property
    def security(self):
        """The :class:`SecurityPanel` instance for the security panel.

        :returns: :class:`SecurityPanel` instance.
        """
        return self._create_panel_for_id('securityPanel')

    # Properties for helpers when working with the deck #

    @property
    def selected_index(self):
        """The index of the currently selected panel.

        :return: Index of the selected panel.
        """
        return int(self.element.get_attribute('selectedIndex'))

    @property
    def selected_panel(self):
        """A :class:`Panel` instance of the currently selected panel.

        :returns: :class:`Panel` instance.
        """
        return self.panels[self.selected_index]

    # Methods for helpers when working with the deck #

    def select(self, panel):
        """Selects the specified panel via the tab element.

        :param panel: The panel to select.

        :returns: :class:`Panel` instance of the selected panel.
        """
        panel.tab.click()
        Wait(self.marionette).until(lambda _: self.selected_panel == panel)

        return panel


class Panel(UIBaseLib):

    def __eq__(self, other):
        return self.element.get_attribute('id') == other.element.get_attribute('id')

    @property
    def tab(self):
        """The DOM element which represents the corresponding tab element at the top.

        :returns: Reference to the tab element.
        """
        name = self.element.get_attribute('id').split('Panel')[0]
        return self.window.window_element.find_element(By.ID, name + 'Tab')


class FeedPanel(Panel):
    pass


class GeneralPanel(Panel):
    pass


class MediaPanel(Panel):
    pass


class PermissionsPanel(Panel):
    pass


class SecurityPanel(Panel):

    @property
    def domain(self):
        """The DOM element which represents the domain textbox.

        :returns: Reference to the textbox element.
        """
        return self.element.find_element(By.ID, 'security-identity-domain-value')

    @property
    def owner(self):
        """The DOM element which represents the owner textbox.

        :returns: Reference to the textbox element.
        """
        return self.element.find_element(By.ID, 'security-identity-owner-value')

    @property
    def verifier(self):
        """The DOM element which represents the verifier textbox.

        :returns: Reference to the textbox element.
        """
        return self.element.find_element(By.ID, 'security-identity-verifier-value')

    @property
    def view_certificate(self):
        """The DOM element which represents the view certificate button.

        :returns: Reference to the button element.
        """
        return self.element.find_element(By.ID, 'security-view-cert')

    @property
    def view_cookies(self):
        """The DOM element which represents the view cookies button.

        :returns: Reference to the button element.
        """
        return self.element.find_element(By.ID, 'security-view-cookies')

    @property
    def view_passwords(self):
        """The DOM element which represents the view passwords button.

        :returns: Reference to the button element.
        """
        return self.element.find_element(By.ID, 'security-view-password')
