"""TFC/E OAuth Tokens API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class OauthTokens(TfcApiBase):
    """
    TFC/E OAuth Tokens methods.
    """
    def list(self, oc_id, page_number=None, page_size=None):
        """
        GET /oauth-clients/:oauth_client_id/oauth-tokens
        """
        path = f'/oauth-clients/{oc_id}/oauth-tokens'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    def show(self, ot_id):
        """
        GET /oauth-tokens/:id
        """
        path = f'/oauth-tokens/{ot_id}'
        return self._requestor.get(path=path)

    def update(self, ot_id, ssh_key=None):
        """
        PATCH /oauth-tokens/:id
        """
        payload = {}
        data = {}
        data['type'] = 'oauth-tokens'
        data['id'] = ot_id
        attributes = {}
        if ssh_key: attributes['ssh-key'] = ssh_key
        data['attributes'] = attributes
        payload['data'] = data
        
        path = f'/oauth-tokens/{ot_id}'
        return self._requestor.patch(path=path, payload=payload)

    def delete(self, ot_id):
        """
        DELETE /oauth-tokens/:id
        """
        path = f'/oauth-tokens/{ot_id}'
        return self._requestor.delete(path=path)
