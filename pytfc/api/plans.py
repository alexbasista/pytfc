"""TFC/E Plans API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import MissingRun
from .runs import Runs


class Plans(TfcApiBase):
    """
    TFC/E Plans methods.
    """    
    def get_plan_id_from_run(self, run_id=None, commit_message=None):
        runs_client = Runs(
          self._requestor,
          self.org,
          self.ws,
          self.ws_id,
          self.log_level
        )
        
        if run_id is not None:
          run = runs_client.show(run_id=run_id).json()
        elif commit_message is not None:
          run = runs_client.show(commit_message=commit_message).json()
        else:
          raise MissingRun

        del runs_client
        plan_id = run['data']['relationships']['plan']['data']['id']
        
        return plan_id
    
    def show(self, plan_id):
        """
        GET /plans/:id
        """
        path = f'/plans/{plan_id}'
        return self._requestor.get(path=path)
    
    def get_json_output(self, plan_id):
        """
        GET /plans/:id/json-output
        """
        path = f'/plans/{plan_id}/json-output'
        return self._requestor.get(path=path).json()