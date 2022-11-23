"""
Module for TFC/E Team Tokens API endpoint.
"""
from pytfc.tfc_api_base import TfcApiBase


class TeamTokens(TfcApiBase):
    """
    TFC/E Team Tokens methods.
    """
    def generate_new(self, team_id):
        """
        POST /teams/:team_id/authentication-token
        """
        path = f'/teams/{team_id}/authentication-token'
        return self._requestor.post(path=path, payload=None)
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id/authentication-token
        """
        path = f'/teams/{team_id}/authentication-token'
        return self._requestor.delete(path=path)