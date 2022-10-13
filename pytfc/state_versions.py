"""
Module for TFC/E State Versions endpoints.
"""
from urllib import request
from .exceptions import MissingWorkspace


class StateVersions(object):
    """
    TFC/E State Versions methods.
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

        self._sv_endpoint = '/'.join([self.client._base_uri_v2, 'workspaces',
                                      self._ws_id, 'state-versions'])
    
    def create(self, serial, md5, state, lineage=None, run_id=None):
        """
        POST /workspaces/:workspace_id/state-versions
        """
        payload = {}
        data = {}
        data['type'] = 'state-versions'
        attributes = {}
        attributes['serial'] = serial
        attributes['md5'] = md5
        attributes['state'] = state
        attributes['lineage'] = lineage
        attributes['json-state'] = None
        attributes['json-state-outputs'] = None
        data['attributes'] = attributes
        relationships = {}
        relationships_run = {}
        relationships_run_data = {}
        relationships_run_data['id'] = run_id
        relationships_run['data'] = relationships_run_data
        relationships['run'] = relationships_run
        data['relationships'] = relationships
        payload['data'] = data

        return self.client._requestor.post(url=self._sv_endpoint, payload=payload)

    def list(self, page_number=None, page_size=None):
        """
        GET /state-versions
        """
        base_url = '/'.join([self.client._base_uri_v2,'state-versions'])
        filters = [f'[workspace][name]={self.ws}', f'[organization][name]={self.client.org}'] 

        return self.client._requestor.get(url=base_url, filters=filters, page_number=page_number, page_size=page_size)

    def get_current(self):
        """
        GET /workspaces/:workspace_id/current-state-version
        """
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
                                                        'workspaces', self._ws_id,
                                                        'current-state-version']))
    
    def show(self, sv_id):
        """
        GET /state-versions/:state_version_id
        """
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
                                                        'state-versions', sv_id]))

    def _get_download_url(self, sv_id=None):
        """
        Helper method to return
        `hosted-state-download-url` of a State Version.
        Uses current State Version of Workspace
        if a State Version ID is not specified.
        """
        if sv_id is None:
            sv = self.get_current()
        else:
            sv = self.show(sv_id=sv_id)
        
        return sv.json()['data']['attributes']['hosted-state-download-url']
    
    def _get_json_download_url(self, sv_id=None):
        """
        Helper method to return
        `hosted-json-state-download-url` of a State Version.
        Uses current State Version of Workspace
        if a State Version ID is not specified.
        """
        if sv_id is None:
            sv = self.get_current()
        else:
            sv = self.show(sv_id=sv_id)
        
        return sv.json()['data']['attributes']['hosted-json-state-download-url']
    
    def download(self, url):
        """
        Utility method to download a State Version
        based on the download URL that is specified.
        Returns raw state object in bytes.
        """
        state_dl = request.urlopen(url=url, data=None)
        state_obj = state_dl.read()
        return state_obj
    
    def download_current(self):
        """
        Utility method to download the current
        State Version of the Workspace.
        Returns raw state object in bytes.
        """
        url = self._get_download_url()
        state_dl = request.urlopen(url=url, data=None)
        state_obj = state_dl.read()
        return state_obj