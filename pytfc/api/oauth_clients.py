"""TFC/E OAuth Clients API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import MissingOauthClient


class OauthClients(TfcApiBase):
    """
    TFC/E OAuth Clients methods.
    """
    _oc_attr_list = [
        #'service_provider', # invalid for PATCH
        'name',
        'key',
        #'http_url', # invalid for PATCH
        #'api_url', # invalid for PATCH
        #'oauth_token_string', # invalid for PATCH
        #'private_key', # invalid for PATCH
        'secret',
        'rsa_public_key'
    ]
    
    def get_oc_id(self, oc_name):
        """
        Helper method to retrieve OAuth Client ID
        based on OAuth Client (display) name passed.
        """
        oc_list = self.list()
        oc_id = [ i['id'] for i in oc_list.json()['data']\
            if i['attributes']['name'] == oc_name ]
        
        return oc_id[0]

    def list(self, page_number=None, page_size=None, include=None):
        """
        GET /organizations/:organization_name/oauth-clients
        """
        if include:
            if include != 'oauth_tokens':
                self._logger.error(f"`{include}` is invalid for 'include'."
                                   " Valid value: `oauth_tokens`.")
        path = f'/organizations/{self.org}/oauth-clients'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, include=include)

    def show(self, oc_id=None, name=None, include=None):
        """
        GET /oauth-clients/:id
        """
        if include != 'oauth_tokens':
            self._logger.error(f"`{include}` is invalid for 'include'."
                               " Valid value: `oauth_tokens`.")
        if oc_id is not None:
            oc_id = oc_id
        elif name is not None:
            oc_id = self.get_oc_id(oc_name=name)
        else:
            self._logger.error("Either `oc_id` or `name` is required.")
            raise MissingOauthClient
        
        path = f'/oauth-clients/{oc_id}'
        return self._requestor.get(path=path)

    def create(self, service_provider, name, http_url, api_url,
               oauth_token_string, private_key=None, key=None,
               secret=None, rsa_public_key=None):
        """
        POST /organizations/:organization_name/oauth-clients
        """        
        payload = {}
        data = {}
        data['type'] = 'oauth-clients'
        attributes = {}
        attributes['service-provider'] = service_provider
        attributes['key'] = key
        attributes['name'] = name
        attributes['http-url'] = http_url
        attributes['api-url'] = api_url
        attributes['oauth-token-string'] = oauth_token_string
        attributes['private-key'] = private_key # Azure DevOps Server only
        attributes['secret'] = secret # Used for BitBucket Server
        attributes['rsa-public-key'] = rsa_public_key # Required for BitBucket Server
        data['attributes'] = attributes
        payload['data'] = data
        
        path = f'/organizations/{self.org}/oauth-clients'
        return self._requestor.post(path=path, payload=payload)

    def update(self, oc_id=None, name=None, **kwargs):
        """
        PATCH /oauth-clients/:id
        """
        if oc_id is not None:
            oc_id = oc_id
        elif name is not None:
            oc_id = self.get_oc_id(oc_name=name)
        else:
            self._logger.error("Either `oc_id` or `name` is required.")
            raise MissingOauthClient

        payload = {}
        data = {}
        data['type'] = 'oauth-clients'
        data['id'] = oc_id
        attributes = {}
        if kwargs.get('new_name'):
            attributes['name'] = kwargs.get('new_name')
            kwargs.pop('new_name')
        for key, value in kwargs.items():
            if key in self._oc_attr_list:
                attributes[key] = value
            else:
                self._logger.warning(\
                    f"`{key} is an invalid key for OAuth Clients API.")
        data['attributes'] = attributes
        payload['data'] = data

        path = f'/oauth-clients/{oc_id}'
        return self._requestor.patch(path=path, payload=payload)

    def delete(self, oc_id=None, name=None):
        """
        DELETE /oauth-clients/:id
        """
        if oc_id is not None:
            oc_id = oc_id
        elif name is not None:
            oc_id = self.get_oc_id(oc_name=name)
        else:
            self._logger.error("Either `oc_id` or `name` is required.")
            raise MissingOauthClient
        
        path = f'/oauth-clients/{oc_id}'
        return self._requestor.delete(path=path)
