"""Base module used by all pytfc api 'child' modules."""
import logging
import sys
from abc import ABCMeta

#logger = logging.getLogger(__name__)


class TfcApiBase:
    """
    Base class for TFC/E API endpoints.
    """

    __metaclass__ = ABCMeta

    def __init__(self, requestor, org, ws, ws_id, log_level):
        """
        TFC/E API 'child' class constructor.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))

        self._requestor = requestor
        self.org = org
        self.ws = ws
        self.ws_id = ws_id
        self.log_level = log_level