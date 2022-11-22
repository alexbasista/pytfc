"""
Module for TFC/E Registry Modules API endpoint.
"""


class RegistryModules:
    """
    TFC/E Registry Modules methods.
    """
    def __init__(self, client):
        self.client = client

        self._rm_endpoint = '/'.join([self.client._base_uri_v2,
            'organizations', self.client.org, 'registry-modules'])

    def list(self, page_number=None, page_size=None, filters=None):
        """
        GET /organizations/:organization_name/registry-module
        """             
        return self.client._requestor.get(url=self._rm_endpoint,
            page_number=page_number, page_size=page_size, filters=filters)

    def list_all(self, filters=None):
        """
        GET /organizations/:organization_name/registry-module

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Registry Modules.

        Returns object (dict) with two arrays: `data` and `included`.
        """             
        return self.client._requestor._list_all(url=self._rm_endpoint,
            filters=filters)

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
        url = '/'.join([
            self._rm_endpoint,
            registry_name,
            namespace,
            name,
            provider
        ])

        return self.client._requestor.get(url=url)

    def delete(self, name, namespace, provider, registry_name='private', version=None):
        """
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider
        DELETE /organizations/:organization_name/registry-modules/:registry_name/:namespace/:name/:provider/:version
        """
        print('coming soon')