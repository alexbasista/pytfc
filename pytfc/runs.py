"""
Module for TFC/E Runs endpoint.
"""
from .exceptions import MissingWorkspace
from .exceptions import MissingRunId


class Runs(object):
    """
    TFC/E Runs methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self._ws_id = self.client.workspaces._get_ws_id(name=self.ws)
        else:
            if self.client.ws:
                self.ws = self.client.ws
                self._ws_id = self.client._ws_id
            else:
                raise MissingWorkspace
    
    def create(self, is_destroy='false', message='Queued via pytfc', cv_id=None, **kwargs):
        """
        POST /runs
        Defaults to using latest Configuration Version if 'cv_id' is not set.
        """
        # handle if Workspace (ws) argument is passsed
        if kwargs.get('ws'):
            ws_id = self.client.workspaces._get_ws_id(kwargs.get('ws'))
        else:
            ws_id = self._ws_id
        
        # handle if Configuration Versions ID is not specified by using the latest
        if cv_id is None:
            cv_id = self.client._get_latest_cv_id()
        
        payload = {}
        data = {}
        data['type'] = 'runs'
        attributes = {}
        attributes['is-destroy'] = is_destroy
        attributes['message'] = message
        attributes['refresh'] = 'true'
        attributes['refresh-only'] = 'false'
        data['attributes'] = attributes
        relationships = {}
        workspace = {}
        workspace_data = {}
        workspace_data['type'] = 'workspaces'
        workspace_data['id'] = ws_id
        workspace['data'] = workspace_data
        relationships['workspace'] = workspace
        configuration_version = {}
        configuration_version_data = {}
        configuration_version_data['type'] = 'configuration-versions'
        configuration_version_data['id'] = cv_id
        configuration_version['data'] = configuration_version_data
        relationships['configuration-version'] = configuration_version
        data['relationships'] = relationships
        payload['data'] = data

        return self.client._requestor.post(url='/'.join([self.client.base_url_v2, 'runs']), payload=payload)

    def apply(self, run_id=None, commit_message=None, comment='Applied by pytfc'):
        """
        POST /runs/:run_id/actions/apply
        """
        if run_id is None:
            if commit_message is None:
                run_id = self._get_latest_run_id()
            else:
                run_id = self._get_run_id_by_commit(commit_message=commit_message)

        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2, 'runs', run_id, 'actions', 'apply']), payload=payload)

    def list(self):
        """
        GET /workspaces/:workspace_id/runs
        """
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2, 'workspaces', self._ws_id, 'runs']))

    def _get_run_id_by_commit(self, commit_message):
        """
        Helper method that returns Run ID of Run in Workspace based on specified commit message.
        """
        runs_list = self.list()
        for run in runs_list.json()['data']:
            if run['type'] == 'runs' and run['attributes']['message'] == commit_message:
                run_id = run['id']
                break
            else:
                run_id = None
                continue
        
        if run_id is None:
            raise MissingRunId
        else:
            return run_id

    def _get_latest_run_id(self):
        """
        Helper method that returns Run ID of latest Run in Workspace.
        """       
        return self.list().json()['data'][0]['id']

    def show(self, run_id='latest', commit_message=None):
        """
        GET /runs/:run_id
        """
        if run_id != 'latest':
            run_id = run_id
        elif commit_message != None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            run_id = self._get_latest_run_id()
        
        return self.client._requestor.get(url="/".join([self.client._base_uri_v2, 'runs', run_id]))

    def discard(self, run_id=None, commit_message=None, comment="Discarded by pytfc"):
        """
        POST /runs/:run_id/actions/discard
        """
        if run_id is None:
            if commit_message is None:
                run_id = self._get_latest_run_id()
            else:
                run_id = self._get_run_id_by_commit(commit_message=commit_message)
        
        payload = {}
        payload['comment'] = comment

        return self.client._requestor.post(url="/".join([self.client._base_uri_v2, 'runs', run_id, 'actions', 'discard']))


    def cancel(self, run_id, commit_message=None, comment="Cancelled by pytfc"):
        """
        POST /runs/:run_id/actions/cancel
        """
        if run_id is None:
            if commit_message is None:
                run_id = self._get_latest_run_id()
            else:
                run_id = self._get_run_id_by_commit(commit_message=commit_message)
        
        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url="/".join([self.client._base_uri_v2, 'runs', run_id, 'actions', 'cancel']))
    
    
    def force_cancel(self, run_id=None, commit_message=None, comment="Forcefully cancelled by pytfc"):
        """
        POST /runs/:run_id/actions/force-cancel
        """
        if run_id is None:
            if commit_message is None:
                run_id = self._get_latest_run_id()
            else:
                run_id = self._get_run_id_by_commit(commit_message=commit_message)
        
        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url="/".join([self.client._base_uri_v2, 'runs', run_id, 'actions', 'force-cancel']))

    def force_execute(self, run_id=None, commit_message=None):
        """
        POST /runs/:run_id/actions/force-execute
        """
        if run_id is None:
            if commit_message is None:
                run_id = self._get_latest_run_id()
            else:
                run_id = self._get_run_id_by_commit(commit_message=commit_message)
        
        return self.client._requestor.post(url="/".join([self.client._base_uri_v2, 'runs', run_id, 'actions', 'force-execute']))
    

    ### --- workflows --- ###
    def terraform_plan(self, source_tf_path, dest_tf_tar, speculative='false', cleanup='true', **kwargs):
        """
        Wraps multiple Configuration Versions and Runs functions
        into a workflow to execute a remote Terraform Plan
        """
        print('coming soon')

    def terraform_apply(self, run_id, **kwargs):
        print('coming soon')