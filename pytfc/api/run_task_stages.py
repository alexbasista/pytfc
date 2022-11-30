"""TFC/E Run Task Stages API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class RunTaskStages(TfcApiBase):
    """
    TFC/E Run Tasks methods.
    """
    def list_stages(self, run_id, page_number=None, page_size=None,
                    include=None):
        """
        GET /runs/:run_id/task-stages
        """
        path = f'/runs/{run_id}/task-stages'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, include=include)

    def show_stage(self, task_stage_id, include=None):
        """
        GET /task-stages/:task_stage_id
        """
        path = f'/task-stages/{task_stage_id}'
        return self._requestor.get(path=path, include=include)
    
    def show_result(self, task_result_id, include=None):
        """
        GET /task-results/:task_result_id
        """
        path = f'/task-results/{task_result_id}'
        return self._requestor.get(path=path, include=include)