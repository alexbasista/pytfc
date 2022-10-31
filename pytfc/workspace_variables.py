"""
Module for TFC/E Workspace Variables API  endpoint.
"""
import json
import hcl as pyhcl
from .exceptions import MissingWorkspace


class WorkspaceVariables:
    """ 
    TFC/E Workspace Variables methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None

    def create(self, key, value, description=None, category='terraform',
        hcl='false', sensitive='false', ws_id=None):
        """
        POST /workspaces/:workspace_id/vars
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
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

        return self.client._requestor.post(url = '/'.join([
            self.client._base_uri_v2, 'workspaces', ws_id, 'vars']),
            payload=payload)

    def list(self, ws_id=None):
        """
        GET /workspaces/:workspace_id/vars
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url = '/'.join([
            self.client._base_uri_v2, 'workspaces', ws_id, 'vars']))
    
    def list_all(self, ws_id=None):
        """
        GET /workspaces/:workspace_id/vars

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Workspace Variables.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        return self.client._requestor._list_all(url='/'.join([
            self.client._base_uri_v2, 'workspaces', ws_id, 'vars']))

    def update(self, var_name=None, var_id=None, ws_id=None):
        """
        PATCH /workspaces/:workspace_id/vars/:variable_id
        """
        print('coming soon')

    def delete(self, var_name=None, var_id=None, ws_id=None):
        """
        DELETE /workspaces/:workspace_id/vars/:variable_id
        """
        print('coming soon')

    def create_from_file(self, var_file, ws_id=None):
        """
        Method to create Workspace Variables from a terraform.tfvars
        filepath to provide an experience similar to Terraform OSS.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
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


