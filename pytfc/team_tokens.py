"""
Module for TFC/E Team Tokens API endpoint.
"""


class TeamTokens:
    """
    TFC/E Team Tokens methods.
    """
    def __init__(self, client):
        self.client = client
    
    def generate_new(self, team_id):
        """
        POST /teams/:team_id/authentication-token
        """
        return self.client._requestor.post(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id,
            'authentication-token']), payload=None)
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id/authentication-token
        """
        return self.client._requestor.delete(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id,
            'authentication-token']))