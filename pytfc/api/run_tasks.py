"""TFC/E Run Tasks API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set


class RunTasks(TfcApiBase):
    """
    TFC/E Run Tasks methods.
    """
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
        # validate include is `workspace_tasks` or `workspace_tasks.workspace`
        
        path = f'/organizations/{self.org}/tasks'
        return self._requestor.get(path=path, include=include,
                                   page_number=page_number,
                                   page_size=page_size)
    
    def show(self, task_id, include=None):
        """
        GET /tasks/:id

        :param include: Allows including related resource data. Value
            must be a Value must be a comma-separated list containing one
            or more of `workspace_tasks` or `workspace_tasks.workspace`.
        :type include: list
        """
        # TODO:
        # validate include is `workspace_tasks` or `workspace_tasks.workspace`
        path = f'/tasks/{task_id}'
        return self._requestor.get(path=path, include=include)
        
    def update(self, task_id, **kwargs):
        """
        PATCH /tasks/:id
        """
        print('coming soon')

    def delete(self, task_id):
        """
        DELETE /tasks/:id
        """
        path = f'/tasks/{task_id}'
        return self._requestor.delete(path=path)
        
    @validate_ws_id_is_set
    def associate_to_ws(self, task_id, ws_id=None):
        """
        POST /workspaces/:workspace_id/tasks
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')
    
    @validate_ws_id_is_set
    def list_for_ws(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/tasks
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/tasks'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    @validate_ws_id_is_set
    def show_for_ws(self, task_id, ws_id):
        """
        GET /workspaces/:workspace_id/tasks/:id
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/tasks/{task_id}'
        return self._requestor.get(path=path)

    @validate_ws_id_is_set
    def update_for_ws(self, ws_id=None):
        """
        PATCH /workspaces/:workspace_id/tasks/:id
        """
        ws_id = ws_id if ws_id else self.ws_id
        print('coming soon')
    
    @validate_ws_id_is_set
    def delete_for_ws(self, task_id, ws_id=None):
        """
        DELETE /workspaces/:workspace_id/tasks/:id
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/tasks/{task_id}'
        return self._requestor.delete(path=path)