# -*- coding: utf-8 -*-
import datetime
import pytz
import logging
logger = logging.getLogger(__name__)


class Utils():
    """
    This class is a utility class.
    """

    @staticmethod
    def duration(days = 0, hours = 0, minutes = 0):
        """
        Generate an ISO 8601 duration string.

        :param      days:     The number of days to add
        :type       days:     number
        :param      hours:    The number of hours to add
        :type       hours:    number
        :param      minutes:  The number of minutes to add
        :type       minutes:  number

        :returns:   ISO 8601 duration string
        :rtype:     string
        """
        return 'P{days}{time}{hours}{minutes}'.format(
            days='{days}D'.format(days=days) if days > 0 else '',
            time='T' if hours > 0 or minutes > 0 else '',
            hours='{hours}H'.format(hours=hours) if hours > 0 else '',
            minutes='{minutes}M'.format(minutes=minutes) if minutes > 0 else '')

    @staticmethod
    def date(date=None):
        """
        Generate an ISO 8601 date string.

        :param      date:     The date to convert. If not defined, the current date & time will be used
        :type       date:     datetime, optional

        :returns:   ISO 8601 date string
        :rtype:     string
        """

        if date == None:
            date = datetime.datetime.now()

        if isinstance(date, datetime.datetime):
            date = date.astimezone(pytz.UTC)

        return date.isoformat(timespec='milliseconds')
