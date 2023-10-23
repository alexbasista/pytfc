"""TFC/E State Version Outputs API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class StateVersionOutputs(TfcApiBase):
    """
    TFC/E State Version Outputs methods.
    """
    def list(self, sv_id, page_number=None, page_size=None):
        """
        GET /state-versions/:state_version_id/outputs
        """
        path = f'/state-versions/{sv_id}/outputs'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    def list_all(self, sv_id):
        """
        GET /state-versions/:state_version_id/outputs

        Built-in logic to enumerate all pages in list response for
        cases where there are more than 100 State Versions.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        path = f'/state-versions/{sv_id}/outputs'
        return self._requestor.list_all(path=path)

    def show(self, svo_id, include=None):
        """
        GET /state-version-outputs/:state_version_output_id

        Optional: `include=outputs` for full details.
        """
        path = f'/state-version-outputs/{svo_id}'
        return self._requestor.get(path=path, include=include)

    def show_current_for_ws(self, ws_id):
        """
        GET /workspaces/:workspace_id/current-state-version-outputs
        """
        path = f'/workspaces/{ws_id}/current-state-version-outputs'
        return self._requestor.get(path=path)