"""
Module for TFC/E Applies endpoint.
"""
from pytfc.exceptions import MissingWorkspace


class Applies(object):
    """
    TFC/E Plans methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
        else:
            if self.client.ws:
                self.ws = self.client.ws
            else:
                raise MissingWorkspace
        
        self._ws_id = self.client.workspaces._get_ws_id(self.ws)
        self.applies_endpoint = '/'.join([self.client._base_uri_v2, 'applies'])

    def _get_apply_id(self, **kwargs):
        print('coming soon.')
    
    def show(self, apply_id):
        """
        GET /applies/:id
        """
        return self.client._requestor.get(url="/".join([self.applies_endpoint, apply_id]))