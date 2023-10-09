"""TFC/E Variable Sets API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class VariableSets(TfcApiBase):
    """
    TFC/E Variable Sets methods.
    """
    def get_varset_id(self, name):
        """
        Helper method that returns Variable
        Set ID based on Variable Set name.
        """
        varsets_list = self.list()
        varset_id = [ i['id'] for i in varsets_list.json()['data']\
                       if i['attributes']['name'] == name ]
        
        return varset_id[0]
    
    def create(self, name, description=None, is_global=False, workspace_ids=[],
               vars=[]):
        """
        POST /organizations/:organization_name/varsets
        """
        workspaces_data = \
        {
            "data": [
                {
                    "id": ws_id, 
                    "type": "workspaces"
                }
                for ws_id in workspace_ids
            ]
        }

        vars_data = \
        {
            "data" : [
                {
                    "type": "vars",
                    "attributes": {
                        "key": var.get('key', ''),
                        "value": var.get('value', ''),
                        "category": var.get('category', 'terraform'),
                        "sensitive": var.get('sensitive', False)
                    }
                }
                for var in vars
            ]
        }
        
        payload = \
        {
            "data": {
                "type": "varsets",
                "attributes": {
                    "name": name,
                    "description": description,
                    "global": is_global
                },
                "relationships": {
                    "workspaces": workspaces_data,
                    "vars": vars_data
                }
            }
        }

        path = f'/organizations/{self.org}/varsets'
        return self._requestor.post(path=path, payload=payload)
    
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

        payload = \
        {
            "data": [
                {
                    "type": "workspaces",
                    "id": ws_id
                }
            ]
        }

        path = f'/varsets/{varset_id}/relationships/workspaces'
        return self._requestor.post(path=path, payload=payload)

    @validate_ws_id_is_set
    def remove_from_workspace(self, varset_id, ws_id=None):
        """
        DELETE /varsets/:varset_id/relationships/workspaces
        """
        ws_id = ws_id if ws_id else self.ws_id

        payload = \
        {
            "data": [
                {
                    "type": "workspaces",
                    "id": ws_id
                }
            ]
        }

        path = f'/varsets/{varset_id}/relationships/workspaces'
        return self._requestor.delete(path=path, payload=payload)

    def apply_to_project(self, varset_id, project_ids=[]):
        """
        POST /varsets/:varset_id/relationships/projects
        """
        payload = \
        {
            "data": [
                {
                    "type": "projects", 
                    "id": prj_id
                }
                for prj_id in project_ids
            ]
        }

        path = f'/varsets/{varset_id}/relationships/projects'
        return self._requestor.post(path=path, payload=payload)
    
    def remove_from_project(self, varset_id, project_ids=[]):
        """
        DELETE /varsets/:varset_id/relationships/projects
        """
        payload = \
        {
            "data": [
                {
                    "type": "projects", 
                    "id": prj_id
                }
                for prj_id in project_ids
            ]
        }

        path = f'/varsets/{varset_id}/relationships/projects'
        return self._requestor.delete(path=path, payload=payload)