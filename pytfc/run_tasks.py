"""
Module for TFC/E Run Tasks API endpoints.
"""
from .exceptions import MissingWorkspace


class RunTasks:
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

    def create(self, name, url, description, category, hmac_key, enabled=True):
        """
        POST /organizations/:organization_name/tasks
        """
        print('coming soon')
    
    def list(self, include=None, page_number=None, page_size=None):
        """
        GET /organizations/:organization_name/tasks

        :param include: Allows including related resource data. Value
            must be a Value must be a comma-separated list containing one
            or more of `workspace_tasks` or `workspace_tasks.workspace`.
        :type include: list
        """
        # TODO:
        # validate filters is `workspace_tasks` or `workspace_tasks.workspace`
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'organizations', self.client.org, 'tasks']), include=include,
            page_number=page_number, page_size=page_size)
    
    def show(self, task_id, include=None):
        """
        GET /tasks/:id

        :param include: Allows including related resource data. Value
            must be a Value must be a comma-separated list containing one
            or more of `workspace_tasks` or `workspace_tasks.workspace`.
        :type include: list
        """
        # TODO:
        # validate filters is `workspace_tasks` or `workspace_tasks.workspace`
        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'tasks', task_id]), include=include)
        
    def update(self, task_id, **kwargs):
        """
        PATCH /tasks/:id
        """
        print('coming soon')

    def delete(self, task_id):
        """
        DELETE /tasks/:id
        """
        return self.client._requestor.delete(url='/'.join([self._base_api_url,
            'tasks', task_id]))
        
    def associate_to_ws(self, task_id, ws_id=None):
        """
        POST /workspaces/:workspace_id/tasks
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace
    
    def list_for_ws(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/tasks
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'tasks']), page_number=page_number,
            page_size=page_size)

    def show_for_ws(self, task_id, ws_id):
        """
        GET /workspaces/:workspace_id/tasks/:id
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'tasks', task_id]))

    def update_for_ws(self, ws_id=None):
        """
        PATCH /workspaces/:workspace_id/tasks/:id
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace

        print('coming soon')
    
    def delete_for_ws(self, task_id, ws_id=None):
        """
        DELETE /workspaces/:workspace_id/tasks/:id
        """
        if ws is not None:
            ws = ws
        elif self.ws:
            ws = self.ws
        else:
            raise MissingWorkspace

        return self.client._requestor.delete(url='/'.join([self._base_api_url,
            'workspaces', ws_id, 'tasks', task_id]))