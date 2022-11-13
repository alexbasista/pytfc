"""
Module for TFC/E Team Tokens API endpoint.
"""
from .requestor import Requestor


class TeamTokens(Requestor):
    """
    TFC/E Team Tokens methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self._teams_endpoint = '/'.join([base_uri, 'teams'])

        super().__init__(headers, log_level, verify)
    
    def generate_new(self, team_id):
        """
        POST /teams/:team_id/authentication-token
        """
        return self.post(url='/'.join([self._teams_endpoint, team_id,
            'authentication-token']), payload=None)
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id/authentication-token
        """
        return self.delete(url='/'.join([self._teams_endpoint, team_id,
            'authentication-token']))