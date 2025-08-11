"""
Utility functions and decorators for pytfc library.

This module contains helper functions and decorators used throughout
the pytfc library for validation and common operations.
"""
import functools
from typing import Any, Callable, TypeVar

from pytfc.exceptions import MissingWorkspace
from pytfc import exceptions

# Type variable for decorator typing
F = TypeVar('F', bound=Callable[..., Any])

# Constants
DEFAULT_LOG_LEVEL = 'WARNING'


def validate_ws_is_set(func: F) -> F:
    """
    Decorator to ensure workspace name is available before calling the function.
    
    This decorator checks that either a workspace name is provided as a keyword
    argument or the instance has a workspace name set. Raises MissingWorkspace
    if neither condition is met.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function that validates workspace availability
        
    Raises:
        MissingWorkspace: If no workspace name is available
        
    Examples:
        >>> @validate_ws_is_set
        ... def show_workspace(self, name=None):
        ...     ws_name = name if name else self.ws
        ...     return self._requestor.get(f'/workspaces/{ws_name}')
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Check if workspace name is provided via kwargs or instance attribute
        if not kwargs.get('name') and not args[0].ws:
            raise MissingWorkspace()
        return func(*args, **kwargs)
    return wrapper


def validate_ws_id_is_set(func: F) -> F:
    """
    Decorator to ensure workspace ID is available before calling the function.
    
    This decorator checks that either a workspace ID is provided as a keyword
    argument or the instance has a workspace ID set. Raises MissingWorkspace
    if neither condition is met.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function that validates workspace ID availability
        
    Raises:
        MissingWorkspace: If no workspace ID is available
        
    Examples:
        >>> @validate_ws_id_is_set
        ... def list_variables(self, ws_id=None):
        ...     workspace_id = ws_id if ws_id else self.ws_id
        ...     return self._requestor.get(f'/workspaces/{workspace_id}/vars')
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Check if workspace ID is provided via kwargs or instance attribute
        if not kwargs.get('ws_id') and not args[0].ws_id:
            raise MissingWorkspace()
        return func(*args, **kwargs)
    return wrapper


def validate_org_is_set(func: F) -> F:
    """
    Decorator to ensure organization is available before calling the function.
    
    This decorator checks that the instance has an organization set.
    Raises MissingOrganization if not available.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function that validates organization availability
        
    Raises:
        MissingOrganization: If no organization is available
        
    Examples:
        >>> @validate_org_is_set
        ... def list_workspaces(self):
        ...     return self._requestor.get(f'/organizations/{self.org}/workspaces')
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        from pytfc.exceptions import MissingOrganization
        
        # Check if organization is set on the instance
        if not args[0].org:
            raise MissingOrganization()
        return func(*args, **kwargs)
    return wrapper

def tfe_only(func):
    """
    Decorator to restrict methods to Terraform Enterprise only.
    
    Raises PyTFCError if the client is connected to Terraform Cloud
    (app.terraform.io) instead of a TFE instance.
    
    Args:
        func: The method to decorate
        
    Returns:
        Decorated function that checks TFE vs TFC
        
    Raises:
        PyTFCError: If method is called against Terraform Cloud
        
    Examples:
        @tfe_only
        def some_tfe_method(self):
            # This will only work on TFE instances
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]  # Get the API client instance
        
        # Check if we can access the hostname through the requestor
        if hasattr(self, '_requestor') and hasattr(self._requestor, '_base_uri'):
            base_uri = self._requestor._base_uri
            if 'app.terraform.io' in base_uri:
                method_name = func.__name__
                raise exceptions.PyTFCError(
                    f"Method '{method_name}' is only available in Terraform Enterprise, "
                    f"not Terraform Cloud. Current endpoint: {base_uri}"
                )
        
        # If we can't determine the hostname, proceed (fail gracefully)
        return func(*args, **kwargs)
    
    return wrapper