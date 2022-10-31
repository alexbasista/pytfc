"""
Module for TFC/E State Versions API endpoints.
"""
from urllib import request
from .exceptions import MissingWorkspace


class StateVersions:
    """
    TFC/E State Versions methods.
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

    def create(self, serial, md5, state, lineage=None, run_id=None, ws_id=None):
        """
        POST /workspaces/:workspace_id/state-versions
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        url = '/'.join([
            self.client._base_uri_v2, 'workspaces', ws_id, 'state-versions'
        ])

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

        return self.client._requestor.post(url=url, payload=payload)

    def list(self, page_number=None, page_size=None, include=None, ws=None):
        """
        GET /state-versions
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace
        
        base_url = '/'.join([self.client._base_uri_v2,'state-versions'])
        filters = [
            f'[workspace][name]={ws}',
            f'[organization][name]={self.client.org}'
        ]

        return self.client._requestor.get(url=base_url, filters=filters,
            page_number=page_number, page_size=page_size, include=include)

    def list_all(self, include=None, ws=None):
        """
        GET /state-versions

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 State Versions.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace
        
        base_url = '/'.join([self.client._base_uri_v2,'state-versions'])
        filters = [
            f'[workspace][name]={ws}',
            f'[organization][name]={self.client.org}'
        ]

        return self.client._requestor._list_all(url=base_url, filters=filters,
            include=include)

    def get_current(self, include=None, ws_id=None):
        """
        GET /workspaces/:workspace_id/current-state-version
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
            'workspaces', ws_id, 'current-state-version']), include=include)
    
    def show(self, sv_id, include=None):
        """
        GET /state-versions/:state_version_id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'state-versions', sv_id]),
            include=include)
    
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
        
        return sv.json()\
            ['data']['attributes']['hosted-state-download-url']
    
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

        return sv.json()\
            ['data']['attributes']['hosted-json-state-download-url']
    
    def download(self, url, context=None, headers={}):
        """
        Utility method to download a State Version
        based on the download URL that is specified.
        Returns raw state object in bytes.
        """
        state_dl_req = request.Request(url=url, headers=headers, data=None)
        state_dl = request.urlopen(state_dl_req, context=context)
        state_obj = state_dl.read()
        return state_obj
    
    def download_current(self, context=None, headers={}):
        """
        Utility method to download the current
        State Version of the Workspace.
        Returns raw state object in bytes.
        """
        url = self._get_download_url()
        state_dl_req = request.Request(url=url, headers=headers, data=None)
        state_dl = request.urlopen(state_dl_req, context=context)
        state_obj = state_dl.read()
        return state_obj