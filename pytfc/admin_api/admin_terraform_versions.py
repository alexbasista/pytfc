"""
TFE Admin Terraform Versions API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminTerraformVersions(TfcApiBase):
    """
    TFE Admin Terraform Versions methods.
    """
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

        return self._requestor.get(path='/admin/terraform-versions',
                                   filters=filters, search=search,
                                   page_number=page_number,
                                   page_size=page_size)
            
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

        return self._requestor.list_all(path='/admin/terraform-versions',
                                        filters=filters, search=search)
    
    def create(self, version):
        """
        POST /admin/terraform-versions
        """
        print('coming soon')

    def show(self, tfv_id):
        """
        GET /admin/terraform-versions/:id
        """
        print('coming soon')

    def update(self, tfv_id):
        """
        PATCH /admin/terraform-versions/:id
        """
        print('coming soon')

    def delete(self, tfv_id):
        """
        DELETE /admin/terraform-versions/:id
        """
        print('coming soon')