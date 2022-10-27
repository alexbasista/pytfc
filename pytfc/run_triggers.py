"""
Module for TFC/E Run Triggers API endpoints.
"""
from .exceptions import MissingWorkspace


class RunTriggers:
    """
    TFC/E Run Triggers methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
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
    
    def create(self, source_ws_obj, ws_id=None):
        """
        POST /workspaces/:workspace_id/run-triggers

        :param source_ws_obj: Source Workspace for Run Trigger.
        :type source_ws_obj: Object with `id` and `type` properties. For example:
            { "id": "ws-abcdefghijklmnop", "type": "workspaces" }
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        print('coming soon')

    def list(self, rt_type, ws_id=None, page_number=None, page_size=None,
            include=None):
        """
        GET /workspaces/:workspace_id/run-triggers
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        if rt_type not in ['inbound', 'outbound']:
            self._logger.error(\
                f"`{rt_type}` is invalid for `rt_type` arg. Valid values are `inbound` and `outbound`.")
            raise ValueError

        filters = [
            f'[run-trigger][type]={rt_type}'
        ]

        # TODO:
        # validate include is either `workspace` or `sourceable`
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'run-triggers']), filters=filters,
            page_number=page_number, page_size=page_size, include=include)
        
    def show(self, rt_id, include=None):
        """
        GET /run-triggers/:run_trigger_id
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'run-triggers', rt_id]), include=include)
    
    def delete(self, rt_id):
        """
        DELETE /run-triggers/:run_trigger_id
        """
        return self.client._requestor.delete(url='/'.join([self._base_api_url,
            'run-triggers', rt_id]))