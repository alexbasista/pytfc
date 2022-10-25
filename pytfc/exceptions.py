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
    """TFC/E Workspace name or ID not specified."""
    pass


class MissingOauthClient(Exception):
    """TFC/E OAuth Client ID or name not specified."""
    pass


class MissingVcsProvider(Exception):
    """TFC/E OAuth Client not found."""
    pass


class MissingRun(Exception):
    """TFC/E Run ID or commit message not specified."""
    pass


class MissingPlan(Exception):
    """TFC/E Plan not specified."""
    pass


class ConfigurationVersionUploadError(Exception):
    """Error uploading Terraform tar.gz to Configuration Version."""
    pass


class InvalidQueryParam(Exception):
    """Unsupported value for query parameter."""
    pass