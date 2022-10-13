"""
Module for TFC/E Workspace Variables endpoint.
"""
import json
import hcl as pyhcl
from .exceptions import MissingWorkspace


class WorkspaceVariables(object):
    """ 
    TFC/E Workspace Variables methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self._ws_id = self.client.workspaces._get_ws_id(name=self.ws)
        else:
            if self.client.ws:
                self.ws = self.client.ws
                self._ws_id = self.client._ws_id
            else:
                raise MissingWorkspace

        self._workspace_variables_endpoint = '/'.join([self.client._base_uri_v2, 'workspaces',
                                                        self._ws_id, 'vars'])

    def create(self, key, value, description=None, category='terraform', hcl='false', sensitive='false'):
        """
        POST /workspaces/:workspace_id/vars
        """
        if category not in ['terraform', 'env']:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'category'.\
                                Valid arguments: 'terraform', 'env'.".format(category))
        if hcl not in ['true', 'false', True, False]:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'hcl'.\
                                Valid arguments: 'true', 'false'.".format(hcl))
        if sensitive not in ['true', 'false', True, False]:
            raise ValueError("[ERROR] '{}' is an invalid argument for 'sensitive'. \
                                Valid arguments: 'true', 'false'.".format(sensitive))

        if isinstance(value, list):
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
        
        return self.client._requestor.post(url=self._workspace_variables_endpoint, payload=payload)

    def create_from_file(self, var_file):
        """
        Method to create Workspace Variables from a terraform.tfvars
        filepath to provide an experience similar to Terraform OSS.
        """
        try:
            with open(var_file, 'r') as fp:
                tfvars = pyhcl.load(fp)
            for key, value in tfvars.items():
                if isinstance(value, dict):
                    value = json.dumps(value).replace(':', ' =')
                    self.create(key=key, value=value, hcl=True)
                elif isinstance(value, list):
                    self.create(key=key, value=value, hcl=True)
                else:
                    self.create(key=key, value=value, hcl=False)
        except Exception as e:
            self._logger.error(f"Unknown exception occured: {e}")


