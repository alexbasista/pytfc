"""TFC/E Run Triggers API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class RunTriggers(TfcApiBase):
    """
    TFC/E Run Triggers methods.
    """
    @validate_ws_id_is_set
    def create(self, source_ws_obj, ws_id=None):
        """
        POST /workspaces/:workspace_id/run-triggers

        :param source_ws_obj: Source Workspace for Run Trigger.
        :type source_ws_obj: Object with `id` and `type` properties. For example:
            { "id": "ws-abcdefghijklmnop", "type": "workspaces" }
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')

    @validate_ws_id_is_set
    def list(self, rt_type, ws_id=None, page_number=None, page_size=None,
             include=None):
        """
        GET /workspaces/:workspace_id/run-triggers
        """
        ws_id = ws_id if ws_id else self.ws_id

        if rt_type not in ['inbound', 'outbound']:
            self._logger.error(f"`{rt_type}` is invalid for `rt_type` arg."
                               " Valid values are `inbound` and `outbound`.")
            raise ValueError

        filters = [
            f'[run-trigger][type]={rt_type}'
        ]

        # TODO:
        # validate include is either `workspace` or `sourceable`
        
        path = f'/workspaces{ws_id}/run-triggers'
        return self._requestor.get(path=path, filters=filters, include=include,
                                   page_number=page_number, page_size=page_size)
        
    def show(self, rt_id, include=None):
        """
        GET /run-triggers/:run_trigger_id
        """
        path = f'/run-triggers/{rt_id}'
        return self._requestor.get(path=path, include=include)
    
    def delete(self, rt_id):
        """
        DELETE /run-triggers/:run_trigger_id
        """
        path = f'/run-triggers/{rt_id}'
        return self._requestor.delete(path=path)