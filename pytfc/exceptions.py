"""
Enhanced exception hierarchy for pytfc with better error handling and context.
"""
from typing import Any, Dict, Optional
import requests


class PyTFCError(Exception):
    """
    Base exception class for all pytfc errors.
    
    This is the base class that all other pytfc exceptions inherit from.
    Users can catch this to handle any pytfc-related error.
    
    Args:
        message: Human-readable error message
        details: Optional dictionary with additional error context
        
    Attributes:
        message: The error message
        details: Dictionary containing additional error information
    """
    
    def __init__(
        self, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        return self.message


class PyTFCConfigurationError(PyTFCError):
    """Raised when there's an issue with client configuration."""
    pass


class PyTFCHTTPError(PyTFCError):
    """
    Raised when an HTTP request fails.
    
    This exception preserves the original HTTP response for detailed debugging.
    
    Attributes:
        response: The original requests.Response object
        status_code: HTTP status code
        url: The URL that was requested
    """
    
    def __init__(
        self, 
        message: str, 
        response: Optional[requests.Response] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message, details)
        self.response = response
        
        if response is not None:
            self.status_code = response.status_code
            self.url = response.url
        else:
            self.status_code = None
            self.url = None
    
    def __str__(self) -> str:
        if self.status_code:
            return f"{self.message} (HTTP {self.status_code})"
        return self.message


# Configuration-related exceptions
class MissingToken(PyTFCConfigurationError):
    """TFC/E Token not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E API token is required. Set TFE_TOKEN environment variable or pass token parameter."
        )


class MissingOrganization(PyTFCConfigurationError):
    """TFC/E Organization not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E Organization is required. Set TFE_ORG environment variable or pass org parameter."
        )


class MissingWorkspace(PyTFCConfigurationError):
    """TFC/E Workspace name or ID not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E Workspace name or ID is required for this operation."
        )


class MissingOauthClient(PyTFCConfigurationError):
    """TFC/E OAuth Client ID or name not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E OAuth Client ID or name is required for this operation."
        )


class MissingVcsProvider(PyTFCConfigurationError):
    """TFC/E OAuth Client not found."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E VCS Provider (OAuth Client) not found."
        )


class MissingRun(PyTFCConfigurationError):
    """TFC/E Run ID or commit message not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E Run ID or commit message is required for this operation."
        )


class MissingPlan(PyTFCConfigurationError):
    """TFC/E Plan not specified."""
    
    def __init__(self) -> None:
        super().__init__(
            "TFC/E Plan ID is required for this operation."
        )


# Validation-related exceptions
class InvalidQueryParam(PyTFCError):
    """Unsupported value for query parameter."""
    
    def __init__(self, param_name: str, param_value: Any, valid_values: Optional[list] = None) -> None:
        if valid_values:
            message = f"Invalid value '{param_value}' for parameter '{param_name}'. Valid values: {valid_values}"
        else:
            message = f"Invalid value '{param_value}' for parameter '{param_name}'"
            
        super().__init__(
            message,
            details={
                'param_name': param_name,
                'param_value': param_value,
                'valid_values': valid_values
            }
        )


# Operation-related exceptions
class ConfigurationVersionUploadError(PyTFCError):
    """Error uploading Terraform tar.gz to Configuration Version."""
    
    def __init__(self, message: str = "Failed to upload configuration version") -> None:
        super().__init__(message)


class PlanExportDownloadError(PyTFCError):
    """Error downloading Plan Export."""
    
    def __init__(self, message: str = "Failed to download plan export") -> None:
        super().__init__(message)


# Legacy base class for backward compatibility (if needed)
class Error(PyTFCError):
    """
    Legacy base class for general exceptions.
    
    Deprecated: Use PyTFCError instead.
    """
    pass


def create_http_error(response: requests.Response) -> PyTFCHTTPError:
    """
    Create an appropriate HTTP error from a requests.Response.
    
    Args:
        response: The HTTP response object
        
    Returns:
        PyTFCHTTPError with appropriate message and context
    """
    try:
        error_data = response.json()
        # Try to extract TFC/E API error message
        if 'errors' in error_data and error_data['errors']:
            message = error_data['errors'][0].get('detail', f"HTTP {response.status_code} error")
        else:
            message = f"HTTP {response.status_code} error"
    except (ValueError, requests.exceptions.JSONDecodeError, IndexError, KeyError):
        message = f"HTTP {response.status_code} error"
    
    return PyTFCHTTPError(message, response)