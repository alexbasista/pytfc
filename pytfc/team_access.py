"""
Module for TFC/E Team Access API endpoint.
"""
from .exceptions import MissingWorkspace


class TeamAccess:
    """
    TFC/E Team Access methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client

        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None
    
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /team-workspaces

        Required Query Parameters:
        filter[workspace][id]
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        filters = [
            f'[workspace][id]={ws_id}'
        ]

        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'team-workspaces']),
            filters=filters, page_number=page_number,
            page_size=page_size)
    
    def list_all(self, ws_id=None):
        """
        GET /team-workspaces

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Team Workspace Access items.

        Returns object (dict) with two arrays: `data` and `included`.

        Required Query Parameters:
        filter[workspace][id]
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        filters = [
            f'[workspace][id]={ws_id}'
        ]

        return self.client._requestor._list_all(url='/'.join([
            self.client._base_uri_v2, 'team-workspaces']), filters=filters)
            

    def show(self, tws_id):
        """
        GET /team-workspaces/:id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'team-workspaces', tws_id]))

    def add(self, access, runs=None, variables=None, state_versions=None,
            sentinel_mocks=None, workspace_locking=None, run_taks=None, ws_id=None):
        """
        POST /team-workspaces
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        valid_access = [
            'read',
            'plan',
            'write',
            'admin',
            'custom'
        ]

        if access not in valid_access:
            raise ValueError
        
        print('the rest coming soon')
        
    def update(self):
        """
        PATCH /team-workspaces/:id
        """
        print('coming soon')
    
    def delete(self, tws_id):
        """
        DELETE /team-workspaces/:id
        """
        return self.client._requestor.delete(url='/'.join([
            self.client._base_uri_v2, 'team-workspaces', tws_id]))