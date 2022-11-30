"""TFC/E SSH Keys API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class SSHKeys(TfcApiBase):
    """
    TFC/E SSH Keys methods.
    """
    def list(self, page_number=None, page_size=None):
        """
        GET /organizations/:organization_name/ssh-keys
        """             
        path = f'/organizations/{self.org}/ssh-keys'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    def show(self, id):
        """
        GET /ssh-keys/:ssh_key_id
        """
        path = f'/ssh-keys/{id}'
        return self._requestor.get(path=path)

    def create(self, name, value):
        """
        POST /organizations/:organization_name/ssh-keys
        """
        print('coming soon')

    def update(self, id):
        """
        PATCH /ssh-keys/:ssh_key_id
        """
        print('coming soon')

    def delete(self, id):
        """
        DELETE /ssh-keys/:ssh_key_id
        """
        path = f'/ssh-keys/{id}'
        return self._requestor.delete(path=path)