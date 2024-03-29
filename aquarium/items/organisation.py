# -*- coding: utf-8 -*-
import json
from ..item import Item


class Organisation(Item):
    """
    This class describes an Organisation object child of Item class.
    """

    def get_member_by_email(self, email):
        """
        Get an exising member of the organisation by his/her email

        :returns:   User object
        :rtype:     :class:`~aquarium.items.user.User`
        """
        member = None
        members = self.get_all_members()
        filtered = [member for member in members if member.data.email == email]

        if (len(filtered) > 0):
            member = filtered[0]

        return member

    def get_all_members(self, limit=200, offset=None):
        """
        Gets all members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.user.User`
        """
        params = {}
        if (limit is not None):
            params['limit'] = limit
        if (offset is not None):
            params['offset'] = offset

        result=self.do_request('GET', 'organisations/{0}/members/all'.format(self._key), params=params)
        result=[self.parent.user(user) for user in result]
        return result

    def get_active_members(self, limit=200, offset=None):
        """
        Gets all active members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.user.User`
        """
        params = {}
        if (limit is not None):
            params['limit'] = limit
        if (offset is not None):
            params['offset'] = offset

        result = self.do_request(
            'GET', 'organisations/{0}/members/active'.format(self._key), params=params)
        result=[self.parent.user(user) for user in result]
        return result

    def get_inactive_members(self, limit=200, offset=None):
        """
        Gets all inactive members of the organisation

        :param      limit:   Maximum limit number of returned members
        :type       limit:   integer
        :param      offset:  Number of skipped members. Used for pagination
        :type       offset:  integer

        :returns:   List of User object
        :rtype:     List of :class:`~aquarium.items.user.User`
        """
        params = {}
        if (limit is not None):
            params['limit'] = limit
        if (offset is not None):
            params['offset'] = offset

        result = self.do_request(
            'GET', 'organisations/{0}/members/inactive'.format(self._key), params=params)
        result=[self.parent.user(user) for user in result]
        return result

    def create_member(self, email, name=None):
        """
        Create a new member in your organisation

        :param      email:  The email of the new member
        :type       email:  string
        :param      name:  The name of the new member
        :type       name:  string, optional

        :returns:   User object
        :rtype:     :class:`~aquarium.items.user.User`
        """

        payload = dict(email=email, name=name)
        data = dict(data=payload)
        member = self.do_request(
            'POST', 'organisations/{0}/createMember'.format(self._key), data=json.dumps(data))

        member = self.parent.cast(member)
        return member

    def get_suborganisations(self, limit=200, offset=None):
        """
        Gets all suborganisations

        :param      limit:   Maximum limit number of returned organisations
        :type       limit:   integer
        :param      offset:  Number of skipped organisations. Used for pagination
        :type       offset:  integer

        :returns:   List of Organisation object
        :rtype:     List of :class:`~aquarium.items.organisation.Organisation`
        """
        params = {}
        if (limit is not None):
            params['limit'] = limit
        if (offset is not None):
            params['offset'] = offset

        result = self.do_request(
            'GET', 'organisations/{0}/suborganisations'.format(self._key), params=params)
        result = [self.parent.organisation(
            organisation) for organisation in result]
        return result
