"""
Module for TFC/E Applies API endpoint.
"""
from .exceptions import MissingWorkspace


class Applies(object):
    """
    TFC/E Applies methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self._ws_id = self.client.workspaces._get_ws_id(name=self.ws)
        else:
            if self.client.ws:
                self.ws = self.client.ws
                self._ws_id = self.client._ws_id
            else:
                raise MissingWorkspace

        self.applies_endpoint = '/'.join([self.client._base_uri_v2, 'applies'])

    def _get_apply_id(self, run_id='latest', **kwargs):
        """
        Helper method to return Apply ID.
        Defaults to using latest Run ID.
        """
        if kwargs.get('commit_message'):
            run_object = self.client.runs.show(commit_message=kwargs.get('commit_message'))
        else:
            run_object = self.client.runs.show(run_id=run_id)
        
        if run_object.json()['data']['relationships']['apply']['data'] == []:
            self._logger.warning("No Apply ID was found.")
            return None
        else:
            return run_object.json()['data']['relationships']['apply']['data']['id']
    
    def show(self, **kwargs):
        """
        GET /applies/:id

        Defaults to querying latest Run ID in Workspace if no args passed.
        """
        if kwargs.get('apply_id') and kwargs.get('apply_id') != 'latest':
            apply_id = kwargs.get('apply_id')
        elif kwargs.get('commit_message'):
            apply_id = self._get_apply_id(commit_message=kwargs.get('commit_message'))
        elif kwargs.get('run_id'):
            apply_id = self._get_apply_id(run_id=kwargs.get('run_id'))
        else:
            apply_id = self._get_apply_id(run_id='latest')

        return self.client._requestor.get(url="/".join([self.applies_endpoint, apply_id]))