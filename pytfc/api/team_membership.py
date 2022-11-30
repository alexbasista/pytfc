"""TFC/E Team Membership API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class TeamMembership(TfcApiBase):
    """
    TFC/E Team Membership methods.
    """
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