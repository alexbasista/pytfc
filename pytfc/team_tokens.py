"""
Module for TFC/E Team Tokens API endpoint.
"""
from .exceptions import InvalidQueryParam


class TeamTokens:
    """
    TFC/E Team Tokens methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._tt_ep = '/'.join([self.client._base_uri_v2,
            'organizations', self.client.org, 'teams'])
    
    def generate_new(self, team_id):
        """
        POST /teams/:team_id/authentication-token
        """
        return self.client._requestor.post(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id,
            'authentication-token']))
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id/authentication-token
        """
        return self.client._requestor.delete(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id,
            'authentication-token']))