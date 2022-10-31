"""
Module for TFC/E Workspace Resources API endpoint.
"""
from .exceptions import MissingWorkspace


class WorkspaceResources:
    """ 
    TFC/E Workspace Resources methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._base_api_url = client._base_uri_v2
        
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
        GET /workspaces/:workspace_id/resources
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'resources']), page_number=page_number,
            page_size=page_size)

    def list_all(self, ws_id=None):
        """
        GET /workspaces/:workspace_id/resources

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspace Resoures.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor._list_all(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'resources']))
