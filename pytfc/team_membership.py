"""
Module for TFC/E Team Membership API endpoint.
"""
from .requestor import Requestor


class TeamMembership(Requestor):
    """
    TFC/E Team Membership methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org

        super().__init__(headers, log_level, verify)
    
    def add_user_with_user_id(self, team_id):
        """
        POST /teams/:team_id/relationships/users
        """
        print('coming soon')

    def add_user_with_org_membership(self, team_id):
        """
        POST /teams/:team_id/relationships/organization-memberships
        """
        print('coming soon')
    
    def delete_user_with_user_id(self, team_id):
        """
        DELETE /teams/:team_id/relationships/users
        """
        print('coming soon')
    
    def delete_user_with_org_membership(self, team_id):
        """
        DELETE /teams/:team_id/relationships/organization-memberships
        """
        print('coming soon')