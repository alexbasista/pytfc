"""
Module for TFE Admin Organizations API endpoints.
For Terraform Enterprise only.
"""
from .requestor import Requestor


class AdminOrganizations(Requestor):
    """
    TFE Admin Organizations methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self.ao_endpoint = '/'.join([base_uri, 'admin', 'organizations'])

        super().__init__(headers, log_level, verify)
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
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

        return self.get(url=self.ao_endpoint, query=query, filters=filters,
            page_number=page_number, page_size=page_size, include=include)

    def show(self, org, include=None):
        """
        GET /api/v2/admin/organizations/:name
        """
        if include is not None:
            if include != 'owners':
                self._logger.error("Invalid `include` query param."
                    " Valid values are: `owners`.")
                raise ValueError
        
        return self.get(url='/'.join([self.ao_endpoint, org]), include=include)

    def update(self, org, **kwargs):
        """
        PATCH /admin/organizations/:name
        """

    def delete(self, org):
        """
        DELETE /admin/organizations/:name
        """
    
    def list_consumers(self, org, page_number=None, page_size=None):
        """
        GET /api/v2/admin/organizations/:name/relationships/module-consumers
        """
        return self.get(url='/'.join([self.ao_endpoint, org, 'relationships',
            'module-consumers']), page_number=page_number, page_size=page_size)

    def update_consumers(self, org):
        """
        PATCH /admin/organizations/:name/relationships/module-consumers
        """

