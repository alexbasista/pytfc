"""
Entry-point module to instantiate an API client object to
interface with the supported TFC/E API endpoints and resources.
"""
from os import getenv
import logging
import sys
from typing import Optional, Dict, Type, Any, Union

from pytfc.requestor import Requestor
from pytfc.utils import DEFAULT_LOG_LEVEL
from pytfc.exceptions import MissingToken, MissingOrganization
from pytfc import api
from pytfc import admin_api


class Client:
    """
    Main client for interacting with Terraform Cloud/Enterprise API.
    
    This client provides access to all TFC/E API endpoints through organized
    sub-clients. It handles authentication, SSL verification, and automatic
    initialization of API endpoint classes.
    
    Args:
        hostname: TFC/E hostname without leading 'https://' (defaults to 'app.terraform.io' for Terraform Cloud)
        token: API token for authentication (can also use TFE_TOKEN env var)
        org: Organization name (can also use TFE_ORG env var)
        ws: Workspace name (requires org to be set)
        log_level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        verify: SSL certificate verification (True/False or path to CA bundle)
        requestor: HTTP requestor class (for testing/customization)
    
    Environment Variables:
        TFE_HOSTNAME: Default hostname if not provided
        TFE_TOKEN: API token if not provided as argument
        TFE_ORG: Organization name if not provided as argument
    
    Raises:
        MissingToken: If no API token is provided via argument or environment
        MissingOrganization: If workspace is set without an organization
    
    Examples:
        Basic usage with environment variables:
        >>> client = pytfc.Client()
        
        Explicit configuration:
        >>> client = pytfc.Client(
        ...     hostname='tfe.company.com',
        ...     token='your-api-token',
        ...     org='my-org',
        ...     ws='my-workspace'
        ... )
        
        Access API endpoints:
        >>> workspaces = client.workspaces.list()
        >>> runs = client.runs.list()
    
    Attributes:
        hostname: The TFC/E hostname being used
        org: Current organization name (if set)
        ws: Current workspace name (if set)  
        ws_id: Current workspace ID (if workspace is set)
        
        # API endpoint clients (available after initialization):
        organizations: Organization management
        workspaces: Workspace management
        runs: Run management
        variables: Variable management
        # ... and many more (see class dictionaries)
    """
    
    _no_org_required_classes: Dict[str, Type[Any]] = {
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

    _org_required_classes: Dict[str, Type[Any]] = {
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
        hostname: Optional[str] = None,
        token: Optional[str] = None,
        org: Optional[str] = None,
        ws: Optional[str] = None,
        log_level: str = DEFAULT_LOG_LEVEL,
        verify: Union[bool, str] = True,
        requestor: Type[Requestor] = Requestor
    ) -> None:
        """
        Initialize the TFC/E API client.
        
        Sets up authentication, configures the HTTP requestor, and initializes
        all available API endpoint clients based on the provided configuration.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self._log_level = getattr(logging, log_level.upper())
        self._logger.setLevel(self._log_level)
        
        # Only add handler if none exists to avoid duplicates
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
            
        self._logger.debug("Instantiating TFC/E API client.")

        # Set hostname with fallback chain
        self.hostname = self._resolve_hostname(hostname)
        self._logger.debug(f"Using hostname: {self.hostname}")

        # Set token (required)
        self._token = self._resolve_token(token)

        # Initialize HTTP requestor
        self._requestor = self._create_requestor(requestor, verify)

        # Set organization (optional)
        self.org = self._resolve_organization(org)

        # Set workspace (optional, requires org)
        self.ws, self.ws_id = self._resolve_workspace(ws)

        # Initialize API endpoint classes
        self._initialize_api_clients()

    def _resolve_hostname(self, hostname: Optional[str]) -> str:
        """Resolve hostname from argument, environment, or default."""
        if hostname is not None:
            self._logger.debug("Setting hostname from argument.")
            resolved_hostname = hostname
        elif getenv('TFE_HOSTNAME'):
            self._logger.debug("Setting hostname from environment variable.")
            resolved_hostname = getenv('TFE_HOSTNAME')
        else:
            self._logger.debug("Setting hostname from package default.")
            resolved_hostname = 'app.terraform.io'

        # Clean up trailing slash
        if resolved_hostname.endswith('/'):
            resolved_hostname = resolved_hostname[:-1]
            
        return resolved_hostname

    def _resolve_token(self, token: Optional[str]) -> str:
        """Resolve API token from argument or environment."""
        if token is not None:
            self._logger.debug("Setting token from argument.")
            return token
        elif getenv('TFE_TOKEN'):
            self._logger.debug("Setting token from environment variable.")
            return getenv('TFE_TOKEN')
        else:
            raise MissingToken()

    def _create_requestor(self, requestor_class: Type[Requestor], verify: Union[bool, str]) -> Requestor:
        """Create and configure the HTTP requestor."""
        base_uri_v2 = f'https://{self.hostname}/api/v2'
        headers = {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/vnd.api+json'
        }
        
        return requestor_class(
            headers=headers,
            base_uri=base_uri_v2,
            verify=verify,
            log_level=self._log_level
        )

    def _resolve_organization(self, org: Optional[str]) -> Optional[str]:
        """Resolve organization from argument or environment."""
        if org is not None:
            self._logger.debug("Setting org from argument.")
            return org
        elif getenv('TFE_ORG'):
            self._logger.debug("Setting org from environment variable.")
            return getenv('TFE_ORG')
        else:
            self._logger.debug("No organization specified.")
            return None

    def _resolve_workspace(self, ws: Optional[str]) -> tuple[Optional[str], Optional[str]]:
        """Resolve workspace name and ID."""
        if ws is not None:
            self._logger.debug("Setting workspace from argument.")
            if self.org is not None:
                self._logger.debug("Fetching workspace ID.")
                ws_id = self._get_ws_id(ws)
                return ws, ws_id
            else:
                self._logger.debug("Cannot fetch workspace ID without organization.")
                return ws, None
        else:
            self._logger.debug("No workspace specified.")
            return None, None

    def _get_ws_id(self, ws_name: str) -> str:
        """
        Fetch workspace ID from workspace name.
        
        Args:
            ws_name: Name of the workspace
            
        Returns:
            Workspace ID string
            
        Raises:
            Various HTTP errors if workspace not found or inaccessible
        """
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        response = self._requestor.get(path=path)
        return response.data['data']['id']

    def _init_api_classes(self, classes_dict: Dict[str, Type[Any]]) -> None:
        """
        Initialize API endpoint classes and attach them to the client.
        
        Args:
            classes_dict: Dictionary mapping attribute names to API classes
        """
        for cls_name, cls in classes_dict.items():
            initialized_cls = cls(
                requestor=self._requestor,
                org=self.org,
                ws=self.ws,
                ws_id=self.ws_id,
                log_level=self._log_level
            )
            setattr(self, cls_name, initialized_cls)

    def _initialize_api_clients(self) -> None:
        """Initialize all API endpoint clients based on current configuration."""
        self._logger.debug("Initializing API classes that do not require an org...")
        self._init_api_classes(self._no_org_required_classes)

        if self.org is not None:
            self._logger.debug("Initializing API classes that require an org...")
            self._init_api_classes(self._org_required_classes)

    def set_org(self, name: str) -> None:
        """
        Set the organization for this client and reinitialize org-dependent APIs.
        
        This method updates the organization context and reinitializes all API
        endpoint clients that require an organization. Any existing workspace
        configuration will be cleared.
        
        Args:
            name: Organization name to set
            
        Note:
            This will clear any previously set workspace (ws/ws_id) since
            workspaces are scoped to organizations.
            
        Examples:
            >>> client.set_org('my-organization')
            >>> workspaces = client.workspaces.list()  # Now works
        """
        self._logger.debug(f"Setting organization to: {name}")
        self.org = name
        
        # Clear workspace when changing org
        self.ws = None
        self.ws_id = None
        
        # Reinitialize org-dependent API clients
        self._init_api_classes(self._org_required_classes)
    
    def set_ws(self, name: str) -> None:
        """
        Set the workspace for this client and reinitialize workspace-dependent APIs.
        
        This method sets the workspace context by fetching the workspace ID
        and reinitializing API endpoint clients. An organization must be set
        before calling this method.
        
        Args:
            name: Workspace name to set
            
        Raises:
            MissingOrganization: If no organization is currently set
            
        Examples:
            >>> client.set_org('my-org')
            >>> client.set_ws('my-workspace')
            >>> variables = client.workspace_variables.list()  # Now scoped to workspace
        """
        if not self.org:
            self._logger.error("Cannot set workspace without organization.")
            raise MissingOrganization()

        self._logger.debug(f"Setting workspace to: {name}")
        
        # Fetch workspace ID
        ws_id = self._get_ws_id(name)
        self._logger.debug(f"Resolved workspace ID: {ws_id}")
        
        self.ws = name
        self.ws_id = ws_id
        
        # Reinitialize org-dependent API clients with new workspace context
        self._init_api_classes(self._org_required_classes)