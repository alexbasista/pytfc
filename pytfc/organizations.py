"""
Module for TFC/E Organization API endpoint.
"""
from .exceptions import MissingOrganization


class Organizations:
    """
    TFC/E Organizations methods.
    """
    _org_attributes_list = [
        'name',
        'email',
        'session_timeout',
        'session_remember',
        'collaborator_auth_policy',
        'cost_estimation_enabled',
        'owners_team_saml_role_id'
    ]
    
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self.organizations_endpoint = '/'.join([
            self.client._base_uri_v2, 'organizations'])

    def list(self):
        """
        GET /organizations
        """
        return self.client._requestor.get(url=self.organizations_endpoint)

    def show(self, name=None):
        """
        GET /organizations/:organization_name
        """
        if name is None:
            if self.client.org:
                name = self.client.org
            else:
              raise MissingOrganization
        
        return self.client._requestor.get(url='/'.join([
            self.organizations_endpoint, name]))

    def create(self, name, email, **kwargs):
        """
        POST /organizations
        """
        payload = {}
        data = {}
        data['type'] = 'organizations'
        attributes = {}
        attributes['name'] = name
        attributes['email'] = email
        for key, value in kwargs.items():
            if key in self._org_attributes_list:
                attributes[key] = value
            else:
                self._logger.warning(f"`{key}` is an invalid key for Organizations API.")
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.post(url=self.organizations_endpoint,
            payload=payload)

    def update(self, name=None, **kwargs):
        """
        PATCH /organizations/:organization_name
        """
        if name is None:
            if self.client.org:
                name = self.client.org
            else:
              raise MissingOrganization
        
        payload = {}
        data = {}
        data['type'] = 'organizations'
        attributes = {}
        attributes['name'] = name
        for key, value in kwargs.items():
            if key in self.org_attributes_list:
                attributes[key] = value
            else:
                self._logger.warning(f"`{key}` is an invalid key for Organizations API.")
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.patch(url='/'.join([
            self.organizations_endpoint, name]), payload=payload)

    def delete(self, name):
        """
        DELETE /organizations/:organization_name
        """
        return self.client._requestor.delete(url='/'.join([
            self.organizations_endpoint, name]))

    def show_entitlement_set(self, name=None):
        """
        GET /organizations/:organization_name/entitlement-set
        """
        if name is None:
            if self.client.org:
                name = self.client.org
            else:
              raise MissingOrganization
        
        return self.client._requestor.get(url='/'.join([
            self.organizations_endpoint, name, 'entitlement-set']))
