#from .client import Client

"""
Entry-point module to instantiate an API client object to
interface with the supported TFC/E API endpoints and resources.
"""
from os import getenv
import logging
import sys
from pytfc.requestor import Requestor
from pytfc.exceptions import MissingToken
from pytfc import api
from pytfc import admin_api


class Client:
    """
    Initialize this parent class to access child classes for all TFC/E
    API endpoints and resources. Kind of behaves like a superclass.
    """
    def __init__(
        self,
        hostname=None,
        token=None,
        org=None,
        ws=None,
        log_level='WARNING',
        verify=True,
        requestor=Requestor
    ):
        
        self._logger = logging.getLogger(self.__class__.__name__)
        self._log_level = getattr(logging, log_level.upper())
        self._logger.setLevel(self._log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.debug("Instantiating TFC/E API Client class.")

        if hostname is not None:
            self.hostname = hostname
        elif getenv('TFE_HOSTNAME'):
            self.hostname = getenv('TFE_HOSTNAME')
        else:
            self.hostname = 'app.terraform.io'

        if self.hostname[-1] == '/':
            self.hostname = self.hostname[:-1]
        self._logger.debug(f"Setting hostname to `{self.hostname}`.")

        if token is not None:
            self._logger.debug(f"Setting token directly from argument.")
            self._token = token
        elif getenv('TFE_TOKEN'):
            self._logger.debug(f"Setting token from environment variable.")
            self._token = getenv('TFE_TOKEN')
        else:
            raise MissingToken

        _base_uri_v2 = f'https://{self.hostname}/api/v2'
        _headers = {
            'Authorization': 'Bearer ' + self._token,
            'Content-Type': 'application/vnd.api+json'
        }
        
        self._requestor = requestor(
            headers=_headers,
            base_uri=_base_uri_v2,
            logger=self._logger,
            verify=verify
        )
        
        self.org = org
        self.ws = ws
        self.ws_id = None

        # Admin API
        self.admin_organizations = admin_api.AdminOrganizations(requestor=self._requestor, org=self.org, ws=self.ws)
        self.admin_runs = admin_api.AdminRuns(requestor=self._requestor, org=self.org, ws=self.ws)
        
        # Regular API
        self.organizations = api.Organizations(requestor=self._requestor, org=self.org, ws=self.ws)
        self.workspaces = api.Workspaces(requestor=self._requestor, org=self.org, ws=self.ws)

    @property
    def requestor(self):
        return self._requestor
        
    @requestor.setter
    def requestor(self, requestor):
        self._requestor = requestor