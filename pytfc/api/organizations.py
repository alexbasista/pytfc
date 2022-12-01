"""TFC/E Organization API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class Organizations(TfcApiBase):
    """
    TFC/E Organizations methods.
    """
    _org_attr_list = [
        'name',
        'email',
        'session_timeout',
        'session_remember',
        'collaborator_auth_policy',
        'cost_estimation_enabled',
        'owners_team_saml_role_id'
    ]

    def list(self):
        """
        GET /organizations
        """
        return self._requestor.get(path='/organizations')

    def show(self, name):
        """
        GET /organizations/:organization_name
        """
        path = f'/organizations/{name}'
        return self._requestor.get(path=path)

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
            if key in self._org_attr_list:
                attributes[key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Organizations API.")
        data['attributes'] = attributes
        payload['data'] = data
        
        return self._requestor.post(path='/organizations', payload=payload)

    def update(self, name, **kwargs):
        """
        PATCH /organizations/:organization_name
        """
        payload = {}
        data = {}
        data['type'] = 'organizations'
        attributes = {}
        if kwargs.get('new_name'):
            attributes['name'] = kwargs.get('new_name')
            kwargs.pop('new_name')
        #attributes['name'] = name
        for key, value in kwargs.items():
            if key in self._org_attr_list:
                attributes[key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Organizations API.")
        data['attributes'] = attributes
        payload['data'] = data
        
        path = f'/organizations/{name}'
        return self._requestor.patch(path=path, payload=payload)

    def delete(self, name):
        """
        DELETE /organizations/:organization_name
        """
        path = f'/organizations/{name}'
        return self._requestor.delete(path=path)

    def show_entitlement_set(self, name):
        """
        GET /organizations/:organization_name/entitlement-set
        """
        path = f'/organizations/{name}/entitlement-set'
        return self._requestor.get(path=path)
