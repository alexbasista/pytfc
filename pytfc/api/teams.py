"""TFC/E Teams API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import InvalidQueryParam


class Teams(TfcApiBase):
    """
    TFC/E Teams methods.
    """
    def list(self, page_number=None, page_size=None, filters=None, include=None):
        """
        GET organizations/:organization_name/teams

        filter example:
        client.teams.list(filters=['[names]=owners]'])
        """
        if filters is not None:
            if not any('[names]=' in f for f in filters):
                self._logger.error(\
                    "`['[names]=<team name>']` is the only valid filter.")
                raise InvalidQueryParam
        
        # TODO:
        # validate `include` is either `users` or `organization-memberships`
        
        path = f'/organizations/{self.org}/teams'
        return self._requestor.get(path=path, page_number=page_number,
                                  page_size=page_size, filters=filters,
                                  include=include)
    
    def list_all(self, filters=None, include=None):
        """
        GET organizations/:organization_name/teams


        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 Teams.

        Returns object (dict) with two arrays: `data` and `included`.

        filter example:
        client.teams.list(filters=['[names]=owners]'])
        """
        if filters is not None:
            if not any('[names]=' in f for f in filters):
                self._logger.error(\
                    "`['[names]=<team name>']` is the only valid filter.")
                raise InvalidQueryParam

        # TODO:
        # validate `include` is either `users` or `organization-memberships`

        path = f'/organizations/{self.org}/teams'
        return self._requestor.list_all(path=path, filters=filters,
                                         include=include)

    def create(self):
        """
        POST /organizations/:organization_name/teams
        """
        print('coming soon')
    
    def show(self, team_id, include=None):
        """
        GET /teams/:team_id
        """
        path = f'/teams/{team_id}'
        return self._requestor.get(path=path, include=include)
    
    def update(self, team_id):
        """
        PATCH /teams/:team_id
        """
        print('coming soon')
    
    def delete(self, team_id):
        """
        DELETE /teams/:team_id
        """
        path = f'/teams/{team_id}'
        return self.clien._requestor.delete(path=path)