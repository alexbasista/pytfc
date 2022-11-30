"""TFC/E Team Access API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class TeamAccess(TfcApiBase):
    """
    TFC/E Team Access methods.
    """
    @validate_ws_id_is_set
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /team-workspaces

        Required Query Parameters:
        filter[workspace][id]
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        filters = [
            f'[workspace][id]={ws_id}'
        ]

        return self._requestor.get(path='team-workspaces', filters=filters,
                                   page_number=page_number, page_size=page_size)

    @validate_ws_id_is_set
    def list_all(self, ws_id=None):
        """
        GET /team-workspaces

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Team Workspace Access items.

        Returns object (dict) with two arrays: `data` and `included`.

        Required Query Parameters:
        filter[workspace][id]
        """
        ws_id = ws_id if ws_id else self.ws_id

        filters = [
            f'[workspace][id]={ws_id}'
        ]

        return self._requestor.list_all(path='team-workspaces', filters=filters)

    def show(self, tws_id):
        """
        GET /team-workspaces/:id
        """
        path = f'/team-workspaces/{tws_id}'
        return self._requestor.get(path=path)

    @validate_ws_id_is_set
    def add(self, access, runs=None, variables=None, state_versions=None,
            sentinel_mocks=None, workspace_locking=None, run_taks=None,
            ws_id=None):
        """
        POST /team-workspaces
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        valid_access = [
            'read',
            'plan',
            'write',
            'admin',
            'custom'
        ]

        if access not in valid_access:
            raise ValueError
        
        print('coming soon')

    def update(self):
        """
        PATCH /team-workspaces/:id
        """
        print('coming soon')

    def delete(self, tws_id):
        """
        DELETE /team-workspaces/:id
        """
        path = f'/team-workspaces/{tws_id}'
        return self._requestor.delete(path=path)