"""
Shared pytest configuration and fixtures for all tests.
"""
import pytest
from unittest.mock import Mock, MagicMock
import pytfc
from pytfc.tfc_api_base import TfcApiBase
from pytfc.api.workspaces import Workspaces


@pytest.fixture
def mock_requestor():
    """Mock requestor for unit tests - no real API calls."""
    mock = Mock()
    
    # Mock common response patterns
    mock.get.return_value = Mock()
    mock.post.return_value = Mock()
    mock.patch.return_value = Mock()
    mock.delete.return_value = Mock()
    mock.list_all.return_value = {'data': [], 'included': []}
    
    return mock


@pytest.fixture
def base_api_instance(mock_requestor):
    """Base API instance for testing base class functionality."""
    return TfcApiBase(
        requestor=mock_requestor,
        org='test-org',
        ws='test-workspace',
        ws_id='ws-123abc',
        log_level='WARNING'
    )


@pytest.fixture
def workspaces_client(mock_requestor):
    """Workspaces client instance for testing."""
    return Workspaces(
        requestor=mock_requestor,
        org='test-org',
        ws='test-workspace', 
        ws_id='ws-123abc',
        log_level='WARNING'
    )


@pytest.fixture
def workspaces_client_no_ws(mock_requestor):
    """Workspaces client without workspace set."""
    return Workspaces(
        requestor=mock_requestor,
        org='test-org',
        ws=None,
        ws_id=None,
        log_level='WARNING'
    )


@pytest.fixture
def sample_workspace_response():
    """Sample API response for workspace operations."""
    return {
        'data': {
            'id': 'ws-123abc',
            'type': 'workspaces',
            'attributes': {
                'name': 'test-workspace',
                'auto-apply': True,
                'terraform-version': '1.6.0',
                'working-directory': '/terraform'
            },
            'relationships': {
                'project': {
                    'data': {'id': 'prj-456def', 'type': 'projects'}
                }
            }
        }
    }


@pytest.fixture
def sample_workspace_list_response():
    """Sample API response for workspace list operations."""
    return {
        'data': [
            {
                'id': 'ws-123abc',
                'type': 'workspaces',
                'attributes': {'name': 'test-workspace-1'}
            },
            {
                'id': 'ws-456def', 
                'type': 'workspaces',
                'attributes': {'name': 'test-workspace-2'}
            }
        ],
        'meta': {
            'pagination': {
                'current-page': 1,
                'page-size': 20,
                'total-pages': 1,
                'total-count': 2
            }
        }
    }