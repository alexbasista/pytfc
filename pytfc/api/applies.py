"""
Module for TFC/E Applies API endpoint.
"""
from pytfc.tfc_api_base import TfcApiBase


class Applies(TfcApiBase):
    """
    TFC/E Applies methods.
    """
    def show(self, apply_id):
        """
        GET /applies/:id
        """
        path = f'/applies/{apply_id}'
        return self._requestor.get(path=path)