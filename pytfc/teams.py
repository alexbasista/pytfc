"""
Module for TFC/E Teams API endpoint.
"""
from .exceptions import InvalidQueryParam


class Teams:
    """
    TFC/E Teams methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._teams_ep = '/'.join([self.client._base_uri_v2,
            'organizations', self.client.org, 'teams'])

    def list(self, page_number=None, page_size=None, filters=None, include=None):
        """
        GET organizations/:organization_name/teams

        filter example:
        client.teams.list(filters=['[names]=owners]'])
        """
        if not any('[names]=' in f for f in filters):
            self._logger.error(\
                "`['[names]=<team name>]']` is the only valid filter.")
            raise InvalidQueryParam
        
        return self.client._requestor.get(url=self._teams_ep,
            page_number=page_number, page_size=page_size,
            filters=filters, include=include)

    def create(self):
        """
        POST /organizations/:organization_name/teams
        """
        print('coming soon')
    
    def show(self, team_id, include=None):
        """
        GET /teams/:team_id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id]), include=include)
    
    def update(self, team_id):
        """
        PATCH /teams/:team_id
        """
        print('coming soon')
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id
        """
        return self.clien._requestor.delete(url='/'.join([
            self.client._base_uri_v2, 'teams', team_id]))