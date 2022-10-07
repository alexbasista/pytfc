"""
Module for custom pytfc exceptions.
"""


class Error(Exception):
    """Base class for general exceptions."""
    pass


class MissingToken(Exception):
    """TFC/E Token not specified."""
    pass


class MissingOrganization(Exception):
    """TFC/E Organization not specified."""
    pass


class MissingWorkspace(Exception):
    """TFC/E Workspace name not specified."""
    pass


class MissingOauthClient(Exception):
    """TFC/E OAuth Client display name not specified."""
    pass


class MissingVcsProvider(Exception):
    """TFC/E OAuth Client not found."""
    pass


class MissingRunId(Exception):
    """TFC/E Run ID not found based on specified commit message."""
    pass


class ConfigurationVersionUploadError(Exception):
    """Error uploading Terraform tar.gz to Configuration Version."""
    pass


class InvalidQueryParam(Exception):
    """Unsupported value for query parameter."""
    pass