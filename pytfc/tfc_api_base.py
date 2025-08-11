"""
Enhanced base module for all pytfc API endpoint classes.

This module provides the foundation class that all API endpoint classes inherit from,
with common utilities and modern Python practices.
"""
import logging
import sys
from abc import ABC
from typing import Any, Optional, Union

from pytfc.exceptions import PyTFCError


class TfcApiBase(ABC):
    """
    Modern base class for TFC/E API endpoints.
    
    This class provides common functionality that all API endpoint classes need,
    including proper logging setup, path helpers, and validation utilities.
    
    Args:
        requestor: HTTP requestor instance for making API calls
        org: Organization name (if applicable)
        ws: Workspace name (if applicable) 
        ws_id: Workspace ID (if applicable)
        log_level: Logging level for this endpoint
        
    Attributes:
        _requestor: HTTP requestor for API calls
        org: Organization name
        ws: Workspace name
        ws_id: Workspace ID
        log_level: Current logging level
        _logger: Logger instance for this endpoint
    """

    def __init__(
        self, 
        requestor: Any, 
        org: Optional[str], 
        ws: Optional[str], 
        ws_id: Optional[str], 
        log_level: Union[str, int]
    ) -> None:
        """Initialize the API endpoint base class."""
        
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(log_level)
        
        # Only add handler if none exists to avoid duplicates
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        self._requestor = requestor
        self.org = org
        self.ws = ws
        self.ws_id = ws_id
        self.log_level = log_level

    # def _get_org_path(self) -> str:
    #     """
    #     Get the organization path component for API endpoints.
        
    #     Returns:
    #         Organization path string (e.g., '/organizations/my-org')
            
    #     Raises:
    #         PyTFCError: If no organization is set
            
    #     Examples:
    #         >>> path = f'{self._get_org_path()}/workspaces'
    #         '/organizations/my-org/workspaces'
    #     """
        
    #     if not self.org:
    #         raise PyTFCError("Organization must be set to use this endpoint")
    #     return f'/organizations/{self.org}'

    # def _get_workspace_path(self, ws_id: Optional[str] = None) -> str:
    #     """
    #     Get the workspace path component for API endpoints.
        
    #     Args:
    #         ws_id: Optional workspace ID override
            
    #     Returns:
    #         Workspace path string (e.g., '/workspaces/ws-123')
            
    #     Raises:
    #         PyTFCError: If no workspace ID is available
            
    #     Examples:
    #         >>> path = f'{self._get_workspace_path()}/runs'
    #         '/workspaces/ws-abc123/runs'
    #     """
        
    #     workspace_id = ws_id or self.ws_id
    #     if not workspace_id:
    #         raise PyTFCError("Workspace ID must be set to use this endpoint")
    #     return f'/workspaces/{workspace_id}'

    def _resolve_ws_name(self, name: Optional[str]) -> str:
        """
        Resolve workspace name from parameter or instance attribute.
        
        Args:
            name: Provided workspace name (takes precedence)
            
        Returns:
            The workspace name to use
            
        Raises:
            PyTFCError: If no workspace name is available
            
        Examples:
            >>> ws_name = self._resolve_ws_name(name)  # Uses 'name' if provided
            >>> ws_name = self._resolve_ws_name(None)  # Uses self.ws
        """
        
        result = name or self.ws
        if not result:
            raise PyTFCError("Workspace name must be provided or set on the instance")
        return result

    def _resolve_ws_id(self, ws_id: Optional[str]) -> str:
        """
        Resolve workspace ID from parameter or instance attribute.
        
        Args:
            ws_id: Provided workspace ID (takes precedence)
            
        Returns:
            The workspace ID to use
            
        Raises:
            PyTFCError: If no workspace ID is available
            
        Examples:
            >>> workspace_id = self._resolve_ws_id(ws_id)  # Uses 'ws_id' if provided
            >>> workspace_id = self._resolve_ws_id(None)  # Uses self.ws_id
        """
        
        result = ws_id or self.ws_id
        if not result:
            raise PyTFCError("Workspace ID must be provided or set on the instance")
        return result

    def _validate_choice(
        self, 
        value: Any, 
        valid_choices: list, 
        param_name: str
    ) -> None:
        """
        Validate that a parameter value is in a list of valid choices.
        
        Args:
            value: The value to validate
            valid_choices: List of valid choices
            param_name: Name of the parameter (for error messages)
            
        Raises:
            PyTFCError: If value is not in valid choices
            
        Examples:
            >>> self._validate_choice('terraform', ['terraform', 'env'], 'category')
            >>> self._validate_choice('invalid', ['terraform', 'env'], 'category')
            PyTFCError: Invalid value 'invalid' for parameter 'category'...
        """
        
        if value not in valid_choices:
            raise PyTFCError(
                f"Invalid value '{value}' for parameter '{param_name}'. "
                f"Valid choices: {valid_choices}"
            )

    def _extract_response_data(self, response: Any) -> Any:
        """
        Extract data from a TFC/E API response.
        
        Handles both old response format (dict) and new TFCResponse format.
        
        Args:
            response: API response object
            
        Returns:
            The response data
            
        Examples:
            >>> data = self._extract_response_data(response)
            >>> project_id = data['data'][0]['id']
        """
        
        if hasattr(response, 'data'):
            # New TFCResponse format
            return response.data
        elif hasattr(response, 'json'):
            # Old response format or requests.Response
            return response.json()
        else:
            # Already a dict
            return response