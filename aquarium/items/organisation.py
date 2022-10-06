# -*- coding: utf-8 -*-
from ..item import Item


class Organisation(Item):
    """
    This class describes an Organisation object child of Item class.
    """

    def get_all_members(self):
        """
        Gets all members of the organisation

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.task.User`
        """

        result=self.do_request('GET', 'organisations/{0}/members/all'.format(self._key))
        result=[self.parent.user(user) for user in result]
        return result

    def get_active_members(self):
        """
        Gets all active members of the organisation

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.task.User`
        """

        result=self.do_request('GET', 'organisations/{0}/members/active'.format(self._key))
        result=[self.parent.user(user) for user in result]
        return result

    def get_inactive_members(self):
        """
        Gets all inactive members of the organisation

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.task.User`
        """

        result=self.do_request('GET', 'organisations/{0}/members/inactive'.format(self._key))
        result=[self.parent.user(user) for user in result]
        return result
