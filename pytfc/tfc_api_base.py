"""Base class used by all pytfc api 'child' classes."""
import logging
from abc import ABCMeta, ABC

logger = logging.getLogger(__name__)


class TfcApiBase:
    """
    Base class for API endpoints.
    """

    __metaclass__ = ABCMeta

    def __init__(self, requestor, org, ws, ws_id):
        """
        TFC/E API 'child' class constructor.
        """
        self._requestor = requestor
        self.org = org
        self.ws = ws
        self.ws_id = ws_id