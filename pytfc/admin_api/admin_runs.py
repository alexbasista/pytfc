"""
TFE Admin Runs API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminRuns(TfcApiBase):
    """
    TFE Admin Runs methods.
    """   
    def list(self, query=None, filters=None, page_number=None, page_size=None,
             include=None):
        """
        GET /api/v2/admin/runs
        """
        return self._requestor.get(path='/admin/runs', query=query,
                                   filters=filters, page_number=page_number,
                                   page_size=page_size, include=include)

    def list_all(self, query=None, filters=None, include=None):
        """
        GET /api/v2/admin/runs

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 Admin Runs.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        return self._requestor.list_all(path='/admin/runs', query=query,
                                        filters=filters, include=include)
    
    def force_cancel(self, run_id, comment=None):
        """
        POST /admin/runs/:id/actions/force-cancel
        """
        payload = {'comment': comment}
        path = f'/admin/runs/{run_id}/actions/force-cancel'
        return self._requestor.post(path=path, payload=payload)