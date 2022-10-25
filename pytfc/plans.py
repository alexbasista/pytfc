"""
Module for TFC/E Plans API endpoint.
"""
from .exceptions import MissingRun


class Plans:
    """
    TFC/E Plans methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger

        self.plans_endpoint = '/'.join([self.client._base_uri_v2, 'plans'])
    
    def _get_plan_id(self, run_id=None, commit_message=None):
        if run_id is not None:
          run = self.client.runs.show(run_id=run_id)
        elif commit_message is not None:
          run = self.client.runs.show(commit_message=commit_message)
        else:
          raise MissingRun

        plan_id = run.json()['data']['relationships']['plan']['data']['id']
        
        return plan_id
    
    def show(self, plan_id=None, run_id=None, commit_message=None):
        """
        GET /plans/:id
        """
        if plan_id is not None:
          plan_id = plan_id
        elif run_id is not None:
          plan_id = self._get_plan_id(run_id=run_id)
        elif commit_message is not None:
          plan_id = self._get_plan_id(commit_message=commit_message)
        else:
          raise MissingRun
        
        return self.client._requestor.get(url='/'.join([
          self.plans_endpoint, plan_id]))
    
    def get_json_output(self, plan_id):
        """
        GET /plans/:id/json-output
        """
        return self.client._requestor.get(url='/'.join([self.plans_endpoint,
          plan_id, 'json-output'])).json()