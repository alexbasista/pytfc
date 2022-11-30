"""TFC/E Runs API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from .configuration_versions import ConfigurationVersions
from pytfc.utils import validate_ws_id_is_set


class Runs(TfcApiBase):
    """
    TFC/E Runs methods.
    """
    @validate_ws_id_is_set
    def create(self, auto_apply=None, is_destroy=False, message='Queued by pytfc',
               refresh=True, refresh_only=False, replace_addrs=None,
               target_addrs=None, variables=None, plan_only=None,
               terraform_version=None, allow_empty_apply=None,
               ws_id=None, cv_id=None):
        """
        POST /runs
        
        Defaults to using latest Configuration Version
        in Workspace if `cv_id` arg is not specified.
        """
        ws_id = ws_id if ws_id else self.ws_id

        if cv_id is None:
            self._logger.debug("A `cv_id` was not specified. Defaulting to"
                               " latest Configuration Version in Workspace.")
            cv_client = ConfigurationVersions(
                self._requestor,
                self.org,
                self.ws,
                ws_id,
                self.log_level
            )
            cv_id = cv_client._get_latest_cv_id()
            self._logger.debug(f"Using Configuration Version `{cv_id}`.")
            del cv_client
        
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

        return self._requestor.post(path='/runs', payload=payload)

    def apply(self, run_id, comment='Applied by pytfc'):
        """
        POST /runs/:run_id/actions/apply
        """
        payload = {'comment': comment}
        path = f'/runs/{run_id}/actions/apply'
        return self._requestor.post(path=path, payload=payload)

    @validate_ws_id_is_set
    def list(self, page_number=None, page_size=None, filters=None,
             search=None, include=None, ws_id=None):
        """
        GET /workspaces/:workspace_id/runs
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        path = f'/workspaces/{ws_id}/runs'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, filters=filters,
                                   search=search)

    @validate_ws_id_is_set
    def list_all(self, filters=None, search=None, include=None, ws_id=None):
        """
        GET /workspaces/:workspace_id/runs

        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 Runs.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/runs'
        return self._requestor.list_all(path=path, filters=filters,
                                        search=search)

    def show(self, run_id, include=None):
        """
        GET /runs/:run_id
        """
        path = f'/runs/{run_id}'
        return self._requestor.get(path=path, include=include)

    def discard(self, run_id, comment='Discarded by pytfc'):
        """
        POST /runs/:run_id/actions/discard
        """
        payload = {'comment': comment}
        path = f'/runs/{run_id}/actions/discard'
        return self._requestor.post(path=path, payload=payload)

    def cancel(self, run_id, comment='Cancelled by pytfc'):
        """
        POST /runs/:run_id/actions/cancel
        """
        payload = {'comment': comment}
        path = f'/runs/{run_id}/actions/cancel'
        return self._requestor.post(path=path, payload=payload)

    def force_cancel(self, run_id, comment='Forcefully cancelled by pytfc'):
        """
        POST /runs/:run_id/actions/force-cancel
        """       
        # TODO:
        # Validate the Run to be forcefully cancelled is eligible
        # to be forcefully cancelled by the value of
        # `data.attributes.is-force-cancelable`

        payload = {'comment': comment}
        path = f'/runs/{run_id}/actions/force-cancel'
        return self._requestor.post(path=path, payload=payload)

    def force_execute(self, run_id):
        """
        POST /runs/:run_id/actions/force-execute
        """
        # TODO:
        # Validate prereqs of forcefully executing a Run:
        # 1) Rhe target Run is in a 'pending' state
        # 2) The Workspace is locked by another Run
        # 3) The Run that locked the Workspace can be discarded

        path = f'/runs/{run_id}/actions/force-execute'
        return self._requestor.post(path=path, payload=None)
    
    def get_plan_json_output(self, run_id):
        """
        GET /runs/:id/plan/json-output
        """
        path = f'/runs/{run_id}/plan/json-output'
        return self._requestor.get(path=path)
    
    @validate_ws_id_is_set
    def get_run_id_by_message(self, message, ws_id=None):
        """
        Helper method that returns Run ID of Run in 
        Workspace by Run `message` specified.
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        runs_list = self.list_all(ws_id=ws_id)
        for run in runs_list['data']:
            if run['type'] == 'runs' and run['attributes']['message'] == message:
                run_id = run['id']
                break
            else:
                run_id = None
                continue
        
        if run_id is None:
            self._logger.warning(\
                f"No Run was found from commit message `{message}`.")
        
        return run_id

    @validate_ws_id_is_set
    def get_latest_run_id(self, ws_id):
        """
        Helper method that returns Run ID of latest Run in Workspace.
        """       
        ws_id = ws_id if ws_id else self.ws_id
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