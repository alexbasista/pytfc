"""
Entry-point module to instantiate an API client object to
interface with the supported TFC/E API endpoints and resources.
"""
from os import getenv
import logging
import sys
from .exceptions import MissingToken
from .organizations import Organizations
from .workspaces import Workspaces
from .oauth_clients import OauthClients
from .oauth_tokens import OauthTokens
from .workspace_variables import WorkspaceVariables
from .configuration_versions import ConfigurationVersions
from .runs import Runs
from .plan_exports import PlanExports
from .plans import Plans
from .applies import Applies
from .state_versions import StateVersions
from .agent_pools import AgentPools
from .ssh_keys import SSHKeys
from .policy_checks import PolicyChecks
from .registry_modules import RegistryModules
from .teams import Teams
from .team_tokens import TeamTokens
from .team_access import TeamAccess
from .team_membership import TeamMembership
from .notification_configurations import NotificationConfigurations
from .run_triggers import RunTriggers
from .workspace_resources import WorkspaceResources
from .run_tasks import RunTasks
from .run_task_stages import RunTaskStages
from .variable_sets import VariableSets
from .admin_organizations import AdminOrganizations
from .admin_terraform_versions import AdminTerraformVersions
from .admin_settings import AdminSettings
from .admin_runs import AdminRuns
from .admin_users import AdminUsers
from .admin_workspaces import AdminWorkspaces
#from .requestor import Requestor

# Constants
DEFAULT_LOG_LEVEL='WARNING'
DEFAULT_VERIFY=True


class Client:
    """
    Initialize this parent class to access child classes for all TFC/E
    API endpoints and resources. Kind of behaves like a superclass.
    """

    _no_org_required = {
        'admin_organizations': AdminOrganizations,
        'admin_runs': AdminRuns,
        'admin_settings': AdminSettings,
        'admin_terraform_versions': AdminTerraformVersions,
        'admin_users': AdminUsers,
        'admin_workspaces': AdminWorkspaces,
        'policy_checks': PolicyChecks,
        'organizations': Organizations,
        #'team_membership': TeamMembership, # under construction
        'team_tokens': TeamTokens
    }

    _org_required = {
        #'agent_pools': AgentPools,
        #'oauth_clients': OauthClients,
        #'oauth_tokens': OauthTokens,
        #'registry_modules': RegistryModules,
        #'ssh_keys': SSHKeys,
        #'teams': Teams,
    }

    _org_and_ws = {
        #'applies': Applies,
        #'configuration_versions': ConfigurationVersions,
        #'notification_configurations': NotificationConfigurations,
        #'plan_exports': PlanExports,
        #'plans': Plans,
        #'run_task_stages': RunTaskStages,
        #'run_tasks': RunTasks,
        #'run_triggers': RunTriggers,
        #'runs': Runs,
        #'state_versions': StateVersions,
        #'team_access': TeamAccess,
        #'variable_sets': VariableSets,
        #'workspace_resources': WorkspaceResources,
        #'workspace_variables': WorkspaceVariables,
        #'workspaces': Workspaces
    }
    
    def __init__(self, hostname=None, token=None, org=None, ws=None,
        log_level=DEFAULT_LOG_LEVEL, verify=True
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

        self._base_uri_v2 = f'https://{self.hostname}/api/v2'
        self._headers = {
            'Authorization': 'Bearer ' + self._token,
            'Content-Type': 'application/vnd.api+json'
        }
        self._verify = verify
        
        #self._requestor = Requestor(client=self, headers=self._headers)
        
        self.org = org
        self.ws = ws
        self.ws_id = None

        self.organizations = None
        self.workspaces = None
        self.oauth_clients = None
        self.oauth_tokens = None
        self.workspace_variables = None
        self.configuration_versions = None
        self.runs = None
        self.plans = None
        self.plan_exports = None
        self.applies = None
        self.state_versions = None
        self.agent_pools = None
        self.ssh_keys = None
        self.applies = None
        self.registry_modules = None
        self.teams = None
        self.team_tokens = None
        self.team_access = None
        self.notification_configurations = None
        self.run_triggers = None
        self.workspace_resources = None
        self.run_tasks = None
        self.run_task_stages = None
        self.variable_sets = None
        self.admin_organizations = None
        self.admin_terraform_versions = None
        self.admin_settings = None
        self.admin_runs = None
        self.admin_users = None
        self.admin_workspaces = None

        self._logger.debug(f"Initializing child classes that do not require an `org`...")
        self._init_child_classes(self._no_org_required, org=self.org, ws=None)
        self._logger.debug(f"Initializing child classes that require an `org`...")
        self._init_child_classes(self._org_required, org=self.org, ws=None)
        self._logger.debug(f"Initializing child classes that require an `org` and `ws`...")
        self._init_child_classes(self._org_and_ws, org=self.org, ws=self.ws)
    
    def _init_child_classes(self, classes_dict, org, ws=None):
        """
        Method to initialize child classes for all
        TFC/E API endpoints.
        """
        for child_class_name in classes_dict:
            child_class = classes_dict[child_class_name]
            if ws is not None:
                initialized_class = child_class(
                    self._headers,
                    self._base_uri_v2,
                    self.org,
                    self.ws,
                    self._log_level,
                    self._verify
                )
            else:
                initialized_class = child_class(
                    self._headers,
                    self._base_uri_v2,
                    self.org,
                    self._log_level,
                    self._verify
                )
  
            self._logger.debug(f"Initializing {child_class.__name__}...")
            setattr(self, child_class_name, initialized_class)

    def set_org(self, name):
        """
        Method to set 'org' attribute on Client object if it
        was not specified when Client object was instantiated.
        """
        self._init_child_classes(org=name)
        
    def set_ws(self, name):
        """
        Method to set 'ws' attribute on Client object if it
        was not specified when Client object was instantiated.
        """
        if not self.org:
            self._logger.error("An `org` has not been set.")
        
        self.ws = name
        self.workspaces = Workspaces(client=self, ws=name)
        self.ws_id = self.workspaces.get_ws_id(name=name)
        self.workspace_variables = WorkspaceVariables(client=self)
        self.configuration_versions = ConfigurationVersions(client=self)
        self.runs = Runs(client=self)
        self.plans = Plans(client=self)
        self.plan_exports = PlanExports(client=self)
        self.applies = Applies(client=self)
        self.state_versions = StateVersions(client=self)
        self.team_access = TeamAccess(client=self)
        self.notification_configurations = NotificationConfigurations(client=self)
        self.run_triggers = RunTriggers(client=self)
        self.workspace_resources = WorkspaceResources(client=self)
        self.run_tasks = RunTasks(client=self)
        self.run_task_stages = RunTaskStages(client=self)
        self.variable_sets = VariableSets(client=self)
