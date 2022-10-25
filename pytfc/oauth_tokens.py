"""
Module for TFC/E OAuth Tokens API endpoint.
"""
from .oauth_clients import OauthClients


class OauthTokens:
    """
    TFC/E OAuth Tokens methods.
    """
    def __init__(self, client):
        self.client = client
        self.oauth_tokens_endpoint = '/'.join([
            self.client._base_uri_v2, 'oauth-tokens'])
        
        self.oauth_clients = OauthClients(client=self.client)

    def list(self, oauth_client_name):
        """
        GET /oauth-clients/:oauth_client_id/oauth-tokens
        
        Must be listed within the confines of a specific OAuth Client.
        """
        oc_id = self.oauth_clients._get_oc_id(name=oauth_client_name)
        
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'oauth-clients', oc_id, 'oauth-tokens']))

    def show(self, oauth_token_id):
        """
        GET /oauth-tokens/:id
        """
        return self.client._requestor.get(url='/'.join([
            self.oauth_tokens_endpoint, oauth_token_id]))

    def update(self, oauth_token_id, **kwargs):
        """
        PATCH /oauth-tokens/:id
        """
        payload = {}
        data = {}
        data['type'] = 'oauth-tokens'
        data['id'] = oauth_token_id
        attributes = {}
        if kwargs.get('ssh_key'):
            attributes['ssh-key'] = kwargs.get('ssh_key')
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.patch(url='/'.join([
            self.oauth_tokens_endpoint, oauth_token_id]),
            payload=payload)

    def delete(self, oauth_token_id):
        """
        DELETE /oauth-tokens/:id

        Equivalent to revoking connection from TFC/E Org to VCS Provider.
        """
        return self.client._requestor.delete(url='/'.join([
            self.oauth_tokens_endpoint, oauth_token_id]))
