"""
TFE Admin Workspaces API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminWorkspaces(TfcApiBase):
    """
    TFE Admin Workspaces methods.
    """
    def list(self, query=None, filters=None, page_number=None,
             page_size=None, include=None):
        """
        GET /api/v2/admin/workspaces
        """
        return self._requestor.get(path='/admin/workspaces', query=query,
                                   filters=filters, page_number=page_number,
                                   page_size=page_size, include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/workspaces

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspaces.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self._requestor.list_all(path='/admin/workspaces', query=query,
                                        filters=filters, include=include)
    
    def show(self, ws_id, include=None):
        """
        GET /api/v2/admin/workspaces/:id
        """
        path = f'/admin/workspaces/{ws_id}'
        return self._requestor.get(path=path, include=include)

    def delete(self, ws_id):
        """
        DELETE /admin/workspaces/:id
        """
        path = f'/admin/workspaces/{ws_id}'
        return self._requestor.delete(path=path)