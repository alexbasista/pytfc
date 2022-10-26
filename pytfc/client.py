"""
Entry-point module to instantiate an API client object to
interface with the supported TFC/E API endpoints and resources.
"""
import os
import logging
import sys
from .exceptions import MissingToken
from .requestor import Requestor
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
from .registry_modules import RegistryModules
from .teams import Teams
from .team_tokens import TeamTokens
from .team_access import TeamAccess
from .notification_configurations import NotificationConfigurations
from .run_triggers import RunTriggers
from .workspace_resources import WorkspaceResources
from .run_tasks import RunTasks
from .run_task_stages import RunTaskStages
from .variable_sets import VariableSets

class Client:
    """
    Initialize this parent class to access child classes for all TFC/E
    API endpoints and resources. Kind of behaves like a superclass.
    """
    def __init__(self, log_level='WARNING', **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._log_level = getattr(logging, log_level.upper())
        self._logger.setLevel(self._log_level)
        self._logger.addHandler(logging.StreamHandler(sys.stdout))
        self._logger.debug("Instantiating TFC/E API Client class.")

        if kwargs.get('hostname'):
            self.hostname = kwargs.get('hostname')
        elif os.getenv('TFE_HOSTNAME'):
            self.hostname = os.getenv('TFE_HOSTNAME')
        else:
            self.hostname = 'app.terraform.io'
        self._logger.debug(f"Setting hostname to `{self.hostname}`.")

        if kwargs.get('token'):
            self._token = kwargs.get('token')
        elif os.getenv('TFE_TOKEN'):
            self._token = os.getenv('TFE_TOKEN')
        else:
            raise MissingToken

        self._base_uri_v2 = 'https://{}/api/v2'.format(self.hostname)
        self._headers = {
            'Authorization': 'Bearer ' + self._token,
            'Content-Type': 'application/vnd.api+json'
        }
        self._requestor = Requestor(client=self, headers=self._headers)
        self.org = kwargs.get('org')
        self.ws = kwargs.get('ws')
        self.ws_id = None

        if kwargs.get('org') and not kwargs.get('ws'):
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
            self.state_versions = StateVersions(client=self)
            self.agent_pools = AgentPools(client=self)
            self.ssh_keys = SSHKeys(client=self)
            self.applies = Applies(client=self)
            self.registry_modules = RegistryModules(client=self)
            self.teams = Teams(client=self)
            self.team_tokens = TeamTokens(client=self)
            self.team_access = TeamAccess(client=self)
            self.notification_configurations = NotificationConfigurations(client=self)
            self.run_triggers = RunTriggers(client=self)
            self.workspace_resources = WorkspaceResources(client=self)
            self.run_tasks = RunTasks(client=self)
            self.run_task_stages = RunTaskStages(client=self)
            self.variable_sets = VariableSets(client=self)
        elif kwargs.get('org') and kwargs.get('ws'):
            self.organizations = Organizations(client=self)
            self.workspaces = Workspaces(client=self, ws=kwargs.get('ws'))
            self.ws_id = self.workspaces.get_ws_id(name=kwargs.get('ws'))
            self.oauth_clients = OauthClients(client=self)
            self.oauth_tokens = OauthTokens(client=self)
            self.workspace_variables = WorkspaceVariables(client=self)
            self.configuration_versions = ConfigurationVersions(client=self)
            self.runs = Runs(client=self)
            self.plans = Plans(client=self)
            self.plan_exports = PlanExports(client=self)
            self.applies = Applies(client=self)
            self.state_versions = StateVersions(client=self)
            self.agent_pools = AgentPools(client=self)
            self.ssh_keys = SSHKeys(client=self)
            self.registry_modules = RegistryModules(client=self)
            self.teams = Teams(client=self)
            self.team_tokens = TeamTokens(client=self)
            self.team_access = TeamAccess(client=self)
            self.notification_configurations = NotificationConfigurations(client=self)
            self.run_triggers = RunTriggers(client=self)
            self.workspace_resources = WorkspaceResources(client=self)
            self.run_tasks = RunTasks(client=self)
            self.run_task_stages = RunTaskStages(client=self)
            self.variable_sets = VariableSets(client=self)
        elif not kwargs.get('org') and kwargs.get('ws'):
            self._logger.warning("An `org` has not been set.")
            self._logger.warning("An `org` must be set before or at the same time as a `ws`.")
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
        self.agent_pools = AgentPools(client=self)
        self.workspace_variables = WorkspaceVariables(client=self)
        self.configuration_versions = ConfigurationVersions(client=self)
        self.ssh_keys = SSHKeys(client=self)
        self.state_versions = StateVersions(client=self)
        self.runs = Runs(client=self)
        self.plans = Plans(client=self)
        self.applies = Applies(client=self)
        self.plan_exports = PlanExports(client=self)
        self.registry_modules = RegistryModules(client=self)
        self.teams = Teams(client=self)
        self.team_tokens = TeamTokens(client=self)
        self.team_access = TeamAccess(client=self)
        self.notification_configurations = NotificationConfigurations(client=self)
        self.run_triggers = RunTriggers(client=self)
        self.workspace_resources = WorkspaceResources(client=self)
        self.run_tasks = RunTasks(client=self)
        self.run_task_stages = RunTaskStages(client=self)
        self.variable_sets = VariableSets(client=self)

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
