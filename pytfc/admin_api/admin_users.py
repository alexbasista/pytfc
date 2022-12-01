"""
TFE Admin Users API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminUsers(TfcApiBase):
    """
    TFE Admin Users methods.
    """   
    def list(self, query=None, filters=None, page_number=None,
             page_size=None, include=None):
        """
        GET /api/v2/admin/users
        """
        return self._requestor.get(path='/admin/users', query=query,
                                   filters=filters, page_number=page_number,
                                   page_size=page_size, include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/users
        """
        return self._requestor.list_all(path='/admin/users', query=query,
                                        filters=filters, include=include)
        
    def delete(self, user_id):
        """
        DELETE /admin/users/:id
        """
        print('coming soon')

    def suspend(self, user_id):
        """
        POST /admin/users/:id/actions/suspend
        """
        print('coming soon')

    def reactivate(self, user_id):
        """
        POST /admin/users/:id/actions/unsuspend
        """
        print('coming soon')

    def grant_admin(self, user_id):
        """
        POST /admin/users/:id/actions/grant_admin
        """
        print('coming soon')

    def revoke_admin(self, user_id):
        """
        POST /admin/users/:id/actions/revoke_admin
        """
        print('coming soon')

    def disable_two_factory(self, user_id):
        """
        POST /admin/users/:id/actions/disable_two_factor
        """
        print('coming soon')

    def impersonate(self, user_id):
        """
        POST /admin/users/:id/actions/impersonate
        """
        print('coming soon')

    def unimpersonate(self, user_id):
        """
        POST /admin/users/actions/unimpersonate
        """
        print('coming soon')