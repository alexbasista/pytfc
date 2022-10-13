"""
Module for TFC/E Policy Checks API endpoint.
"""
from .exceptions import MissingWorkspace


class PolicyChecks(object):
    """
    TFC/E Policy Checks methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self._ws_id = self.client.workspaces._get_ws_id(name=self.ws)
        else:
            if self.client.ws:
                self.ws = self.client.ws
                self._ws_id = self.client._ws_id
            else:
                raise MissingWorkspace

    def list(self, **kwargs):
        """
        GET /runs/:run_id/policy-checks

        Defaults to querying latest Run ID in Workspace if no args passed.
        """
        if kwargs.get('run_id'): #and kwargs.get('run_id') != 'latest':
            run_id = kwargs.get('run_id')
        elif kwargs.get('commit_message'):
            run_id = self.client.runs._get_run_id_by_commit(commit_message=kwargs.get('commit_message'))
        else:
            run_id = self.client.runs._get_latest_run_id()
        
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2, 'runs', run_id, 'policy-checks']))