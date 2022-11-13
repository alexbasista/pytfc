"""
Module for TFE Admin Terraform Versions API endpoints.
For Terraform Enterprise only.
"""
from .requestor import Requestor


class AdminTerraformVersions(Requestor):
    """
    TFE Admin Terraform Versions methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self._atv_endpoint = '/'.join([base_uri, 'admin', 'terraform-versions'])

        super().__init__(headers, log_level, verify)

    def list(self, filters=None, search=None, page_number=None, page_size=None):
        """
        GET /admin/terraform-versions
        """
        if search is not None:
            if 'version' not in search:
                self._logger.error("Invalid search query string."
                    " Valid values are: `{'version': '<#.#.#>'}`.")
                raise ValueError
        
        # TODO:
        # Add validation for `filters` param
        # filter[version]

        return self.get(url=self._atv_endpoint, filters=filters, search=search,
            page_number=page_number, page_size=page_size)
        
    def list_all(self, filters=None, search=None):
        """
        GET /admin/terraform-versions

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Terraform Versions.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        if search is not None:
            if 'version' not in search:
                self._logger.error("Invalid search query string."
                    " Valid values are: `{'version': '<#.#.#>'}`.")
                raise ValueError
        
        # TODO:
        # Add validation for `filters` param
        # filter[version]

        return self.client._requestor._list_all(url=self._atv_endpoint,
            filters=filters, search=search)
    
    def create(self, version):
        """
        POST /admin/terraform-versions
        """
    
    def show(self, tfv_id):
        """
        GET /admin/terraform-versions/:id
        """

    def update(self, tfv_id):
        """
        PATCH /admin/terraform-versions/:id
        """
    
    def delete(self, tfv_id):
        """
        DELETE /admin/terraform-versions/:id
        """