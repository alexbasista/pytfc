"""
Module for TFC/E Plans endpoint.
"""
from pytfc.exceptions import MissingWorkspace


class Plans(object):
    """
    TFC/E Plans methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
        else:
            if self.client.ws:
                self.ws = self.client.ws
            else:
                raise MissingWorkspace
        
        self._ws_id = self.client.workspaces._get_ws_id(self.ws)
        self.plans_endpoint = '/'.join([self.client._base_uri_v2, 'plans'])
    
    def _get_plan_id(self, **kwargs):
        if kwargs.get('run_id'):
          # retrieve Run by Run ID
          run_object = self.client.runs.show(run_id=kwargs.get('run_id'))
        elif kwargs.get('commit_message'):
          # retrieve Run by Commit Message
          run_object = self.client.runs.show(commit_message=kwargs.get('commit_message'))
        else:
          # retrieve latest Run
          run_object = self.client.runs.show(run_id='latest')

        print("[INFO] Getting Plan from RunID: {}".format(run_object.json()['data']['id']))
        print("[INFO] Found PlanID: {}".format(run_object.json()['data']['relationships']['plan']['data']['id']))
        return run_object.json()['data']['relationships']['plan']['data']['id']
    
    def show(self, **kwargs):
        """
        GET /plans/:id
        """
        if kwargs.get('plan_id'):
          if kwargs.get('plan_id', 'latest'):
            # retrieve Plan ID of latest Run
            plan_id = self._get_plan_id(run_id='latest')
          else:
            # retrieve Plan by Plan ID
            plan_id = kwargs.get('plan_id')
        elif kwargs.get('run_id'):
          # retrieve Run by Run ID to derive Plan
          plan_id = self._get_plan_id(run_id=kwargs.get('run_id'))
        elif kwargs.get('commit_message'):
          # retrieve Run by Commit Message to derive Plan
          plan_id = self._get_plan_id(commit_message=kwargs.get('commit_message'))
        else:
          # retrieve Plan ID of latest Run
          plan_id = self._get_plan_id(run_id='latest')
        
        return self.client._requestor.get(url="/".join([self.plans_endpoint, plan_id]))
    
    def get_json_output(self, **kwargs):
        """
        GET /plans/:id/json-output
        """
        if kwargs.get('plan_id'):
          # retrieve Plan by Plan ID
          plan_id = kwargs.get('plan_id')
        elif kwargs.get('run_id'):
          # retrieve Run by Run ID to derive Plan
          plan_id = self._get_plan_id(run_id=kwargs.get('run_id'))
        elif kwargs.get('commit_message'):
          # retrieve Run by Commit Message to derive Plan
          plan_id = self._get_plan_id(commit_message=kwargs.get('commit_message'))
        else:
          # retrieve latest Run to derive Plan
          plan_id = self._get_plan_id(run_id='latest')
        
        return self.client._requestor.get(url="/".join([self.plans_endpoint, plan_id, 'json-output'])).json()