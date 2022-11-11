"""
Module for TFE Admin Runs API endpoints.
For Terraform Enterprise only.
"""


class AdminRuns:
    """
    TFE Admin Runs methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._ar_endpoint = '/'.join([self.client._base_uri_v2, 'admin',
            'runs'])
    
    def list(self, query=None, filters=None, page_number=None, page_size=None,
        include=None):
        """
        GET /api/v2/admin/runs
        """
        return self.client._requestor.get(url=self._ar_endpoint, query=query,
            filters=filters, page_number=page_number, page_size=page_size,
            include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/runs

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Admin Runs.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self.client._requestor._list_all(url=self._ar_endpoint,
            query=query, filters=filters, include=include)
    
    def force_cancel(self, run_id, comment=None):
        """
        POST /admin/runs/:id/actions/force-cancel
        """
        payload = {'comment': comment}

        return self.client._requestor.post(url='/'.join([self._ar_endpoint,
            run_id, 'actions', 'force-cancel']), payload=payload)