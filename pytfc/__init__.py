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
from pytfc.exceptions import MissingOrganization
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
        'organizations': api.Organizations,
        'policy_checks': api.PolicyChecks,
        'team_membership': api.TeamMembership,
        'team_tokens': api.TeamTokens
    }

    _org_required_classes = {
        'agent_pools': api.AgentPools,
        'applies': api.Applies,
        'audit_trails': api.AuditTrails,
        'configuration_versions': api.ConfigurationVersions,
        'notification_configurations': api.NotificationConfigurations,
        'oauth_clients': api.OauthClients,
        'oauth_tokens': api.OauthTokens,
        'plan_exports': api.PlanExports,
        'plans': api.Plans,
        'projects': api.Projects,
        'registry_modules': api.RegistryModules,
        'runs': api.Runs,
        'run_task_stages': api.RunTaskStages,
        'run_tasks': api.RunTasks,
        'run_triggers': api.RunTriggers,
        'ssh_keys': api.SSHKeys,
        'state_versions': api.StateVersions,
        'state_version_outputs': api.StateVersionOutputs,
        'team_access': api.TeamAccess,
        'teams': api.Teams,
        'variable_sets': api.VariableSets,
        'workspaces': api.Workspaces,
        'workspace_variables': api.WorkspaceVariables,
        'workspace_resources': api.WorkspaceResources,
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
        self._logger.debug("Instantiating TFC/E API client.")

        if hostname is not None:
            self._logger.debug("Setting hostname from argument.")
            self.hostname = hostname
        elif getenv('TFE_HOSTNAME'):
            self._logger.debug("Setting hostname from environment variable.")
            self.hostname = getenv('TFE_HOSTNAME')
        else:
            self._logger.debug("Setting hostname from package default.")
            self.hostname = 'app.terraform.io'

        if self.hostname[-1] == '/':
            self.hostname = self.hostname[:-1]
        self._logger.debug(f"Setting hostname to `{self.hostname}`.")

        if token is not None:
            self._logger.debug("Setting token from argument.")
            self._token = token
        elif getenv('TFE_TOKEN'):
            self._logger.debug("Setting token from environment variable.")
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

        if org is not None:
            self._logger.debug("Setting org from argument.")
            self.org = org
        elif getenv('TFE_ORG'):
            self._logger.debug("Setting org from environment variable.")
            self.org = getenv('TFE_ORG')
        else:
            self._logger.debug("An org was not set.")
            self.org = org

        if ws is not None:
            self._logger.debug("Setting ws from argument.")
            self.ws = ws
            if self.org is not None:
                self._logger.debug(f"Fetching and setting ws_id from ws argument.")
                self.ws_id = self._get_ws_id(self.ws)
            else:
                self.ws_id = None
        else:
            self._logger.debug("A ws was not set.")
            self.ws = ws
            self.ws_id = None

        self._logger.debug("Initializing API classes that do not"
                           " require an org to be set...")
        self._init_api_classes(
            classes_dict=self._no_org_required_classes,
            org=self.org,
            ws=self.ws,
            ws_id=self.ws_id
        )

        if self.org is not None:
            self._logger.debug("Initializing API classes that"
                    " require an org to be set...")
            self._init_api_classes(
                classes_dict=self._org_required_classes,
                org=self.org, # needed ?
                ws=self.ws, # needed ?
                ws_id=self.ws_id # needed ?
            )
    
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
                org=self.org,
                ws=self.ws,
                ws_id=self.ws_id,
                log_level=self._log_level
            )

            setattr(self, cls_name, initialized_cls)

    def set_org(self, name):
        """
        Sets Organization (as `org`) on Client object
        and re-initializes all API endpoint classes
        that require an `org` to be set.

        Using this method will unset any pre-existing
        Workspace attributes on the Client object.
        """
        self._logger.debug(f"Setting `org` attribute on client to `{name}`.")
        self.org = name
        self.ws = None
        self.ws_id = None
        self._init_api_classes(classes_dict=self._org_required_classes)
    
    def set_ws(self, name):
        """
        Sets Workspace (as `ws`) on Client object and
        re-initializes all API endpoint classes that
        require an `org` to be set.
        """
        if not self.org:
            self._logger.error("Cannot set a Workspace (`ws`) on without an"
                               " Organization (`org`) having already been set.")
            raise MissingOrganization

        self._logger.debug(f"Setting `ws` attribute on client to `{name}`.")
        ws_id = self._get_ws_id(name)
        self._logger.debug(f"Setting `ws_id` attribute on client to `{ws_id}`.")
        self.ws = name
        self.ws_id = ws_id
        self._init_api_classes(classes_dict=self._org_required_classes)