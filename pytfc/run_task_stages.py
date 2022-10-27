"""
Module for TFC/E Run Task Stages API endpoints.
"""
from .exceptions import MissingWorkspace


class RunTaskStages:
    """
    TFC/E Run Tasks methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._base_api_url = self.client._base_uri_v2

        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None
    
    def list_stages(self, run_id, page_number=None, page_size=None,
            include=None):
        """
        GET /runs/:run_id/task-stages
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'runs', run_id, 'task-stages']), page_number=page_number,
            page_size=page_size, include=include)

    def show_stage(self, task_stage_id, include=None):
        """
        GET /task-stages/:task_stage_id
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'task-stages', task_stage_id]), include=include)
    
    def show_result(self, task_result_id, include=None):
        """
        GET /task-results/:task_result_id
        """
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'task-results', task_result_id]), include=include)