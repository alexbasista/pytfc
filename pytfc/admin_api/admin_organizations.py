"""
TFE Admin Organizations API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminOrganizations(TfcApiBase):
    """
    TFE Admin Organizations methods.
    """    
    def list(self, query=None, filters=None, page_number=None,
             page_size=None, include=None):
        """
        GET /api/v2/admin/organizations
        """
        if query is not None:
            if 'email' not in query and 'name' not in query:
                self._logger.error("Invalid search query string."
                    " Valid values are: `email`, `name`.")
                raise ValueError
        
        # TODO:
        # Add validation for `filters` param
        # filter[module_producer]
        
        if include is not None:
            if include != 'owners':
                self._logger.error("Invalid `include` query param."
                    " Valid values are: `owners`.")
                raise ValueError

        return self._requestor.get(path='/admin/organizations', query=query,
                                   filters=filters, page_number=page_number,
                                   page_size=page_size, include=include)

    def show(self, org, include=None):
        """
        GET /api/v2/admin/organizations/:name
        """
        if include is not None:
            if include != 'owners':
                self._logger.error("Invalid `include` query param."
                    " Valid values are: `owners`.")
                raise ValueError
        
        path = f'/admin/organizations/{org}'
        return self._requestor.get(path=path, include=include)

    def update(self, org, **kwargs):
        """
        PATCH /admin/organizations/:name
        """
        print('coming soon')

    def delete(self, org):
        """
        DELETE /admin/organizations/:name
        """
        print('coming soon')

    def list_consumers(self, org, page_number=None, page_size=None):
        """
        GET /api/v2/admin/organizations/:name/relationships/module-consumers
        """
        path = f'/admin/organizations/{org}/relationships/module-consumers'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    def update_consumers(self, org):
        """
        PATCH /admin/organizations/:name/relationships/module-consumers
        """
        print('coming soon')

