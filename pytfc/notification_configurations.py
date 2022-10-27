"""
Module for TFC/E Notification Configurations API endpoint.
"""
from .exceptions import MissingWorkspace


class NotificationConfigurations:
    """
    TFC/E Notification Configurations methods.
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

    def create(self, name, destination_type, enabled=False, token=None,
            triggers=None, url=None, users=None, ws_id=None):
        """
        POST /workspaces/:workspace_id/notification-configurations
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        print('coming soon')
    
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/notification-configurations
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'notification-configurations']),
            page_number=page_number, page_size=page_size)
    
    def show(self, nc_id):
        """
        GET /notification-configurations/:notification-configuration-id
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'notification-configurations', nc_id]))
    
    def update(self, nc_id):
        """
        PATCH /notification-configurations/:notification-configuration-id
        """
        print('coming soon')
    
    def verify(self, nc_id):
        """
        POST /notification-configurations/:notification-configuration-id/actions/verify
        """
        print('coming soon')

    def delete(self, nc_id):
        """
        DELETE /notification-configurations/:notification-configuration-id
        """
        return self.client._requestor.delete(url='/'.join([self._base_api_url,
            'notification-configurations', nc_id]))