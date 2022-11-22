#from .client import Client

"""
Entry-point module to instantiate an API client object to
interface with the supported TFC/E API endpoints and resources.
"""
from os import getenv
import logging
import sys
from pytfc.requestor import Requestor
from pytfc.utils import DEFAULT_LOG_LEVEL
from pytfc.exceptions import MissingToken
from pytfc import api
from pytfc import admin_api


class Client:
    """
    Initialize this class to access sub-classes
    for all TFC/E API endpoints and resources.
    """
    _no_org_required_classes = {
        'admin_organizations': admin_api.AdminOrganizations,
        'admin_runs': admin_api.AdminRuns,
        'admin_settings': admin_api.AdminSettings,
        'admin_terraform_versions': admin_api.AdminTerraformVersions,
        'admin_users': admin_api.AdminUsers,
        'admin_workspaces': admin_api.AdminWorkspaces,
        # 'policy_checks': PolicyChecks,
         'organizations': api.Organizations,
        # #'team_membership': TeamMembership, # under construction
        # 'team_tokens': TeamTokens
    }

    _org_required_classes = {
        'workspaces': api.Workspaces,
    }

    def __init__(
        self,
        hostname=None,
        token=None,
        org=None,
        ws=None,
        log_level=DEFAULT_LOG_LEVEL,
        verify=True,
        requestor=Requestor
    ):

        self._logger = logging.getLogger(self.__class__.__name__)
        self._log_level = getattr(logging, log_level.upper())
        self._logger.setLevel(self._log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.debug("Instantiating TFC/E API Client.")

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
            verify=verify,
            log_level=self._log_level
        )
        
        self.org = org
        #self.ws = ws
        #self.ws_id = (self._get_ws_id(self.ws)) if self.org and self.ws else None

        ws_id = (self._get_ws_id(ws)) if org and ws else None

        self._logger.debug("Initializing API classes that do not"
                           " require an `org` to be set...")
        self._init_api_classes(
            self._no_org_required_classes,
            org,
            ws,
            ws_id
        )
        
        self._logger.debug("Initializing API classes that"
                           " require an `org` to be set...")
        if org is not None:
            self._init_api_classes(
                self._org_required_classes,
                org,
                ws,
                ws_id
            )

    # @property
    # def requestor(self):
    #     return self._requestor
        
    # @requestor.setter
    # def requestor(self, requestor):
    #     self._requestor = requestor
    
    def _get_ws_id(self, ws_name):
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.get(path=path).json()['data']['id']
    
    def _init_api_classes(self, classes_dict, org=None, ws=None, ws_id=None):
        """
        Initialize all supported API endpoint classes.
        """
        for cls_name in classes_dict:
            cls = classes_dict[cls_name]
            initialized_cls = cls(
                requestor=self._requestor,
                org=org,
                ws=ws,
                ws_id=ws_id,
                log_level=self._log_level
            )

            self._logger.debug(f"Initializing {cls.__name__}.")
            setattr(self, cls_name, initialized_cls)

    def set_org(self, name):
        """
        Sets Organization (as `org`) on Client object
        and re-initializes all API endpoint classes
        that require an `org` to be set.
        """
        self._logger.debug(f"Setting `org` on client to {name}.")
        self.__setattr__('org', name)
        self._init_api_classes(
            classes_dict=self._org_required_classes,
            org=name
        )
    
    def set_ws(self, name):
        """
        Sets Workspace (as `ws`) on Client object and
        re-initializes all API endpoint classes that
        require an `org` to be set.
        """
        self._logger.debug(f"Setting `ws` on client to {name}.")
        ws_id = self._get_ws_id(name)
        self._logger.debug(f"Setting `ws_id` on client to {ws_id}.")
        self.__setattr__('ws', name)
        self.__setattr__('ws_id', ws_id)
        self._init_api_classes(
            classes_dict=self._org_required_classes,
            ws=name,
            ws_id=ws_id
        )