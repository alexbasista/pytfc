"""
Module for TFE Admin Workspaces API endpoints.
For Terraform Enterprise only.
"""
from .requestor import Requestor


class AdminWorkspaces(Requestor):
    """
    TFE Admin Workspaces methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self._aw_endpoint = '/'.join([base_uri, 'admin', 'workspaces'])

        super().__init__(headers, log_level, verify)
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
        """
        GET /api/v2/admin/workspaces
        """
        return self.get(url=self._aw_endpoint, query=query, filters=filters,
            page_number=page_number, page_size=page_size, include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/workspaces

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspaces.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self._list_all(url=self._aw_endpoint, query=query,
            filters=filters, include=include)
    
    def show(self, ws_id, include=None):
        """
        GET /api/v2/admin/workspaces/:id
        """
        return self.get(url='/'.join([self._aw_endpoint, ws_id]),
            include=include)

    def delete(self, ws_id):
        """
        DELETE /admin/workspaces/:id
        """
        return self.delete(url='/'.join([self._aw_endpoint, ws_id]))