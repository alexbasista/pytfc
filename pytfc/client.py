"""
Entry-point module to initialize and configure a client object 
to interface with the supported TFC/E API endpoints and resources.
"""
import os
#import sys
from pytfc.exceptions import MissingToken
from pytfc.requestor import Requestor
from pytfc.organizations import Organizations
from pytfc.workspaces import Workspaces
from pytfc.oauth_clients import OauthClients
from pytfc.oauth_tokens import OauthTokens
from pytfc.workspace_variables import WorkspaceVariables
from pytfc.configuration_versions import ConfigurationVersions
from pytfc.runs import Runs
from pytfc.plan_exports import PlanExports
from pytfc.plans import Plans
from pytfc.applies import Applies

class Client(object):
    """
    Initialize this parent class to access child classes for all TFC/E
    API endpoints and resources. Kind of behaves like a superclass.
    """
    def __init__(self, **kwargs):
        if os.getenv('TFE_HOSTNAME'):
            self.hostname = os.getenv('TFE_HOSTNAME')
        elif kwargs.get('hostname'):
            self.hostname = kwargs.get('hostname')
        else:
            self.hostname = 'app.terraform.io'

        if os.getenv('TFC_TOKEN'):
            self.token = os.getenv('TFC_TOKEN')
        elif os.getenv('TFE_TOKEN'):
            self.token = os.getenv('TFE_TOKEN')
        else:
            if kwargs.get('token'):
                self.token = kwargs.get('token')
            else:
                raise MissingToken

        self._base_uri_v2 = 'https://{}/api/v2'.format(self.hostname)
        self._headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/vnd.api+json'
        }
        self._requestor = Requestor(headers=self._headers)
        self.org = kwargs.get('org')
        self.ws = kwargs.get('ws')

        if kwargs.get('org') and not kwargs.get('ws'):
            self.organizations = Organizations(client=self)
            self.workspaces = Workspaces(client=self)
            self.oauth_clients = OauthClients(client=self)
            self.oauth_tokens = OauthTokens(client=self)
            self.workspace_variables = None
            self.configuration_versions = None
            self.runs = None
            self.plans = None
            self.plan_exports = None
            self.applies = None
        elif kwargs.get('org') and kwargs.get('ws'):
            self.organizations = Organizations(client=self)
            self.workspaces = Workspaces(client=self)
            self.oauth_clients = OauthClients(client=self)
            self.oauth_tokens = OauthTokens(client=self)
            self.workspace_variables = WorkspaceVariables(client=self)
            self.configuration_versions = ConfigurationVersions(client=self)
            self.runs = Runs(client=self)
            self.plans = Plans(client=self)
            self.plan_exports = PlanExports(client=self)
            self.applies = Applies(client=self)
        else:
            self.organizations = Organizations(client=self)

    def set_org(self, name):
        """
        Method to set 'org' attribute on Client object if it
        was not specified when Client object was instantiated.
        """
        self.org = name
        self.workspaces = Workspaces(client=self)
        self.oauth_clients = OauthClients(client=self)
        self.oauth_tokens = OauthTokens(client=self)

    def set_ws(self, name):
        """
        Method to set 'ws' attribute on Client object if it
        was not specified when Client object was instantiated.
        """
        self.ws = name
        self.workspaces = Workspaces(client=self)
        self.workspace_variables = WorkspaceVariables(client=self)
        self.configuration_versions = ConfigurationVersions(client=self)
        self.runs = Runs(client=self)
        self.plans = Plans(client=self)
        self.plan_exports = PlanExports(client=self)
        self.applies = Applies(client=self)
