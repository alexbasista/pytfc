"""
Module for TFC/E Runs endpoint.
"""
import time
from pytfc.exceptions import MissingWorkspace
from pytfc.exceptions import MissingRunId
from pytfc.api.configuration_versions import ConfigurationVersions


class Runs(object):
    """
    TFC/E Runs methods.
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
        data['configuration-version'] = configuration_version
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
            if run['type'] == "runs" and run['attributes']['message'] == commit_message:
                return run['id']
            else:
                raise MissingRunId

    def _get_latest_run_id(self):
        """
        Helper method that returns Run ID of latest Run in Workspace.
        """
        runs_list = self.list()
        
        return runs_list.json()['data'][0]['id']

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
        # # create Terraform tar.gz
        # tf_tar = self.client.configuration_versions._create_tf_tarfile(source=source_tf_path, dest=dest_tf_tar)
        
        # # handle if Workspace (ws) argument explicitly specified
        # if kwargs.get('ws'):
        #     ws_id = self.client.workspaces._get_ws_id(kwargs.get('ws'))
        # else:
        #     ws_id = self._ws_id
        
        # # create Configuration Version
        # cv = self.client.configuration_versions.create(ws_id=ws_id, auto_queue_runs='false', speculative=speculative)
        # cv_id = cv['data']['id']
        # cv_upload_url = cv['data']['attributes']['upload-url']

        # # get Configuration Version status
        # cv_status = self.client.configuration_versions.get_cv_status(cv_id=cv_id)
        
        # # poll Configuration Version status until it is ready to use
        # while (cv_status is not 'uploaded'):
        #     time.sleep(1)
        #     cv_status = self.client.configuration_versions.get_cv_status(cv_id=cv_id)
        #     if cv_status is 'uploaded':
        #         break
        
        # # upload Terraform tar.gz to Configuration Version
        # with open(tf_tar, 'rb') as tf_upload:
        #     self.client.configuration_versions.upload(cv_upload_url=cv_upload_url, tf_tarfile=tf_upload)

        # # evaluate if Speculative Plan was specified
        # #if speculative is 'true':
            

        # # create Terraform Run
        # #self.create()

        # # delete temporary Terraform tar.gz after upload
        # if cleanup is 'true':
        #     self.client.configuration_versions._cleanup_tf_tarfile(path=tf_tar)
        # elif cleanup is 'false':
        #     print("INFO: skipping cleanup of {}".format(tf_tar))
        # else:
        #     raise ValueError("ERROR: '{}' is an invalid argument for 'cleanup' parameter. Valid arguments: 'true' or 'false'.".format(cleanup))

        # return run_id

    def terraform_apply(self, run_id, **kwargs):
        print('coming soon')