"""
Module for TFE Admin Runs API endpoints.
For Terraform Enterprise only.
"""
from .requestor import Requestor


class AdminRuns(Requestor):
    """
    TFE Admin Runs methods.
    """
    def __init__(self, headers, base_uri, org, log_level, verify):
        self.org = org
        self._ar_endpoint = '/'.join([base_uri, 'admin', 'runs'])

        super().__init__(headers, log_level, verify)
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
        """
        GET /api/v2/admin/runs
        """
        return self.get(url=self._ar_endpoint, query=query, filters=filters,
            page_number=page_number, page_size=page_size, include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/runs

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Admin Runs.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self._list_all(url=self._ar_endpoint, query=query,
            filters=filters, include=include)
    
    def force_cancel(self, run_id, comment=None):
        """
        POST /admin/runs/:id/actions/force-cancel
        """
        payload = {'comment': comment}

        return self.post(url='/'.join([self._ar_endpoint, run_id, 'actions',
            'force-cancel']), payload=payload)