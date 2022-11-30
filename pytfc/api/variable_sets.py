"""TFC/E Variable Sets API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class VariableSets(TfcApiBase):
    """
    TFC/E Variable Sets methods.
    """
    def create(self, name, description=None, is_global=False, workspaces=None,
               vars=None):
        """
        POST /organizations/:organization_name/varsets
        """
        print('coming soon')
    
    def update(self, varset_id):
        """
        PUT/PATCH /varsets/:varset_id
        """
        print('coming soon')

    def delete(self, varset_id):
        """
        DELETE /varsets/:varset_id
        """
        path = f'/varsets/{varset_id}'
        return self._requestor.delete(path=path)
    
    def show(self, varset_id, include=None):
        """
        GET /varsets/:varset_id
        """
        path = f'/varsets/{varset_id}'
        return self._requestor.get(path=path, include=include)
    
    def list(self, page_number=None, page_size=None, include=None):
        """
        GET /organizations/:organization_name/varsets
        """
        path = f'/organizations/{self.org}/varsets'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, include=include)

    def add_variable(self, varset_id, **kwargs):
        """
        POST /varsets/:varset_external_id/relationships/vars
        """
        print('coming soon')
    
    def update_variable(self, varset_id, var_id, **kwargs):
        """
        PATCH /varsets/:varset_id/relationships/vars/:var_id
        """
        print('coming soon')

    def delete_variable(self, varset_id, var_id):
        """
        DELETE /varsets/:varset_id/relationships/vars/:var_id
        """
        print('coming soon')

    def list_variables(self, varset_id, include=None):
        """
        GET /varsets/:varset_id/relationships/vars
        """
        path = f'/varsets{varset_id}/relationships/vars'
        return self._requestor.get(path=path, include=include)

    @validate_ws_id_is_set
    def apply_to_workspace(self, varset_id, ws_id=None):
        """
        POST /varsets/:varset_id/relationships/workspaces
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')

    @validate_ws_id_is_set
    def remove_from_workspace(self, varset_id, ws_id=None):
        """
        DELETE /varsets/:varset_id/relationships/workspaces
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')