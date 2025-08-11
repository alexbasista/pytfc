"""TFC/E Workspace API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc import utils


class Workspaces(TfcApiBase):
    """
    TFC/E Workspaces methods.
    """
    _ws_attr_list = [
        'name',
        'agent_pool_id',
        'allow_destroy_plan',
        'auto_apply',
        'description',
        'execution_mode',
        'file_triggers_enabled',
        'global_remote_state',
        'queue_all_runs',
        'source_name',
        'source_url',
        'speculative_enabled',
        'terraform_version',
        'trigger_prefixes',
        'trigger_patterns',
        'working_directory',
        'assessments_enabled'
    ]
    _ws_vcs_attr_list = [
        'oauth_token_id',
        'branch',
        'ingress_submodules',
        'identifier',
        'tags_regex',
        'github_app_installation_id',
        'vcs_repo' # only used by `update()` to remove repo from Workspace
    ]

    @utils.validate_ws_is_set
    def get_ws_id(self, name=None):
        """
        Helper method that returns Workspace ID based on Workspace name.
        """
        ws_name = name if name else self.ws
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        ws = self._requestor.get(path=path)

        return ws.json()['data']['id']

    @utils.validate_ws_id_is_set
    def get_ws_name(self, ws_id=None):
        """
        Helper method that returns Workspace name based on Workspace ID.
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}'
        ws = self._requestor.get(path=path)

        return ws.json()['data']['attributes']['name']

    @utils.validate_ws_is_set
    def create(self, name=None, project_id=None, **kwargs):
        """
        POST /organizations/:organization_name/workspaces
        """
        ws_name = name if name else self.ws
        
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        vcs_repo = {}
        attributes['name'] = ws_name
        kwargs.pop('new_name', None)
        for key, value in kwargs.items():
            if key in self._ws_attr_list:
                attributes[key] = value
            elif key in self._ws_vcs_attr_list:
                new_key = key.replace("_", "-" )
                vcs_repo[new_key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Workspaces API.")
        if len(vcs_repo) > 0 and not all(i == None for i in vcs_repo.values()):
            # Check if all VCS repo attributes are null and if they are, do NOT
            # add to payload to avoid 422 error with Workspace creation.
            attributes['vcs-repo'] = vcs_repo
        data['attributes'] = attributes

        if project_id is not None:
            relationships = {}
            project = {}
            project_data = {}
            project_data['id'] = project_id
            project['data'] = project_data
            relationships['project'] = project
            data['relationships'] = relationships
        
        payload['data'] = data
        path = f'/organizations/{self.org}/workspaces'
        return self._requestor.post(path=path, payload=payload)

    @utils.validate_ws_is_set
    def update(self, name=None, project_id=None, **kwargs):
        """
        PATCH /organizations/:organization_name/workspaces/:name
        """
        ws_name = name if name else self.ws

        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        vcs_repo = {}
        if kwargs.get('new_name'):
            attributes['name'] = kwargs.get('new_name')
            kwargs.pop('new_name')
        for key, value in kwargs.items():
            if key in self._ws_attr_list:
                attributes[key] = value
            elif key in self._ws_vcs_attr_list:
                if key == 'vcs_repo':
                    pass
                else:
                    new_key = key.replace("_", "-" )
                    vcs_repo[new_key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Workspaces API.")
        if kwargs.get('vcs_repo') == 'null':
            attributes['vcs-repo'] = None
        elif len(vcs_repo) > 0 and not all(i == None for i in vcs_repo.values()):
            # Check if all VCS repo attributes are null and if they are, do NOT
            # add to payload to avoid 422 error with Workspace creation.
            attributes['vcs-repo'] = vcs_repo
        data['attributes'] = attributes
        
        if project_id is not None:
            relationships = {}
            project = {}
            project_data = {}
            project_data['id'] = project_id
            project['data'] = project_data
            relationships['project'] = project
            data['relationships'] = relationships
        
        payload['data'] = data
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.patch(path=path, payload=payload)

    def list(self, page_number=None, page_size=None, search=None, include=None):
        """
        GET /organizations/:organization_name/workspaces
        """
        path = f'/organizations/{self.org}/workspaces/'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, search=search,
                                   include=include)

    def list_all(self, search=None, include=None):
        """
        GET /organizations/:organization_name/workspaces

        Built-in logic to enumerate all pages in list response
        for cases where there are more than 100 Workspace.

        Returns object (dict) with two arrays: `data` and `included`.
        """
        path = f'/organizations/{self.org}/workspaces/'
        return self._requestor.list_all(path=path, search=search,
                                         include=include)

    @utils.validate_ws_is_set
    def show(self, name=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        """
        ws_name = name if name else self.ws
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.get(path=path)

    def delete(self, name):
        """
        DELETE /organizations/:organization_name/workspaces/:name
        """
        ws_name = name
        path = f'/organizations/{self.org}/workspaces/{ws_name}'
        return self._requestor.delete(path=path)

    @utils.validate_ws_is_set
    def lock(self, name=None, **kwargs):
        """
        POST /workspaces/:workspace_id/actions/lock
        """
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        reason = kwargs.pop('reason', 'Locked by pytfc')
        payload = { 'reason': reason }
        
        path = f'/workspaces/{ws_id}/actions/lock'
        return self._requestor.post(path=path, payload=payload)

    @utils.validate_ws_is_set
    def unlock(self, name=None):
        """
        POST /workspaces/:workspace_id/actions/unlock
        """
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        path = f'/workspaces/{ws_id}/actions/unlock'
        return self._requestor.post(path=path, payload=None)

    @utils.validate_ws_is_set
    def force_unlock(self, name=None):
        """
        POST /workspaces/:workspace_id/actions/force-unlock
        """
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        path = f'/workspaces/{ws_id}/actions/force-unlock'
        return self._requestor.post(path=path, payload=None)

    @utils.validate_ws_is_set
    def assign_ssh_key(self, ssh_key_id, name=None):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key
        """
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        attributes['id'] = ssh_key_id
        data['attributes'] = attributes
        payload['data'] = data
        
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        path = f'/workspaces/{ws_id}/relationships/ssh-key'
        return self._requestor.patch(path=path, payload=payload)

    @utils.validate_ws_is_set
    def unassign_ssh_key(self, name=None):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key
        """
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        attributes['id'] = 'null'
        data['attributes'] = attributes
        payload['data'] = data
        
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        path = f'/workspaces/{ws_id}/relationships/ssh-key'
        return self._requestor.patch(path=path, payload=payload)
    
    @utils.validate_ws_is_set
    def get_remote_state_consumers(self, name=None, page_number=None,
                                   page_size=None):
        """
        GET /workspaces/:workspace_id/relationships/remote-state-consumers
        """

        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        path = f'/workspaces/{ws_id}/relationships/remote-state-consumers'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    @utils.validate_ws_is_set
    def replace_remote_state_consumers(self, name=None):
        """
        PATCH /workspaces/:workspace_id/relationships/remote-state-consumers
        """
        # first check if `global-remote-state is false`

        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')
    
    @utils.validate_ws_is_set
    def add_remote_state_consumers(self, name=None):
        """
        POST /workspaces/:workspace_id/relationships/remote-state-consumers
        """
        # first check if `global-remote-state is false`
        
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')

    @utils.validate_ws_is_set
    def delete_remote_state_consumers(self, name=None):
        """
        DELETE /workspaces/:workspace_id/relationships/remote-state-consumers
        """
        # first check if `global-remote-state is false`

        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')

    @utils.validate_ws_is_set
    def get_tags(self, name=None):
        """
        GET /workspaces/:workspace_id/relationships/tags
        """
        # query parameters

        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')

    @utils.validate_ws_is_set
    def add_tags(self, name=None):
        """
        POST /workspaces/:workspace_id/relationships/tags
        """
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')

    @utils.validate_ws_is_set
    def remove_tags(self, name=None):
        """
        DELETE /workspaces/:workspace_id/relationships/tags
        """
        ws_name = name if name else self.ws
        ws_id = self.get_ws_id(name=ws_name)
        print('coming soon.')