"""TFC/E State Versions API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set, validate_ws_is_set
from urllib import request


class StateVersions(TfcApiBase):
    """
    TFC/E State Versions methods.
    """
    @validate_ws_id_is_set
    def create(self, serial, md5, state, lineage=None, run_id=None, ws_id=None):
        """
        POST /workspaces/:workspace_id/state-versions
        """
        ws_id = ws_id if ws_id else self.ws_id

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

        path = f'/workspaces/{ws_id}/state-versions'
        return self._requestor.post(path=path, payload=payload)

    @validate_ws_is_set
    def list(self, page_number=None, page_size=None, include=None, ws=None):
        """
        GET /state-versions
        """
        ws = ws if ws else self.ws

        filters = [
            f'[workspace][name]={ws}',
            f'[organization][name]={self.org}'
        ]

        return self._requestor.get(path='/state-versions', filters=filters,
                                   page_number=page_number, page_size=page_size,
                                   include=include)

    @validate_ws_is_set
    def list_all(self, include=None, ws=None):
        """
        GET /state-versions

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 State Versions.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        ws = ws if ws else self.ws
        
        filters = [
            f'[workspace][name]={ws}',
            f'[organization][name]={self.org}'
        ]

        return self._requestor.list_all(path='/state-versions',
                                         filters=filters, include=include)

    @validate_ws_id_is_set
    def get_current(self, include=None, ws_id=None):
        """
        GET /workspaces/:workspace_id/current-state-version
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/current-state-version'
        return self._requestor.get(path=path, include=include)
    
    def show(self, sv_id, include=None):
        """
        GET /state-versions/:state_version_id
        """
        path = f'/state-versions/{sv_id}'
        return self._requestor.get(path=path, include=include)
    
    def get_download_url(self, sv_id=None):
        """
        Helper method to return
        `hosted-state-download-url` of a State Version.
        Uses current State Version of Workspace
        if a State Version ID is not specified.
        """
        if sv_id is None:
            self._logger.debug(\
                "Getting download URL from current State Version.")
            sv = self.get_current()
        else:
            self._logger.debug(\
                f"Getting download URL from State Version `{sv_id}`.")
            sv = self.show(sv_id=sv_id)
        
        return sv.json()\
            ['data']['attributes']['hosted-state-download-url']
    
    def get_json_download_url(self, sv_id=None):
        """
        Helper method to return
        `hosted-json-state-download-url` of a State Version.
        Uses current State Version of Workspace
        if a State Version ID is not specified.
        """
        if sv_id is None:
            self._logger.debug(\
                "Getting JSON download URL from current State Version.")
            sv = self.get_current()
        else:
            self._logger.debug(\
                f"Getting JSON download URL from State Version `{sv_id}`.")
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
        url = self.get_download_url()
        state_dl_req = request.Request(url=url, headers=headers, data=None)
        state_dl = request.urlopen(state_dl_req, context=context)
        state_obj = state_dl.read()
        return state_obj