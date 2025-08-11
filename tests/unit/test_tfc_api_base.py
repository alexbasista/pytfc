"""
Unit tests for TfcApiBase class functionality.
"""
import pytest
from pytfc.exceptions import PyTFCError
from unittest.mock import Mock

class TestTfcApiBase:
    """Test cases for TfcApiBase helper methods."""

    def test_get_org_path_success(self, base_api_instance):
        """Test successful organization path generation."""
        result = base_api_instance._get_org_path()
        assert result == '/organizations/test-org'

    def test_get_org_path_no_org_set(self, mock_requestor):
        """Test error when no organization is set."""
        from pytfc.tfc_api_base import TfcApiBase
        
        api = TfcApiBase(
            requestor=mock_requestor,
            org=None,  # No org set
            ws=None,
            ws_id=None,
            log_level='WARNING'
        )
        
        with pytest.raises(PyTFCError, match="Organization must be set"):
            api._get_org_path()

    def test_get_workspace_path_success(self, base_api_instance):
        """Test successful workspace path generation."""
        result = base_api_instance._get_workspace_path()
        assert result == '/workspaces/ws-123abc'

    def test_get_workspace_path_with_override(self, base_api_instance):
        """Test workspace path with ID override."""
        result = base_api_instance._get_workspace_path('ws-override')
        assert result == '/workspaces/ws-override'

    def test_get_workspace_path_no_ws_id(self, mock_requestor):
        """Test error when no workspace ID is available."""
        from pytfc.tfc_api_base import TfcApiBase
        
        api = TfcApiBase(
            requestor=mock_requestor,
            org='test-org',
            ws=None,
            ws_id=None,  # No workspace ID
            log_level='WARNING'
        )
        
        with pytest.raises(PyTFCError, match="Workspace ID must be set"):
            api._get_workspace_path()

    def test_resolve_ws_name_from_param(self, base_api_instance):
        """Test workspace name resolution from parameter."""
        result = base_api_instance._resolve_ws_name('param-workspace')
        assert result == 'param-workspace'

    def test_resolve_ws_name_from_instance(self, base_api_instance):
        """Test workspace name resolution from instance attribute."""
        result = base_api_instance._resolve_ws_name(None)
        assert result == 'test-workspace'

    def test_resolve_ws_name_no_value(self, mock_requestor):
        """Test error when no workspace name is available."""
        from pytfc.tfc_api_base import TfcApiBase
        
        api = TfcApiBase(
            requestor=mock_requestor,
            org='test-org',
            ws=None,  # No workspace name
            ws_id=None,
            log_level='WARNING'
        )
        
        with pytest.raises(PyTFCError, match="Workspace name must be provided"):
            api._resolve_ws_name(None)

    def test_resolve_ws_id_from_param(self, base_api_instance):
        """Test workspace ID resolution from parameter."""
        result = base_api_instance._resolve_ws_id('ws-param')
        assert result == 'ws-param'

    def test_resolve_ws_id_from_instance(self, base_api_instance):
        """Test workspace ID resolution from instance attribute."""
        result = base_api_instance._resolve_ws_id(None)
        assert result == 'ws-123abc'

    def test_validate_choice_valid(self, base_api_instance):
        """Test validation with valid choice."""
        # Should not raise an exception
        base_api_instance._validate_choice('terraform', ['terraform', 'env'], 'category')

    def test_validate_choice_invalid(self, base_api_instance):
        """Test validation with invalid choice."""
        with pytest.raises(PyTFCError, match="Invalid value 'invalid' for parameter 'category'"):
            base_api_instance._validate_choice('invalid', ['terraform', 'env'], 'category')

    def test_extract_response_data_dict(self, base_api_instance):
        """Test response data extraction from dict."""
        response_data = {'data': {'id': 'test'}}
        result = base_api_instance._extract_response_data(response_data)
        assert result == response_data

    def test_extract_response_data_mock_with_data_attr(self, base_api_instance):
        """Test response data extraction from object with data attribute."""
        mock_response = Mock()
        mock_response.data = {'extracted': 'from_data_attr'}
        
        result = base_api_instance._extract_response_data(mock_response)
        assert result == {'extracted': 'from_data_attr'}

    def test_extract_response_data_mock_with_json(self, base_api_instance):
        """Test response data extraction from mock with json() method."""
        mock_response = Mock(spec=['json'])  # Only has json method
        mock_response.json.return_value = {'data': {'id': 'test'}}
        
        result = base_api_instance._extract_response_data(mock_response)
        assert result == {'data': {'id': 'test'}}