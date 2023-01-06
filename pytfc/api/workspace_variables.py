"""TFC/E Workspace Variables API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set
import json
import hcl as pyhcl


class WorkspaceVariables(TfcApiBase):
    """ 
    TFC/E Workspace Variables methods.
    """
    @validate_ws_id_is_set
    def create(self, key, value, description=None, category='terraform',
               hcl='false', sensitive='false', ws_id=None):
        """
        POST /workspaces/:workspace_id/vars
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        if category not in ['terraform', 'env']:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'category'.\
                                Valid arguments: 'terraform', 'env'.".format(category))
        if hcl not in ['true', 'false', True, False]:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'hcl'.\
                                Valid arguments: 'true', 'false'.".format(hcl))
        if sensitive not in ['true', 'false', True, False]:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'sensitive'.\
                                Valid arguments: 'true', 'false'.".format(sensitive))

        if isinstance(value, list):
            value = json.dumps(value)
            hcl = True

        if isinstance(value, dict):
            value = json.dumps(value)
            hcl = True

        payload = {}
        data = {}
        data['type'] = 'vars'
        attributes = {}
        attributes['key'] = key
        attributes['value'] = value
        attributes['description'] = description
        attributes['category'] = category
        attributes['hcl'] = hcl
        attributes['sensitive'] = sensitive
        data['attributes'] = attributes
        payload['data'] = data

        path = f'/workspaces/{ws_id}/vars'
        return self._requestor.post(path=path, payload=payload)

    @validate_ws_id_is_set
    def list(self, ws_id=None):
        """
        GET /workspaces/:workspace_id/vars
        """
        ws_id = ws_id if ws_id else self.ws_id

        path = f'/workspaces/{ws_id}/vars'
        return self._requestor.get(path=path)

    def update(self, var_name=None, var_id=None, ws_id=None):
        """
        PATCH /workspaces/:workspace_id/vars/:variable_id
        """
        print('coming soon')

    @validate_ws_id_is_set
    def delete(self, var_name=None, var_id=None, ws_id=None):
        """
        DELETE /workspaces/:workspace_id/vars/:variable_id
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        # TODO:
        # Add lookup for `var_name` to `var_id`
        
        path = f'/workspaces/{ws_id}/vars/{var_id}'
        return self._requestor.delete(path=path)

    @validate_ws_id_is_set
    def create_from_file(self, var_file, ws_id=None):
        """
        Method to create Workspace Variables from a terraform.tfvars
        filepath to provide an experience similar to Terraform OSS.
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        try:
            with open(var_file, 'r') as fp:
                tfvars = pyhcl.load(fp)
            for key, value in tfvars.items():
                if isinstance(value, dict):
                    value = json.dumps(value)
                    self.create(key=key, value=value, hcl=True, ws_id=ws_id)
                elif isinstance(value, list):
                    self.create(key=key, value=value, hcl=True, ws_id=ws_id)
                else:
                    self.create(key=key, value=value, hcl=False, ws_id=ws_id)
        except Exception as e:
            self._logger.error(f"Unknown exception occured: {e}")


