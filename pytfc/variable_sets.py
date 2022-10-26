"""
Module for TFC/E Variable Sets API endpoints.
"""
from .exceptions import MissingWorkspace


class VariableSets:
    """
    TFC/E Variable Sets methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._base_api_url = self.client._base_uri_v2

        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None
    
    def create(self, name, description=None, is_global=False, workspaces=None,
                vars=None):
        """
        POST organizations/:organization_name/varsets
        """
        print('coming soon')
    
    def update(self, varset_id):
        """
        PUT/PATCH varsets/:varset_id
        """
        print('coming soon')

    def delete(self, varset_id):
        """
        DELETE varsets/:varset_id
        """
        return self.client._requestor.delete(url='/'.join([self._base_api_url,
            'varsets', varset_id]))
    
    def show(self, varset_id, include=None):
        """
        GET varsets/:varset_id
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'varsets', varset_id]), include=include)
    
    def list(self, page_number=None, page_size=None, include=None):
        """
        GET organizations/:organization_name/varsets
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'organizations', self.client.org, 'varsets']),
            page_number=page_number, page_size=page_size, include=include)

    def add_variable(self, varset_id, **kwargs):
        """
        POST varsets/:varset_external_id/relationships/vars
        """
        print('coming soon')
    
    def update_variable(self, varset_id, var_id, **kwargs):
        """
        PATCH varsets/:varset_id/relationships/vars/:var_id
        """
        print('coming soon')

    def delete_variable(self, varset_id, var_id):
        """
        DELETE varsets/:varset_id/relationships/vars/:var_id
        """
        print('coming soon')

    def list_variables(self, varset_id, include=None):
        """
        GET varsets/:varset_id/relationships/vars
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'varsets', varset_id, 'relationships', 'vars']), include=include)

    def apply_to_workspace(self, varset_id, ws_id=None):
        """
        POST varsets/:varset_id/relationships/workspaces
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace
        
        print('coming soon')

    def remove_from_workspace(self, varset_id, ws_id=None):
        """
        DELETE varsets/:varset_id/relationships/workspaces
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace
        
        print('coming soon')