"""
Module for TFC/E Applies API endpoint.
"""


class Applies:
    """
    TFC/E Applies methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
    
    def show(self, apply_id):
        """
        GET /applies/:id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'applies', apply_id]))