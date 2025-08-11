"""
Unit tests for Workspaces API client.
"""
import pytest
from unittest.mock import Mock, call
from pytfc.exceptions import PyTFCError


class TestWorkspacesPayloadBuilding:
    """Test workspace payload building logic."""

    def test_build_workspace_payload_minimal(self, workspaces_client):
        """Test payload building with minimal parameters."""
        result = workspaces_client._build_workspace_payload(name='test-ws')
        
        expected = {
            'data': {
                'type': 'workspaces',
                'attributes': {'name': 'test-ws'}
            }
        }
        assert result == expected

    def test_build_workspace_payload_with_project(self, workspaces_client):
        """Test payload building with project relationship."""
        result = workspaces_client._build_workspace_payload(
            name='test-ws',
            project_id='prj-123'
        )
        
        assert result['data']['relationships'] == {
            'project': {
                'data': {'id': 'prj-123', 'type': 'projects'}
            }
        }

    def test_build_workspace_payload_with_workspace_attrs(self, workspaces_client):
        """Test payload building with workspace attributes."""
        result = workspaces_client._build_workspace_payload(
            name='test-ws',
            auto_apply=True,
            terraform_version='1.6.0',
            working_directory='/terraform'
        )
        
        attrs = result['data']['attributes']
        assert attrs['auto-apply'] is True
        assert attrs['terraform-version'] == '1.6.0' 
        assert attrs['working-directory'] == '/terraform'

    def test_build_workspace_payload_with_vcs_attrs(self, workspaces_client):
        """Test payload building with VCS attributes."""
        result = workspaces_client._build_workspace_payload(
            name='test-ws',
            identifier='org/repo',
            oauth_token_id='ot-123',
            branch='main'
        )
        
        vcs_repo = result['data']['attributes']['vcs-repo']
        assert vcs_repo['identifier'] == 'org/repo'
        assert vcs_repo['oauth-token-id'] == 'ot-123'
        assert vcs_repo['branch'] == 'main'

    def test_build_workspace_payload_remove_vcs(self, workspaces_client):
        """Test payload building to remove VCS integration."""
        result = workspaces_client._build_workspace_payload(
            name='test-ws',
            vcs_repo='null'
        )
        
        assert result['data']['attributes']['vcs-repo'] is None

    def test_build_workspace_payload_underscore_conversion(self, workspaces_client):
        """Test that underscores are converted to hyphens."""
        result = workspaces_client._build_workspace_payload(
            terraform_version='1.6.0',
            oauth_token_id='ot-123'
        )
        
        # Workspace attribute
        assert 'terraform-version' in result['data']['attributes']
        assert 'terraform_version' not in result['data']['attributes']
        
        # VCS attribute  
        vcs_repo = result['data']['attributes']['vcs-repo']
        assert 'oauth-token-id' in vcs_repo
        assert 'oauth_token_id' not in vcs_repo


class TestWorkspacesCRUD:
    """Test workspace CRUD operations."""

    def test_create_success(self, workspaces_client, mock_requestor):
        """Test successful workspace creation."""
        mock_requestor.post.return_value = Mock()
        
        result = workspaces_client.create(name='new-workspace')
        
        # Verify correct API call was made
        mock_requestor.post.assert_called_once()
        call_args = mock_requestor.post.call_args
        
        assert call_args[1]['path'] == '/organizations/test-org/workspaces'
        payload = call_args[1]['payload']
        assert payload['data']['attributes']['name'] == 'new-workspace'

    def test_create_uses_instance_workspace(self, workspaces_client, mock_requestor):
        """Test create uses instance workspace when name not provided."""
        workspaces_client.create()  # No name provided
        
        call_args = mock_requestor.post.call_args
        payload = call_args[1]['payload']
        assert payload['data']['attributes']['name'] == 'test-workspace'

    def test_create_no_workspace_name_fails(self, workspaces_client_no_ws):
        """Test create fails when no workspace name available."""
        with pytest.raises(PyTFCError, match="Workspace name must be provided"):
            workspaces_client_no_ws.create()

    def test_update_success(self, workspaces_client, mock_requestor):
        """Test successful workspace update."""
        workspaces_client.update(name='test-ws', auto_apply=True)
        
        mock_requestor.patch.assert_called_once()
        call_args = mock_requestor.patch.call_args
        
        assert call_args[1]['path'] == '/organizations/test-org/workspaces/test-ws'
        payload = call_args[1]['payload']
        assert payload['data']['attributes']['auto-apply'] is True

    def test_update_with_rename(self, workspaces_client, mock_requestor):
        """Test workspace update with rename."""
        workspaces_client.update(name='old-name', new_name='new-name')
        
        call_args = mock_requestor.patch.call_args
        payload = call_args[1]['payload']
        assert payload['data']['attributes']['name'] == 'new-name'

    def test_list_success(self, workspaces_client, mock_requestor):
        """Test workspace listing."""
        workspaces_client.list(page_number=1, page_size=20)
        
        mock_requestor.get.assert_called_once_with(
            path='/organizations/test-org/workspaces',
            page_number=1,
            page_size=20,
            search=None,
            include=None
        )

    def test_list_all_success(self, workspaces_client, mock_requestor):
        """Test list all workspaces."""
        workspaces_client.list_all(search={'name': 'test'})
        
        mock_requestor.list_all.assert_called_once_with(
            path='/organizations/test-org/workspaces',
            search={'name': 'test'},
            include=None
        )

    def test_show_success(self, workspaces_client, mock_requestor):
        """Test showing specific workspace."""
        workspaces_client.show(name='test-ws')
        
        mock_requestor.get.assert_called_once_with(
            path='/organizations/test-org/workspaces/test-ws'
        )

    def test_delete_success(self, workspaces_client, mock_requestor):
        """Test workspace deletion."""
        workspaces_client.delete(name='test-ws')
        
        mock_requestor.delete.assert_called_once_with(
            path='/organizations/test-org/workspaces/test-ws'
        )


class TestWorkspaceActions:
    """Test workspace action methods (lock, unlock, etc.)."""

    def test_lock_success(self, workspaces_client, mock_requestor):
        """Test workspace locking."""
        # Mock the get_workspace_id call
        mock_response = Mock(spec=['json'])  # Only has json method, no data attribute
        mock_response.json.return_value = {'data': {'id': 'ws-123abc'}}
        mock_requestor.get.return_value = mock_response
        
        workspaces_client.lock(name='test-ws', reason='Maintenance')
        
        # Should call get to get workspace ID, then post to lock
        assert mock_requestor.get.call_count == 1
        mock_requestor.post.assert_called_once_with(
            path='/workspaces/ws-123abc/actions/lock',
            payload={'reason': 'Maintenance'}
        )

    def test_unlock_success(self, workspaces_client, mock_requestor):
        """Test workspace unlocking."""
        mock_response = Mock(spec=['json'])  # Only has json method, no data attribute
        mock_response.json.return_value = {'data': {'id': 'ws-123abc'}}
        mock_requestor.get.return_value = mock_response
        workspaces_client.unlock(name='test-ws')
        
        mock_requestor.post.assert_called_once_with(
            path='/workspaces/ws-123abc/actions/unlock',
            payload=None
        )

    def test_force_unlock_success(self, workspaces_client, mock_requestor):
        """Test workspace force unlock."""
        mock_response = Mock(spec=['json'])  # Only has json method, no data attribute
        mock_response.json.return_value = {'data': {'id': 'ws-123abc'}}
        mock_requestor.get.return_value = mock_response
        
        workspaces_client.force_unlock(name='test-ws')
        
        mock_requestor.post.assert_called_once_with(
            path='/workspaces/ws-123abc/actions/force-unlock',
            payload=None
        )


class TestWorkspaceUtilities:
    """Test workspace utility methods."""

    def test_get_workspace_id_success(self, workspaces_client, mock_requestor):
        """Test getting workspace ID from name."""
        mock_response = Mock(spec=['json'])
        mock_response.json.return_value = {'data': {'id': 'ws-123abc'}}
        mock_requestor.get.return_value = mock_response
        
        result = workspaces_client.get_workspace_id('test-ws')
        
        assert result == 'ws-123abc'
        mock_requestor.get.assert_called_once_with(
            path='/organizations/test-org/workspaces/test-ws'
        )

    def test_get_workspace_id_api_error(self, workspaces_client, mock_requestor):
        """Test get workspace ID handles API errors."""
        mock_requestor.get.side_effect = Exception("API Error")
        
        with pytest.raises(PyTFCError, match="Failed to get workspace ID"):
            workspaces_client.get_workspace_id('test-ws')

    def test_get_workspace_name_success(self, workspaces_client, mock_requestor):
        """Test getting workspace name from ID."""
        mock_response = Mock(spec=['json'])
        mock_response.json.return_value = {
            'data': {'attributes': {'name': 'test-workspace'}}
        }
        mock_requestor.get.return_value = mock_response
        
        result = workspaces_client.get_workspace_name('ws-123abc')
        
        assert result == 'test-workspace'
        mock_requestor.get.assert_called_once_with(path='/workspaces/ws-123abc')
