"""TFC/E Audit Trails API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class AuditTrails(TfcApiBase):
    """
    TFC/E Audit Trails methods.
    """
    def list(self, since=None, page_number=None, page_size=None):
        """
        GET /organization/audit-trail
        """
        path = '/organization/audit-trail'
        return self._requestor.get(path=path, since=since,
                                   page_number=page_number,
                                   page_size=page_size)

    def list_all(self, since=None):
        """
        GET /organization/audit-trail

        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 audit events.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        path = '/organization/audit-trail'
        return self._requestor.list_all(path=path, since=since)