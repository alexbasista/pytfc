"""
TFC/E Workspaces API endpoint module.

This module provides a modern, type-safe interface to Terraform Cloud/Enterprise
workspace management operations including CRUD operations, VCS integration,
locking mechanisms, and remote state management.
"""
from typing import Any, Dict, List, Optional, Union

from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import PyTFCError


class Workspaces(TfcApiBase):
    """
    TFC/E Workspaces API client.
    
    Provides methods for managing Terraform Cloud/Enterprise workspaces including
    CRUD operations, VCS integration, locking mechanisms, and remote state management.
    
    Examples:
        Basic workspace creation:
        >>> client.workspaces.create(name='my-workspace')
        
        VCS-integrated workspace:
        >>> client.workspaces.create(
        ...     name='my-app-prod',
        ...     identifier='company/terraform-configs',
        ...     oauth_token_id='ot-123',
        ...     working_directory='/prod'
        ... )
        
        Update workspace settings:
        >>> client.workspaces.update(
        ...     name='my-workspace',
        ...     auto_apply=True,
        ...     terraform_version='1.6.0'
        ... )
    """

    # Valid workspace attributes for intelligent parameter routing
    _WORKSPACE_ATTRIBUTES = {
        'name',
        'agent_pool_id',
        'allow_destroy_plan',
        'auto_apply',
        'description',
        'execution_mode',
        'file_triggers_enabled',
        'global_remote_state',
        'queue_all_runs',
        'source_name',
        'source_url',
        'speculative_enabled',
        'terraform_version',
        'trigger_prefixes',
        'trigger_patterns',
        'working_directory',
        'assessments_enabled',
    }
    
    # Valid VCS repository attributes for intelligent parameter routing
    _VCS_ATTRIBUTES = {
        'oauth_token_id',
        'branch',
        'ingress_submodules',
        'identifier',
        'tags_regex',
        'github_app_installation_id',
        'vcs_repo',
    }

    def create(
        self,
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Create a new workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            project_id: Project ID to create workspace in
            **kwargs: Additional workspace and VCS attributes
            
        Returns:
            API response with created workspace data
            
        Raises:
            PyTFCError: If workspace name cannot be resolved
            
        Examples:
            Simple workspace:
            >>> response = client.workspaces.create(name='my-workspace')
            
            With VCS integration:
            >>> response = client.workspaces.create(
            ...     name='my-app',
            ...     identifier='org/repo',
            ...     oauth_token_id='ot-123',
            ...     working_directory='/terraform'
            ... )
        """
        
        ws_name = self._resolve_ws_name(name)
        
        payload = self._build_workspace_payload(
            name=ws_name,
            project_id=project_id,
            **kwargs
        )
        
        path = f'/organizations/{self.org}/workspaces'
        return self._requestor.post(path=path, payload=payload)

    def update(
        self,
        name: Optional[str] = None,
        new_name: Optional[str] = None,
        project_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Update an existing workspace.
        
        Args:
            name: Current workspace name (uses self.ws if not provided)
            new_name: New name for the workspace
            project_id: New project ID for the workspace
            **kwargs: Additional workspace and VCS attributes to update
            
        Returns:
            API response with updated workspace data
            
        Special handling:
            - Use vcs_repo='null' to remove VCS integration
            - new_name will rename the workspace
            
        Examples:
            Update settings:
            >>> response = client.workspaces.update(
            ...     name='my-workspace',
            ...     auto_apply=True,
            ...     terraform_version='1.6.0'
            ... )
            
            Remove VCS integration:
            >>> response = client.workspaces.update(
            ...     name='my-workspace',
            ...     vcs_repo='null'
            ... )
        """
        
        ws_name = self._resolve_ws_name(name)
        
        # Handle renaming
        if new_name:
            kwargs['name'] = new_name
        
        payload = self._build_workspace_payload(
            project_id=project_id,
            **kwargs
        )
        
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.patch(path=path, payload=payload)

    def list(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        search: Optional[Dict[str, str]] = None,
        include: Optional[str] = None
    ) -> Any:
        """
        List workspaces in the organization.
        
        Args:
            page_number: Page number for pagination
            page_size: Number of items per page
            search: Search parameters
            include: Related resources to include
            
        Returns:
            API response with workspace list
            
        Examples:
            List all workspaces:
            >>> workspaces = client.workspaces.list()
            
            Search for workspaces:
            >>> workspaces = client.workspaces.list(
            ...     search={'name': 'prod'}
            ... )
        """
        
        path = f'/organizations/{self.org}/workspaces'
        return self._requestor.get(
            path=path,
            page_number=page_number,
            page_size=page_size,
            search=search,
            include=include
        )

    def list_all(
        self,
        search: Optional[Dict[str, str]] = None,
        include: Optional[str] = None
    ) -> Dict[str, List[Any]]:
        """
        List all workspaces across all pages.
        
        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 workspaces.
        
        Args:
            search: Search parameters
            include: Related resources to include
            
        Returns:
            Dictionary with 'data' and 'included' arrays containing all results
            
        Examples:
            Get all workspaces:
            >>> all_workspaces = client.workspaces.list_all()
            >>> for workspace in all_workspaces['data']:
            ...     print(workspace['attributes']['name'])
        """
        
        path = f'/organizations/{self.org}/workspaces'
        return self._requestor.list_all(
            path=path,
            search=search,
            include=include
        )

    def show(self, name: Optional[str] = None) -> Any:
        """
        Get details for a specific workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response with workspace details
            
        Examples:
            >>> workspace = client.workspaces.show(name='my-workspace')
            >>> print(workspace['data']['attributes']['terraform-version'])
        """
        
        ws_name = self._resolve_ws_name(name)
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.get(path=path)

    def delete(self, name: str) -> Any:
        """
        Delete a workspace.
        
        Args:
            name: Name of workspace to delete
            
        Returns:
            API response confirming deletion
            
        Examples:
            >>> client.workspaces.delete(name='old-workspace')
        """
        
        path = f'/organizations/{self.org}/workspaces/{name}'
        return self._requestor.delete(path=path)

    # Workspace Actions
    
    def lock(
        self,
        name: Optional[str] = None,
        reason: str = 'Locked by pytfc'
    ) -> Any:
        """
        Lock a workspace to prevent runs.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            reason: Reason for locking
            
        Returns:
            API response confirming lock
            
        Examples:
            >>> client.workspaces.lock(
            ...     name='prod-workspace',
            ...     reason='Maintenance window'
            ... )
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        payload = {'reason': reason}
        path = f'/workspaces/{ws_id}/actions/lock'
        return self._requestor.post(path=path, payload=payload)

    def unlock(self, name: Optional[str] = None) -> Any:
        """
        Unlock a workspace to allow runs.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response confirming unlock
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        path = f'/workspaces/{ws_id}/actions/unlock'
        return self._requestor.post(path=path, payload=None)

    def force_unlock(self, name: Optional[str] = None) -> Any:
        """
        Force unlock a workspace (bypasses normal unlock restrictions).
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response confirming force unlock
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        path = f'/workspaces/{ws_id}/actions/force-unlock'
        return self._requestor.post(path=path, payload=None)

    # SSH Key Management
    
    def assign_ssh_key(
        self,
        ssh_key_id: str,
        name: Optional[str] = None
    ) -> Any:
        """
        Assign an SSH key to a workspace.
        
        Args:
            ssh_key_id: ID of the SSH key to assign
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response confirming assignment
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        payload = {
            'data': {
                'type': 'workspaces',
                'attributes': {'id': ssh_key_id}
            }
        }
        
        path = f'/workspaces/{ws_id}/relationships/ssh-key'
        return self._requestor.patch(path=path, payload=payload)

    def unassign_ssh_key(self, name: Optional[str] = None) -> Any:
        """
        Remove SSH key assignment from a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response confirming removal
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        payload = {
            'data': {
                'type': 'workspaces',
                'attributes': {'id': 'null'}
            }
        }
        
        path = f'/workspaces/{ws_id}/relationships/ssh-key'
        return self._requestor.patch(path=path, payload=payload)

    # Remote State Management
    
    def get_remote_state_consumers(
        self,
        name: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Any:
        """
        Get workspaces that consume this workspace's remote state.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            page_number: Page number for pagination
            page_size: Items per page
            
        Returns:
            API response with consumer workspace list
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        path = f'/workspaces/{ws_id}/relationships/remote-state-consumers'
        return self._requestor.get(
            path=path,
            page_number=page_number,
            page_size=page_size
        )

    def replace_remote_state_consumers(self, name: Optional[str] = None) -> Any:
        """
        Replace remote state consumers for a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response
            
        Note:
            Implementation coming soon. First checks if global-remote-state is false.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        # First check if global-remote-state is false
        raise NotImplementedError("Method implementation coming soon")

    def add_remote_state_consumers(self, name: Optional[str] = None) -> Any:
        """
        Add remote state consumers to a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response
            
        Note:
            Implementation coming soon. First checks if global-remote-state is false.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        # First check if global-remote-state is false
        raise NotImplementedError("Method implementation coming soon")

    def delete_remote_state_consumers(self, name: Optional[str] = None) -> Any:
        """
        Remove remote state consumers from a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response
            
        Note:
            Implementation coming soon. First checks if global-remote-state is false.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        # First check if global-remote-state is false
        raise NotImplementedError("Method implementation coming soon")

    # Tag Management
    
    def get_tags(self, name: Optional[str] = None) -> Any:
        """
        Get tags for a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response with workspace tags
            
        Note:
            Implementation coming soon.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        # Add query parameters support
        raise NotImplementedError("Method implementation coming soon")

    def add_tags(self, name: Optional[str] = None) -> Any:
        """
        Add tags to a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response
            
        Note:
            Implementation coming soon.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        raise NotImplementedError("Method implementation coming soon")

    def remove_tags(self, name: Optional[str] = None) -> Any:
        """
        Remove tags from a workspace.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            API response
            
        Note:
            Implementation coming soon.
        """
        
        ws_name = self._resolve_ws_name(name)
        ws_id = self.get_workspace_id(name=ws_name)
        
        # TODO: Implement this method
        raise NotImplementedError("Method implementation coming soon")

    # Utility Methods
    
    def get_workspace_id(self, name: Optional[str] = None) -> str:
        """
        Get workspace ID from workspace name.
        
        Args:
            name: Workspace name (uses self.ws if not provided)
            
        Returns:
            Workspace ID string
            
        Raises:
            PyTFCError: If workspace cannot be found
            
        Examples:
            >>> ws_id = client.workspaces.get_workspace_id('my-workspace')
            'ws-abc123def456'
        """
        
        ws_name = self._resolve_ws_name(name)
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        
        try:
            response = self._requestor.get(path=path)
            data = self._extract_response_data(response)
            return data['data']['id']
        except Exception as e:
            raise PyTFCError(f"Failed to get workspace ID for '{ws_name}': {e}")

    def get_workspace_name(self, ws_id: Optional[str] = None) -> str:
        """
        Get workspace name from workspace ID.
        
        Args:
            ws_id: Workspace ID (uses self.ws_id if not provided)
            
        Returns:
            Workspace name string
            
        Examples:
            >>> name = client.workspaces.get_workspace_name('ws-abc123')
            'my-workspace'
        """
        
        workspace_id = self._resolve_ws_id(ws_id)
        path = f'/workspaces/{workspace_id}'
        
        try:
            response = self._requestor.get(path=path)
            data = self._extract_response_data(response)
            return data['data']['attributes']['name']
        except Exception as e:
            raise PyTFCError(f"Failed to get workspace name for '{workspace_id}': {e}")

    # Private helper methods
    
    def _build_workspace_payload(
        self,
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Build the JSON payload for workspace create/update operations.
        
        Uses intelligent parameter routing to place attributes in the correct
        location within the JSON structure:
        - Workspace attributes → data.attributes.*
        - VCS attributes → data.attributes.vcs-repo.*
        - Project ID → data.relationships.project
        
        Args:
            name: Workspace name
            project_id: Project ID
            **kwargs: Additional workspace and VCS attributes
            
        Returns:
            Complete JSON payload for API request
        """
        
        payload: Dict[str, Any] = {
            'data': {
                'type': 'workspaces',
                'attributes': {},
            }
        }
        
        # Add workspace name if provided
        if name:
            payload['data']['attributes']['name'] = name
        
        attributes = payload['data']['attributes']
        vcs_repo = {}
        
        # Handle special case for removing VCS repo
        if kwargs.get('vcs_repo') == 'null':
            attributes['vcs-repo'] = None
            return payload  # Early return to avoid processing other VCS attrs
        
        # Remove new_name if present (handled by caller)
        kwargs.pop('new_name', None)
        
        # Intelligent parameter routing
        for key, value in kwargs.items():
            if key in self._WORKSPACE_ATTRIBUTES:
                # Workspace attribute → data.attributes.*
                api_key = key.replace('_', '-')
                attributes[api_key] = value
                
            elif key in self._VCS_ATTRIBUTES:
                # VCS attribute → data.attributes.vcs-repo.*
                if key == 'vcs_repo':
                    # Skip the special vcs_repo flag
                    pass
                else:
                    api_key = key.replace('_', '-')
                    vcs_repo[api_key] = value
                
            else:
                # Unknown attribute - log warning but still pass through
                self._logger.warning(
                    f"Unknown workspace attribute '{key}'. "
                    f"This will be passed to the API for validation."
                )
                # Pass unknown attributes as regular workspace attributes
                api_key = key.replace('_', '-')
                attributes[api_key] = value
        
        # Add VCS repo configuration if any VCS attributes were provided
        # and not all values are None
        if vcs_repo and any(v is not None for v in vcs_repo.values()):
            attributes['vcs-repo'] = vcs_repo
        
        # Add project relationship if provided
        if project_id:
            payload['data']['relationships'] = {
                'project': {
                    'data': {'id': project_id, 'type': 'projects'}
                }
            }
        
        return payload