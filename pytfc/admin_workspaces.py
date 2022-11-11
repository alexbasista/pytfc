"""
Module for TFE Admin Workspaces API endpoints.
For Terraform Enterprise only.
"""


class AdminWorkspaces:
    """
    TFE Admin Workspaces methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._aw_endpoint = '/'.join([self.client._base_uri_v2, 'admin',
            'workspaces'])
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
        """
        GET /api/v2/admin/workspaces
        """
        return self.client._requestor.get(url=self._aw_endpoint, query=query,
            filters=filters, page_number=page_number, page_size=page_size,
            include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/workspaces

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspaces.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self.client._requestor._list_all(url=self._aw_endpoint,
             query=query, filters=filters, include=include)
    
    def show(self, ws_id, include=None):
        """
        GET /api/v2/admin/workspaces/:id
        """
        return self.client._requestor.get(url='/'.join([self._aw_endpoint,
            ws_id]), include=include)

    def delete(self, ws_id):
        """
        DELETE /admin/workspaces/:id
        """
        return self.client._requestor.delete(url='/'.join([
            self._aw_endpoint, ws_id]))