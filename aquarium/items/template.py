# -*- coding: utf-8 -*-
from .. import URL_CONTENT_TYPE
from ..item import Item
import logging
logger=logging.getLogger(__name__)


class Template(Item):
    """
    This class describes a Template object child of Item class.
    """

    def apply(self):
        """
        Apply the template on all its items.

        :returns:   List of applied items
        :rtype:     list
        """
        logger.debug('Apply template %s', self._key)
        result=self.do_request('POST', 'templates/'+str(self._key)+'/apply', headers=URL_CONTENT_TYPE)
        result=self.parent.cast(result)
        return result
