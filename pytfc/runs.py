"""
Module for TFC/E Runs API endpoint.
"""
from .configuration_versions import ConfigurationVersions
from .exceptions import MissingWorkspace
from .exceptions import MissingRun


class Runs:
    """
    TFC/E Runs methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws_id'):
            self.ws_id = kwargs.get('ws_id')
            self.ws = self.client.workspaces.get_ws_name(ws_id=self.ws_id)
        elif kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None
    
    def create(self, auto_apply=None, is_destroy=False, message='Queued by pytfc',
                refresh=True, refresh_only=False, replace_addrs=None,
                target_addrs=None, variables=None, plan_only=None,
                terraform_version=None, allow_empty_apply=None,
                cv_id=None, ws_id=None):
        """
        POST /runs
        
        Defaults to using latest Configuration Version
        in Workspace if `cv_id` arg is not specified.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        if cv_id is None:
            cv = ConfigurationVersions(client=self.client, ws_id=ws_id)
            cv_id = cv._get_latest_cv_id()
        
        payload = {}
        data = {}
        data['type'] = 'runs'
        attributes = {}
        attributes['auto-apply'] = auto_apply
        attributes['is-destroy'] = is_destroy
        attributes['message'] = message
        attributes['refresh'] = refresh
        attributes['refresh-only'] = refresh_only
        attributes['replace-addrs'] = replace_addrs
        attributes['target-addrs'] = target_addrs
        attributes['variables'] = variables
        attributes['plan-only'] = plan_only
        attributes['terraform-version'] = terraform_version
        attributes['allow-empty-apply'] = allow_empty_apply
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

        return self.client._requestor.post(url='/'.join([
            self.client._base_uri_v2, 'runs']), payload=payload)

    def apply(self, run_id=None, commit_message=None, comment='Applied by pytfc'):
        """
        POST /runs/:run_id/actions/apply
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is None:
            self._logger.info(\
                f"Using Run with commit message `{commit_message}` in Workspace.")
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            raise MissingRun

        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url='/'.join([
            self.client._base_uri_v2, 'runs', run_id, 'actions', 'apply']),
            payload=payload)

    def list(self, page_number=None, page_size=None, filters=None, search=None,
            ws_id=None):
        """
        GET /workspaces/:workspace_id/runs
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
            'workspaces', ws_id, 'runs']), page_number=page_number,
            page_size=page_size, filters=filters, search=search)

    def show(self, run_id=None, commit_message=None):
        """
        GET /runs/:run_id
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is not None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
            print(f"Found Run: {run_id}")
        else:
            raise MissingRun
        
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
            'runs', run_id]))

    def discard(self, run_id=None, commit_message=None,
            comment='Discarded by pytfc'):
        """
        POST /runs/:run_id/actions/discard
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is not None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            raise MissingRun
        
        payload = {}
        payload['comment'] = comment

        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
            'runs', run_id, 'actions', 'discard']))

    def cancel(self, run_id=None, commit_message=None,
            comment='Cancelled by pytfc'):
        """
        POST /runs/:run_id/actions/cancel
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is not None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            raise MissingRun
        
        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
            'runs', run_id, 'actions', 'cancel']))

    def force_cancel(self, run_id=None, commit_message=None,
            comment='Forcefully cancelled by pytfc'):
        """
        POST /runs/:run_id/actions/force-cancel
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is not None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            raise MissingRun
        
        payload = {}
        payload['comment'] = comment
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
            'runs', run_id, 'actions', 'force-cancel']))

    def force_execute(self, run_id=None, commit_message=None):
        """
        POST /runs/:run_id/actions/force-execute
        """
        if run_id is not None:
            run_id = run_id
        elif commit_message is not None:
            run_id = self._get_run_id_by_commit(commit_message=commit_message)
        else:
            raise MissingRun
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
            'runs', run_id, 'actions', 'force-execute']))
    
    def get_plan_json_output(self, run_id):
        """
        GET /runs/:id/plan/json-output
        """
        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
            'runs', run_id, 'plan', 'json-output']))
    
    def _get_run_id_by_commit(self, commit_message, ws_id=None):
        """
        Helper method that returns Run ID of Run in 
        Workspace by `commit_message` that is passed in.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        runs_list = self.list(ws_id=ws_id)
        for run in runs_list.json()['data']:
            if run['type'] == 'runs' and run['attributes']['message'] == commit_message:
                run_id = run['id']
                break
            else:
                run_id = None
                continue
        
        if run_id is None:
            self._logger.warning(\
                f"No Run was found from commit message `{commit_message}`.")
        
        return run_id

    def _get_latest_run_id(self, ws_id):
        """
        Helper method that returns Run ID of latest Run in Workspace.
        """       
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        runs_list = self.list(ws_id=ws_id)

        return runs_list.json()['data'][0]['id']

    def terraform_plan(self, source_tf_path, dest_tf_tar, speculative='false', cleanup='true', **kwargs):
        """
        Utility method that wraps other methods from
        other classes to trigger a Terraform Plan.
        """
        print('coming soon')

    def terraform_apply(self, run_id, **kwargs):
        """
        Utility method that wraps other methods from
        other classes to trigger a Terraform Apply
        off of a Run.
        """
        print('coming soon')