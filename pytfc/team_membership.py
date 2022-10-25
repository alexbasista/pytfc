"""
Module for TFC/E Team Membership API endpoint.
"""


class TeamMembership:
    """
    TFC/E Team Membership methods.
    """
    def __init__(self, client):
        self.client = client
    
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