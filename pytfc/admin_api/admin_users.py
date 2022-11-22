"""
Module for TFE Admin Users API endpoints.
For Terraform Enterprise only.
"""


class AdminUsers:
    """
    TFE Admin Users methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._au_endpoint = '/'.join([self.client._base_uri_v2, 'admin',
            'users'])
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
        """
        GET /api/v2/admin/users
        """
        return self.client._requestor.get(url=self._au_endpoint, query=query,
            filters=filters, page_number=page_number, page_size=page_size,
            include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/users
        """
        return self.client._requestor._list_all(url=self._au_endpoint,
            query=query, filters=filters, include=include)
        
    def delete(self, user_id):
        """
        DELETE /admin/users/:id
        """
    
    def suspend(self, user_id):
        """
        POST /admin/users/:id/actions/suspend
        """
    
    def reactivate(self, user_id):
        """
        POST /admin/users/:id/actions/unsuspend
        """
    
    def grant_admin(self, user_id):
        """
        POST /admin/users/:id/actions/grant_admin
        """
    
    def revoke_admin(self, user_id):
        """
        POST /admin/users/:id/actions/revoke_admin
        """
    
    def disable_two_factory(self, user_id):
        """
        POST /admin/users/:id/actions/disable_two_factor
        """
    
    def impersonate(self, user_id):
        """
        POST /admin/users/:id/actions/impersonate
        """

    def unimpersonate(self, user_id):
        """
        POST /admin/users/actions/unimpersonate
        """
