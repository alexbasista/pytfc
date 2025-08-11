"""
TFC/E Projects API endpoint module.

This module provides a modern, type-safe interface to Terraform Cloud/Enterprise
project management operations including CRUD operations, workspace organization,
and project-level settings.
"""
from typing import Any, Dict, List, Optional

from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import PyTFCError


class Projects(TfcApiBase):
    """
    TFC/E Projects API client.
    
    Provides methods for managing Terraform Cloud/Enterprise projects including
    CRUD operations, workspace organization, and project-level configuration.
    Projects help organize workspaces and provide a way to group related
    infrastructure resources.
    
    Examples:
        Create a new project:
        >>> project = client.projects.create(
        ...     name='web-infrastructure',
        ...     description='Frontend and backend services'
        ... )
        
        List all projects:
        >>> projects = client.projects.list()
        >>> for project in projects['data']:
        ...     print(f"{project['attributes']['name']}: {project['id']}")
        
        Update project settings:
        >>> client.projects.update(
        ...     project_id='prj-abc123',
        ...     description='Updated project description'
        ... )
    """

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Create a new project in the organization.
        
        Args:
            name: Project name (must be unique within organization)
            description: Optional project description
            **kwargs: Additional project attributes
            
        Returns:
            API response with created project data
            
        Examples:
            Basic project:
            >>> project = client.projects.create(name='my-project')
            
            Project with description:
            >>> project = client.projects.create(
            ...     name='web-infrastructure',
            ...     description='Frontend and backend services'
            ... )
            
            Project with additional settings:
            >>> project = client.projects.create(
            ...     name='secure-project',
            ...     description='High-security infrastructure',
            ...     auto_destroy_at='2024-12-31T23:59:59Z'
            ... )
        """
        payload = self._build_project_payload(
            name=name,
            description=description,
            **kwargs
        )
        
        path = f'/organizations/{self.org}/projects'
        return self._requestor.post(path=path, payload=payload)

    def update(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Update an existing project.
        
        Args:
            project_id: ID of the project to update
            name: New project name (optional)
            description: New project description (optional)
            **kwargs: Additional project attributes to update
            
        Returns:
            API response with updated project data
            
        Examples:
            Update project name:
            >>> client.projects.update(
            ...     project_id='prj-abc123',
            ...     name='renamed-project'
            ... )
            
            Update description:
            >>> client.projects.update(
            ...     project_id='prj-abc123',
            ...     description='Updated project description'
            ... )
            
            Update multiple attributes:
            >>> client.projects.update(
            ...     project_id='prj-abc123',
            ...     name='new-name',
            ...     description='New description',
            ...     auto_destroy_at='2025-01-01T00:00:00Z'
            ... )
        """
        payload = self._build_project_payload(
            name=name,
            description=description,
            **kwargs
        )
        
        path = f'/projects/{project_id}'
        return self._requestor.patch(path=path, payload=payload)

    def list(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        query: Optional[str] = None,
        filters: Optional[List[str]] = None,
        include: Optional[str] = None
    ) -> Any:
        """
        List projects in the organization.
        
        Args:
            page_number: Page number for pagination
            page_size: Number of items per page
            query: Search query to filter projects by name
            filters: List of filter strings in format ['[field]=value']
            include: Related resources to include
            
        Returns:
            API response with project list
            
        Examples:
            List all projects:
            >>> projects = client.projects.list()
            
            Search for projects:
            >>> projects = client.projects.list(query='web')
            
            Paginated listing:
            >>> projects = client.projects.list(
            ...     page_number=1,
            ...     page_size=25
            ... )
            
            With filters:
            >>> projects = client.projects.list(
            ...     filters=['[name]=production']
            ... )
        """
        path = f'/organizations/{self.org}/projects'
        return self._requestor.get(
            path=path,
            page_number=page_number,
            page_size=page_size,
            query=query,
            filters=filters,
            include=include
        )

    def list_all(
        self,
        query: Optional[str] = None,
        filters: Optional[List[str]] = None,
        include: Optional[str] = None
    ) -> Any:
        """
        List all projects across all pages.
        
        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 projects.
        
        Args:
            query: Search query to filter projects by name
            filters: List of filter strings in format ['[field]=value']
            include: Related resources to include
            
        Returns:
            TFCResponse with 'data' and 'included' arrays containing all results
            
        Examples:
            Get all projects:
            >>> all_projects = client.projects.list_all()
            >>> for project in all_projects.data['data']:
            ...     print(project['attributes']['name'])
            
            Search across all pages:
            >>> web_projects = client.projects.list_all(query='web')
        """
        path = f'/organizations/{self.org}/projects'
        return self._requestor.list_all(
            path=path,
            query=query,
            filters=filters,
            include=include
        )

    def show(self, project_id: str, include: Optional[str] = None) -> Any:
        """
        Get details for a specific project.
        
        Args:
            project_id: ID of the project to retrieve
            include: Related resources to include
            
        Returns:
            API response with project details
            
        Examples:
            Basic project details:
            >>> project = client.projects.show(project_id='prj-abc123')
            >>> print(project['data']['attributes']['name'])
            
            Include related resources:
            >>> project = client.projects.show(
            ...     project_id='prj-abc123',
            ...     include='workspaces'
            ... )
        """
        path = f'/projects/{project_id}'
        return self._requestor.get(path=path, include=include)

    def delete(self, project_id: str) -> Any:
        """
        Delete a project.
        
        Note: A project must be empty (no workspaces) before it can be deleted.
        
        Args:
            project_id: ID of the project to delete
            
        Returns:
            API response confirming deletion
            
        Examples:
            >>> client.projects.delete(project_id='prj-abc123')
        """
        path = f'/projects/{project_id}'
        return self._requestor.delete(path=path)

    # Utility Methods

    def get_project_id(self, name: str) -> Optional[str]:
        """
        Get project ID from project name.
        
        Helper method to find a project ID by searching for projects
        with the specified name.
        
        Args:
            name: Project name to search for
            
        Returns:
            Project ID if found, None if not found
            
        Raises:
            PyTFCError: If multiple projects match the name or API error occurs
            
        Examples:
            >>> project_id = client.projects.get_project_id('my-project')
            >>> if project_id:
            ...     print(f"Found project: {project_id}")
            ... else:
            ...     print("Project not found")
        """
        try:
            response = self.list(query=name)
            data = self._extract_response_data(response)
            
            if not data['data']:
                self._logger.debug(f"No project found with name '{name}'")
                return None
            
            # Filter results to find exact name match
            exact_matches = [
                project for project in data['data']
                if project['attributes']['name'] == name
            ]
            
            if len(exact_matches) == 0:
                self._logger.debug(f"No exact match found for project name '{name}'")
                return None
            elif len(exact_matches) == 1:
                project_id = exact_matches[0]['id']
                self._logger.debug(f"Found project '{name}' with ID: {project_id}")
                return project_id
            else:
                # Multiple exact matches - this shouldn't happen but handle gracefully
                raise PyTFCError(
                    f"Multiple projects found with name '{name}'. "
                    f"Project names should be unique within an organization."
                )
                
        except Exception as e:
            if isinstance(e, PyTFCError):
                raise
            raise PyTFCError(f"Failed to get project ID for '{name}': {e}")

    def get_project_name(self, project_id: str) -> str:
        """
        Get project name from project ID.
        
        Args:
            project_id: Project ID
            
        Returns:
            Project name string
            
        Raises:
            PyTFCError: If project not found or API error occurs
            
        Examples:
            >>> name = client.projects.get_project_name('prj-abc123')
            >>> print(f"Project name: {name}")
        """
        try:
            response = self.show(project_id=project_id)
            data = self._extract_response_data(response)
            return data['data']['attributes']['name']
        except Exception as e:
            raise PyTFCError(f"Failed to get project name for '{project_id}': {e}")

    # Private Helper Methods

    def _build_project_payload(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Build the JSON payload for project create/update operations.
        
        Args:
            name: Project name
            description: Project description
            **kwargs: Additional project attributes
            
        Returns:
            Complete JSON payload for API request
            
        Note:
            All kwargs are passed through to the API after converting
            underscores to hyphens. The API will validate parameters.
        """
        payload: Dict[str, Any] = {
            'data': {
                'type': 'projects',
                'attributes': {},
            }
        }
        
        # Add core fields if provided
        if name is not None:
            payload['data']['attributes']['name'] = name
        if description is not None:
            payload['data']['attributes']['description'] = description
        
        # Process all additional attributes - let the API validate them
        for key, value in kwargs.items():
            # Convert underscores to hyphens for API compatibility
            api_key = key.replace('_', '-')
            payload['data']['attributes'][api_key] = value
        
        return payload
