"""
Module for TFC/E State Versions endpoint.
"""
from pytfc.exceptions import MissingWorkspace


class StateVersions(object):
    """
    TFC/E State Versions methods.
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
    
    def create(self):
        """
        POST /workspaces/:workspace_id/state-versions
        """
        print('coming soon.')
    
    def list(self):
        """
        GET /state-versions
        """
        print('coming soon.')
    
    def _get_sv_id(self):
        """
        Helper method to return State
        Version ID based on something.
        """
        print('coming soon.')

    def get_current(self):
        """
        GET /workspaces/:workspace_id/current-state-version
        """
        print('coming soon.')
    
    def show(self):
        """
        GET /state-versions/:state_version_id
        """
        print('coming soon.')