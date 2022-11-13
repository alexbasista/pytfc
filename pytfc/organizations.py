"""
Module for TFC/E Organization API endpoints.
"""
from .exceptions import MissingOrganization
from .requestor import Requestor


class Organizations(Requestor):
    """
    TFC/E Organizations methods.
    """
    _valid_org_attributes = [
        'name',
        'email',
        'session_timeout',
        'session_remember',
        'collaborator_auth_policy',
        'cost_estimation_enabled',
        'owners_team_saml_role_id'
    ]
    
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self.orgs_endpoint = '/'.join([base_uri, 'organizations'])
        
        super().__init__(headers, log_level, verify)

    def list(self, query=None, page_number=None, page_size=None, include=None):
        """
        GET /organizations
        """
        return self.get(url=self.orgs_endpoint, query=query,
            page_number=page_number, page_size=page_size, include=include)

    def list_all(self, query=None, include=None):
        """
        GET /organizations

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Organizations.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self._list_all(url=self.orgs_endpoint, query=query,
            include=include)

    def show(self, name=None):
        """
        GET /organizations/:organization_name
        """
        if name is None:
            if self.org:
                name = self.org
            else:
              raise MissingOrganization
        
        return self.get(url='/'.join([self.orgs_endpoint, name]))

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
            if key in self._valid_org_attributes:
                attributes[key] = value
            else:
                self._logger.warning(f"`{key}` is an invalid key for"
                    " Organizations API. Skipping over this key.")
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.post(url=self.orgs_endpoint, payload=payload)

    def update(self, name=None, **kwargs):
        """
        PATCH /organizations/:organization_name
        """
        if name is None:
            if self.org:
                name = self.org
            else:
              raise MissingOrganization
        
        payload = {}
        data = {}
        data['type'] = 'organizations'
        attributes = {}
        attributes['name'] = name
        for key, value in kwargs.items():
            if key in self._valid_org_attributes:
                attributes[key] = value
            else:
                self._logger.warning(f"`{key}` is an invalid key for"
                " Organizations API. Skipping over this key.")
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.patch(url='/'.join([self.orgs_endpoint, name]),
            payload=payload)

    def delete(self, name):
        """
        DELETE /organizations/:organization_name
        """
        return self.delete(url='/'.join([self.orgs_endpoint, name]))

    def show_entitlement_set(self, name=None):
        """
        GET /organizations/:organization_name/entitlement-set
        """
        if name is None:
            if self.client.org:
                name = self.client.org
            else:
              raise MissingOrganization
        
        return self.get(url='/'.join([self.orgs_endpoint, name,
            'entitlement-set']))
