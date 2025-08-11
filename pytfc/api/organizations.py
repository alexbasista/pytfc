"""
TFC/E Organizations API endpoint module.
"""
from typing import Any, Dict, Optional

from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import tfe_only


class Organizations(TfcApiBase):
    """
    TFC/E Organizations API client.
    
    Provides methods for managing Terraform Cloud/Enterprise organizations including
    CRUD operations, settings management, and entitlement viewing.
    
    Examples:
        List all organizations:
        >>> orgs = client.organizations.list()
        
        Create a new organization:
        >>> client.organizations.create(
        ...     name='my-company',
        ...     email='admin@mycompany.com'
        ... )
        
        Update organization settings:
        >>> client.organizations.update(
        ...     name='my-company',
        ...     cost_estimation_enabled=True,
        ...     session_timeout=20160
        ... )
    """

    def list(self, include: Optional[str] = None) -> Any:
        """
        List all organizations.
        
        Args:
            include: Related resources to include (e.g., 'entitlement_set')
        
        Returns:
            API response with organization list
            
        Examples:
            Basic organization list:
            >>> orgs = client.organizations.list()
            >>> for org in orgs['data']:
            ...     print(org['attributes']['name'])
            
            Include entitlement sets:
            >>> orgs = client.organizations.list(include='entitlement_set')
        """
        
        return self._requestor.get(path='/organizations', include=include)

    def show(self, name: str, include: Optional[str] = None) -> Any:
        """
        Get details for a specific organization.
        
        Args:
            name: Organization name
            include: Related resources to include (e.g., 'entitlement_set')
            
        Returns:
            API response with organization details
            
        Examples:
            Basic organization details:
            >>> org = client.organizations.show(name='my-company')
            
            Include entitlement set:
            >>> org = client.organizations.show(
            ...     name='my-company', 
            ...     include='entitlement_set'
            ... )
        """
        
        path = f'/organizations/{name}'
        return self._requestor.get(path=path, include=include)

    def create(self, name: str, email: str, **kwargs: Any) -> Any:
        """
        Create a new organization.
        
        Args:
            name: Organization name
            email: Organization email address
            **kwargs: Additional organization attributes
            
        Returns:
            API response with created organization data
            
        Examples:
            Basic organization:
            >>> response = client.organizations.create(
            ...     name='my-company',
            ...     email='admin@mycompany.com'
            ... )
            
            With additional settings:
            >>> response = client.organizations.create(
            ...     name='my-company',
            ...     email='admin@mycompany.com',
            ...     cost_estimation_enabled=True,
            ...     session_timeout=20160,
            ...     collaborator_auth_policy='password'
            ... )
        """
        
        payload = self._build_organization_payload(
            name=name,
            email=email,
            **kwargs
        )
        
        return self._requestor.post(path='/organizations', payload=payload)

    def update(self, name: str, new_name: Optional[str] = None, **kwargs: Any) -> Any:
        """
        Update an existing organization.
        
        Args:
            name: Current organization name
            new_name: New name for the organization (optional)
            **kwargs: Additional organization attributes to update
            
        Returns:
            API response with updated organization data
            
        Examples:
            Update settings:
            >>> response = client.organizations.update(
            ...     name='my-company',
            ...     cost_estimation_enabled=True,
            ...     session_timeout=30240
            ... )
            
            Rename organization:
            >>> response = client.organizations.update(
            ...     name='old-name',
            ...     new_name='new-company-name'
            ... )
        """
        
        # Handle renaming
        if new_name:
            kwargs['name'] = new_name
        
        payload = self._build_organization_payload(**kwargs)
        
        path = f'/organizations/{name}'
        return self._requestor.patch(path=path, payload=payload)

    def delete(self, name: str) -> Any:
        """
        Delete an organization.
        
        Args:
            name: Name of organization to delete
            
        Returns:
            API response confirming deletion
            
        Examples:
            >>> client.organizations.delete(name='old-organization')
        """
        
        path = f'/organizations/{name}'
        return self._requestor.delete(path=path)

    def show_entitlement_set(self, name: str) -> Any:
        """
        Get the entitlement set for an organization.
        
        Shows what features and limits are available for the organization
        based on their Terraform Cloud/Enterprise plan.
        
        Args:
            name: Organization name
            
        Returns:
            API response with entitlement details
            
        Examples:
            >>> entitlements = client.organizations.show_entitlement_set('my-company')
            >>> print(entitlements['data']['attributes']['cost-estimation'])
        """
        
        path = f'/organizations/{name}/entitlement-set'
        return self._requestor.get(path=path)

    @tfe_only
    def create_data_retention_policy(
        self, 
        name: str, 
        policy_type: str,
        delete_older_than_n_days: Optional[int] = None,
        **kwargs: Any
    ) -> Any:
        """
        Create a data retention policy for an organization.
        
        This endpoint is only available in Terraform Enterprise.
        
        Args:
            name: Organization name
            policy_type: Data retention policy type (e.g., 'data-retention-policy-delete-olders')
            delete_older_than_n_days: Number of days after which to delete data (optional)
            **kwargs: Additional policy attributes
            
        Returns:
            API response with policy creation result
            
        Examples:
            Create a deletion policy:
            >>> response = client.organizations.create_data_retention_policy(
            ...     name='my-company',
            ...     policy_type='data-retention-policy-delete-olders',
            ...     delete_older_than_n_days=33
            ... )
        """
        
        payload = self._build_data_retention_policy_payload(
            policy_type, delete_older_than_n_days, **kwargs
        )
        
        path = f'/organizations/{name}/relationships/data-retention-policy'
        return self._requestor.post(path=path, payload=payload)

    @tfe_only
    def update_data_retention_policy(
        self, 
        name: str, 
        policy_type: str,
        delete_older_than_n_days: Optional[int] = None,
        **kwargs: Any
    ) -> Any:
        """
        Update the data retention policy for an organization.
        
        This endpoint is only available in Terraform Enterprise.
        
        Args:
            name: Organization name
            policy_type: Data retention policy type (e.g., 'data-retention-policy-delete-olders')
            delete_older_than_n_days: Number of days after which to delete data (optional)
            **kwargs: Additional policy attributes
            
        Returns:
            API response with policy update result
            
        Examples:
            Update a deletion policy:
            >>> response = client.organizations.update_data_retention_policy(
            ...     name='my-company',
            ...     policy_type='data-retention-policy-delete-olders',
            ...     delete_older_than_n_days=45
            ... )
        """
        
        payload = self._build_data_retention_policy_payload(
            policy_type, delete_older_than_n_days, **kwargs
        )
        
        path = f'/organizations/{name}/relationships/data-retention-policy'
        return self._requestor.post(path=path, payload=payload)

    @tfe_only
    def show_data_retention_policy(self, name: str) -> Any:
        """
        Get the data retention policy for an organization.
        
        Shows the data retention policy set explicitly on the organization.
        When no data retention policy is set for the organization, returns
        the default policy configured for the Terraform Enterprise installation.
        
        This endpoint is only available in Terraform Enterprise.
        
        Args:
            name: Organization name
            
        Returns:
            API response with data retention policy details
            
        Examples:
            >>> policy = client.organizations.show_data_retention_policy('my-company')
            >>> print(policy['data']['attributes']['delete-older-than'])
        """
        
        path = f'/organizations/{name}/relationships/data-retention-policy'
        return self._requestor.get(path=path)

    @tfe_only
    def delete_data_retention_policy(self, name: str) -> Any:
        """
        Remove the data retention policy for an organization.
        
        This endpoint removes the data retention policy explicitly set on an organization.
        When the data retention policy is deleted, the organization inherits the default 
        policy configured for the Terraform Enterprise installation.
        
        This endpoint is only available in Terraform Enterprise.
        
        Args:
            name: Organization name
            
        Returns:
            API response confirming policy deletion
            
        Examples:
            Remove organization's data retention policy:
            >>> response = client.organizations.delete_data_retention_policy('my-company')
            
            # Organization will now inherit the TFE installation default policy
        """
        
        path = f'/organizations/{name}/relationships/data-retention-policy'
        return self._requestor.delete(path=path)

    @tfe_only
    def show_module_producers(
        self, 
        name: str, 
        page_number: Optional[int] = None, 
        page_size: Optional[int] = None
    ) -> Any:
        """
        Get module producers for an organization.
        
        Returns organizations that can produce modules for consumption
        by the specified organization.
        
        Args:
            name: Organization name
            page_number: Page number for pagination (optional)
            page_size: Number of items per page (optional, max 100)
            
        Returns:
            API response with module producer organizations list
            
        Examples:
            Get module producers:
            >>> producers = client.organizations.show_module_producers('my-company')
            
            With pagination:
            >>> producers = client.organizations.show_module_producers(
            ...     name='my-company',
            ...     page_number=1,
            ...     page_size=50
            ... )
        """
        
        path = f'/organizations/{name}/relationships/module-producers'
        return self._requestor.get(
            path=path,
            page_number=page_number,
            page_size=page_size
        )

    # Private helper methods
    
    def _build_organization_payload(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Build the JSON payload for organization create/update operations.
        
        Args:
            name: Organization name
            email: Organization email
            **kwargs: Additional organization attributes
            
        Returns:
            Complete JSON payload for API request
            
        Note:
            All kwargs are passed through to the API after converting
            underscores to hyphens. The API will validate parameters.
        """
        
        payload: Dict[str, Any] = {
            'data': {
                'type': 'organizations',
                'attributes': {},
            }
        }
        
        # Add required fields if provided
        if name:
            payload['data']['attributes']['name'] = name
        if email:
            payload['data']['attributes']['email'] = email
        
        # Process all additional attributes - let the API validate them
        for key, value in kwargs.items():
            # Convert underscores to hyphens for API compatibility
            api_key = key.replace('_', '-')
            payload['data']['attributes'][api_key] = value
        
        return payload

    def _build_data_retention_policy_payload(
        self,
        policy_type: str,
        delete_older_than_n_days: Optional[int] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Build the JSON payload for data retention policy operations.
        
        Args:
            policy_type: Must be 'data_retention_policy_delete_olders' or 
                        'data_retention_policy_dont_deletes'
            delete_older_than_n_days: Number of days for deletion policies
            **kwargs: Additional policy attributes
            
        Returns:
            Complete JSON payload for API request
            
        Raises:
            ValueError: If policy_type is invalid or required parameters are missing
        """
        
        # Valid policy types (Python format)
        valid_types = {
            'data_retention_policy_delete_olders',
            'data_retention_policy_dont_deletes'
        }
        
        if policy_type not in valid_types:
            raise ValueError(
                f"Invalid policy_type '{policy_type}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )
        
        # Convert to API format
        api_policy_type = policy_type.replace('_', '-')
        
        payload = {
            'data': {
                'type': api_policy_type,
                'attributes': {}
            }
        }
        
        if policy_type == 'data_retention_policy_delete_olders':
            # Validate required parameter for delete-olders policy
            if delete_older_than_n_days is None:
                raise ValueError(
                    "delete_older_than_n_days is required for "
                    "'data_retention_policy_delete_olders' policy type"
                )
            payload['data']['attributes']['deleteOlderThanNDays'] = delete_older_than_n_days
            
        elif policy_type == 'data_retention_policy_dont_deletes':
            # Warn if delete_older_than_n_days was provided but will be ignored
            if delete_older_than_n_days is not None:
                self._logger.warning(
                    f"delete_older_than_n_days={delete_older_than_n_days} provided for "
                    f"policy_type '{policy_type}' but will be ignored. "
                    f"This policy type does not support deletion parameters."
                )
        
        # Add any additional attributes from kwargs
        for key, value in kwargs.items():
            payload['data']['attributes'][key] = value
        
        return payload