"""
Module for TFC/E OAuth Clients endpoint.
"""
from .exceptions import MissingOrganization


class OauthClients(object):
    """
    TFC/E OAuth Clients methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self.oauth_clients_endpoint = '/'.join([self.client._base_uri_v2, 'organizations', self.client.org, 'oauth-clients'])

    def _get_oc_id(self, name):
        """
        Helper method to retrieve the OAuth Client ID of an OAuth Client based on OAuth Client display name
        """
        oc_list = self.list()
        oc_id = [ i['id'] for i in oc_list.json()['data'] if i['attributes']['name'] == name ]
        return oc_id[0]

    def list(self):
        """
        GET /organizations/:organization_name/oauth-clients
        """
        if self.client.org is None:
            raise MissingOrganization

        return self.client._requestor.get(url='/'.join([self.oauth_clients_endpoint]))

    def show(self, name):
        """
        GET /oauth-clients/:id
        """
        oc_id = self._get_oc_id(name=name)
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2, 'oauth-clients', oc_id]))

    def create(self, service_provider, name, http_url, api_url, oauth_token_string, **kwargs):
        """
        POST /organizations/:organization_name/oauth-clients
        """
        if self.client.org is None:
            raise MissingOrganization
        
        payload = {}
        data = {}
        data['type'] = 'oauth-clients'
        attributes = {}
        attributes['service-provider'] = service_provider
        attributes['name'] = name
        attributes['http-url'] = http_url
        attributes['api-url'] = api_url
        attributes['oauth-token-string'] = oauth_token_string
        if kwargs.get('private_key'):
            attributes['private-key'] = kwargs.get('private_key')
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.post(url='/'.join([self.oauth_clients_endpoint]), payload=payload)


    def update(self, name, **kwargs):
        """
        PATCH /oauth-clients/:id
        """
        oc_id = self._get_oc_id(name=name)

        payload = {}
        data = {}
        data['type'] = 'oauth-clients'
        data['id'] = oc_id
        attributes = {}
        if kwargs.get('new_name'):
            attributes['name'] = kwargs.get('new_name')
        if kwargs.get('key'):
            attributes['key'] = kwargs.get('key')
        if kwargs.get('secret'):
            attributes['secret'] = kwargs.get('secret')
        data['attributes'] = attributes
        payload['data'] = data

        return self.client._requestor.patch(url='/'.join([self.oauth_clients_endpoint]), payload=payload)

    def delete(self, name):
        """
        DELETE /oauth-clients/:id
        """
        oc_id = self._get_oc_id(name=name)
        return self.client._requestor.delete(url='/'.join([self.client._base_uri_v2, 'oauth-clients', oc_id]))
