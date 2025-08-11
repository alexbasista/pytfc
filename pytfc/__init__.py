"""
Python HTTP client library for Terraform Cloud/Enterprise API.

This module provides the main entry point for interacting with TFC/E APIs.
Import the Client class to get started, and access specific exceptions
for error handling.

Basic Usage:
    >>> import pytfc
    >>> client = pytfc.Client(
    ...     hostname='app.terraform.io',  # or your TFE hostname
    ...     token='your-api-token',
    ...     org='your-organization'
    ... )
    >>> workspaces = client.workspaces.list()

Exception Handling:
    >>> from pytfc import PyTFCError, MissingToken
    >>> try:
    ...     client = pytfc.Client()
    ... except MissingToken:
    ...     print("Set TFE_TOKEN environment variable")
    ... except PyTFCError as e:
    ...     print(f"Library error: {e}")

Available Classes:
    Client: Main API client for TFC/E
    PyTFCError: Base exception for all library errors
    PyTFCConfigurationError: Configuration-related errors
    PyTFCHTTPError: HTTP request errors
"""

from .client import Client
from .exceptions import (
    # Base exceptions
    PyTFCError,
    PyTFCConfigurationError,
    PyTFCHTTPError,
    
    # Specific exceptions
    MissingToken,
    MissingOrganization,
    MissingWorkspace,
    MissingOauthClient,
    MissingVcsProvider,
    MissingRun,
    MissingPlan,
    ConfigurationVersionUploadError,
    InvalidQueryParam,
    PlanExportDownloadError,
)