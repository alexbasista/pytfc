"""
Module for TFC/E SSH Keys API endpoint.
"""


class SSHKeys:
    """
    TFC/E SSH Keys methods.
    """
    def __init__(self, client):
        self.client = client

    def list(self, page_number=None, page_size=None):
        """
        GET /organizations/:organization_name/ssh-keys
        """             
        base_url = '/'.join([self.client._base_uri_v2, 'organizations',
            self.client.org, 'ssh-keys'])

        return self.client._requestor.get(url=base_url,
            page_number=page_number, page_size=page_size)

    def show(self, id):
        """
        GET /ssh-keys/:ssh_key_id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'ssh-keys', id]))

    def create(self, name, value):
        """
        POST /organizations/:organization_name/ssh-keys
        """
        print('coming soon')

    def update(self, name):
        """
        PATCH /ssh-keys/:ssh_key_id
        """
        print('coming soon')

    def delete(self, name):
        """
        DELETE /ssh-keys/:ssh_key_id
        """
        print('coming soon')