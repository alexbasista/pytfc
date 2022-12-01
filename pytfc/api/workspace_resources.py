"""
Module for TFC/E Workspace Resources API endpoint.
"""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set
from pytfc.exceptions import MissingWorkspace


class WorkspaceResources(TfcApiBase):
    """ 
    TFC/E Workspace Resources methods.
    """
    @validate_ws_id_is_set
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/resources
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        path = f'/workspaces/{ws_id}/resources'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    @validate_ws_id_is_set
    def list_all(self, ws_id=None):
        """
        GET /workspaces/:workspace_id/resources

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspace Resoures.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        ws_id = ws_id if ws_id else self.ws_id

        path = f'/workspaces/{ws_id}/resources'
        return self._requestor.list_all(path=path)
