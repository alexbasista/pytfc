"""
TFC/E Runs API endpoints module.

This module provides a modern, type-safe interface to Terraform Cloud/Enterprise
run management operations including creation, execution control, and monitoring.
"""
from typing import Any, Dict, List, Optional, Union

from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import PyTFCError
from .configuration_versions import ConfigurationVersions
from pytfc.utils import validate_ws_id_is_set


class Runs(TfcApiBase):
    """
    TFC/E Runs API client.
    
    Provides methods for managing Terraform Cloud/Enterprise runs including
    creation, execution control, monitoring, and state management.
    
    Examples:
        Create a new run:
        >>> run = client.runs.create(
        ...     message='Deploy infrastructure',
        ...     auto_apply=True
        ... )
        
        Apply a planned run:
        >>> client.runs.apply(
        ...     run_id='run-abc123',
        ...     comment='Approved for deployment'
        ... )
        
        List workspace runs:
        >>> runs = client.runs.list()
        >>> for run in runs['data']:
        ...     print(f"{run['id']}: {run['attributes']['message']}")
    """
    @validate_ws_id_is_set
    def create(
        self,
        message: str = 'Queued by pytfc',
        auto_apply: bool = False,
        is_destroy: bool = False,
        refresh: bool = True,
        refresh_only: bool = False,
        plan_only: bool = False,
        save_plan: bool = False,
        allow_empty_apply: Optional[bool] = None,
        allow_config_generation: bool = False,
        replace_addrs: Optional[List[str]] = None,
        target_addrs: Optional[List[str]] = None,
        variables: Optional[List[Dict[str, Any]]] = None,
        terraform_version: Optional[str] = None,
        ws_id: Optional[str] = None,
        cv_id: Optional[str] = None,
        **kwargs: Any
    ) -> Any:
        """
        Create a new run in the workspace.
        
        Args:
            message: Run message/description
            auto_apply: Whether to automatically apply after planning
            is_destroy: Whether this is a destroy run
            refresh: Whether to refresh state before planning
            refresh_only: Whether to only refresh state (no plan/apply)
            plan_only: Whether to only plan (no apply even if auto_apply=True)
            save_plan: Whether to save the plan for later application
            allow_empty_apply: Whether to allow applies with no changes
            allow_config_generation: Whether to allow config generation
            replace_addrs: List of resource addresses to replace
            target_addrs: List of resource addresses to target
            variables: List of variables for this run
            terraform_version: Specific Terraform version to use
            ws_id: Workspace ID (uses self.ws_id if not provided)
            cv_id: Configuration version ID (uses latest if not provided)
            **kwargs: Additional run attributes
            
        Returns:
            API response with created run data
            
        Examples:
            Basic run:
            >>> run = client.runs.create(message='Deploy infrastructure')
            
            Auto-apply run:
            >>> run = client.runs.create(
            ...     message='Deploy to production',
            ...     auto_apply=True
            ... )
            
            Destroy run:
            >>> run = client.runs.create(
            ...     message='Destroy old resources',
            ...     is_destroy=True
            ... )
            
            Targeted run:
            >>> run = client.runs.create(
            ...     message='Update specific resources',
            ...     target_addrs=['aws_instance.web', 'aws_s3_bucket.data']
            ... )
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
        attributes['allow-empty-apply'] = allow_empty_apply
        attributes['allow-config-generation'] = allow_config_generation
        attributes['auto-apply'] = auto_apply
        attributes['is-destroy'] = is_destroy
        attributes['message'] = message
        attributes['refresh'] = refresh
        attributes['refresh-only'] = refresh_only
        attributes['replace-addrs'] = replace_addrs
        attributes['target-addrs'] = target_addrs
        attributes['variables'] = variables
        attributes['plan-only'] = plan_only
        attributes['save-plan'] = save_plan
        attributes['terraform-version'] = terraform_version
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

    def apply(self, run_id: str, comment: str = 'Applied by pytfc') -> Any:
        """
        Apply a planned run.
        
        Args:
            run_id: ID of the run to apply
            comment: Comment for the apply action
            
        Returns:
            API response confirming apply action
            
        Examples:
            Apply with default comment:
            >>> client.runs.apply(run_id='run-abc123')
            
            Apply with custom comment:
            >>> client.runs.apply(
            ...     run_id='run-abc123',
            ...     comment='Approved by security team'
            ... )
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
        # 1) The target Run is in a 'pending' state
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
