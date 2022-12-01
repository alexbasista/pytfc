"""TFC/E Notification Configurations API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class NotificationConfigurations(TfcApiBase):
    """
    TFC/E Notification Configurations methods.
    """
    @validate_ws_id_is_set
    def create(self, name, destination_type, enabled=False, token=None,
               triggers=None, url=None, users=None, ws_id=None):
        """
        POST /workspaces/:workspace_id/notification-configurations
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')
    
    @validate_ws_id_is_set
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/notification-configurations
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/notification-configurations'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)
    
    def show(self, nc_id):
        """
        GET /notification-configurations/:notification-configuration-id
        """
        path = f'/notification-configurations/{nc_id}'
        return self._requestor.get(path=path)
    
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
        path = f'/notification-configurations/{nc_id}'
        return self._requestor.delete(path=path)