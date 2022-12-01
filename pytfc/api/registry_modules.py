"""TFC/E Registry Modules API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class RegistryModules(TfcApiBase):
    """
    TFC/E Registry Modules methods.
    """
    def list(self, page_number=None, page_size=None, filters=None):
        """
        GET /organizations/:organization_name/registry-module
        """             
        path = f'/organizations/{self.org}/registry-modules'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, filters=filters)

    def list_all(self, filters=None):
        """
        GET /organizations/:organization_name/registry-module

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Registry Modules.

        Returns object (dict) with two arrays: `data` and `included`.
        """             
        path = f'/organizations/{self.org}/registry-modules'
        return self._requestor.list_all(path=path, filters=filters)

    def publish_from_vcs(self):
        """
        POST /organizations/:organization_name/registry-modules/vcs
        """
        print('coming soon')

    def create(self):
        """
        POST /organizations/:organization_name/registry-modules
        """
        print('coming soon')

    def create_version(self):
        """
        POST /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/versions
        """
        print('coming soon')

    def add_version(self):
        """
        PUT https://archivist.terraform.io/v1/object/<UNIQUE OBJECT ID>
        """
        print('coming soon')
    
    def show(self, name, namespace, provider, registry_name='private'):
        """
        GET /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider
        """
        path = '/'.join([
            '/organizations',
            self.org,
            'registry-modules',
            registry_name,
            namespace,
            name,
            provider
        ])
        return self._requestor.get(path=path)

    def delete(self, name, namespace, provider,
               registry_name='private', version=None):
        """
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/:version
        """
        print('coming soon')