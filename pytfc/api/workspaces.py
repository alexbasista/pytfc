"""
Module for TFC/E Workspace API endpoint.
"""
from pytfc.exceptions import MissingOrganization
from pytfc.exceptions import MissingWorkspace
from pytfc.exceptions import MissingVcsProvider
from .oauth_clients import OauthClients
from pytfc.tfc_api_base import TfcApiBase
import logging
#from pytfc.utils import validate_ws_is_set, validate_ws_id_is_set
from pytfc import utils


class Workspaces(TfcApiBase):
    """
    TFC/E Workspaces methods.
    """
    _logger = logging.getLogger(__name__)
    
    _ws_attr_list = [
        'name',
        'agent_pool_id',
        'allow_destroy_plan',
        'auto_apply',
        'description',
        'execution_mode',
        'file_triggers_enabled',
        'global-remote-state',
        'queue_all_runs',
        'source_name', # beta
        'source_url', # beta
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
        'vcs_repo' # only used by `update()` to remove repo from Workspace
    ]
    
    # def __init__(self, client, **kwargs):
    #     self.client = client
    #     self._logger = client._logger

    #     if kwargs.get('org'):
    #         self.org = kwargs.get('org')
    #     elif self.client.org:
    #         self.org = self.client.org                
    #     else:
    #         raise MissingOrganization
        
    #     self.ws_endpoint = '/'.join([
    #         self.client._base_uri_v2, 'organizations', self.org, 'workspaces'
    #     ])

    #     if kwargs.get('ws'):
    #         self.ws = kwargs.get('ws')
    #         self.ws_id = self.get_ws_id(name=kwargs.get('ws'))
    #     elif self.client.ws_id:
    #         self.ws = self.client.ws
    #         self.ws_id = self.client.ws_id
    #     else:
    #         self.ws = None
    #         self.ws_id = None

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
    def create(self, name=None, **kwargs):
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
                vcs_repo[key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Workspaces API.")
        
        # handle multiple scenarios with obtaining the OAuth Token ID attribute
        if kwargs.get('identifier'):
            self._logger.info(\
                f"VCS repo identifier `{kwargs.get('identifier')}` was specified.")
            oc = OauthClients(client=self.client)
            # validate an OAuth Client (VCS Provider) actually exists in the Org
            try:
                self._logger.info(\
                    f"Retrieving list of OAuth Clients (VCS Providers) in Org `{self.org}`.")
                oc_list = oc.list()
                if len(oc_list.json()['data']) < 1:
                    self._logger.error(\
                        f"No OAuth Client (VCS Provider) was found in Org `{self.org}`.")
                    raise MissingVcsProvider
                elif len(oc_list.json()['data']) >= 1:
                    oc_display_name = oc_list.json()['data'][0]['attributes']['name']
                    ot_id = oc_list.json()\
                        ['data'][0]['relationships']['oauth-tokens']['data'][0]['id']
            except Exception as e:
                self._logger.error(\
                    f"Unable to retrieve OAuth Clients (VCS Providers) list from Org `{self.org}`.")
                self._logger.error(e)
            
            # explicitly specifying an OAuth Token ID gets first priority
            if kwargs.get('oauth_token_id'):
                self._logger.info("An OAuth Token ID was specified directly.")
                vcs_repo['oauth-token-id'] = kwargs.get('oauth_token_id')
            
            # explicitly specifying an OAuth Client (VCS Provider) Display Name
            # (`oauth_client_name`) gets second priority
            elif kwargs.get('oauth_client_name'):
                self._logger.info("An OAuth Client Display Name was specified directly.")
                oauth_client = oc.show(name=kwargs.get('oauth_client_name'))
                vcs_repo['oauth-token-id'] = oauth_client.json()\
                    ['data']['relationships']['oauth-tokens']['data'][0]['id']
            
            # if neither are specified and there is only one OAuth
            # Oauth Client in the Org - default to using that one
            elif kwargs.get('oauth_token_id') is None\
                and kwargs.get('oauth_client_name') is None\
                and len(oc_list.json()['data']) == 1:
                    self._logger.info(f"Detected `{oc_display_name}` is the only OAuth Client, proceeding with this one.")
                    vcs_repo['oauth-token-id'] = ot_id
            
            # if neither are specified and there are multiple OAuth Clients in the Org,
            # then log a warning but default to the first OAuth Client returned in the list
            elif kwargs.get('oauth_token_id') is None\
                and kwargs.get('oauth_client_name') is None\
                and len(oc_list.json()['data']) > 1:
                    self._logger.warning(\
                        "Detected multiple OAuth Clients exist but a specific one was not specified.")
                    self._logger.info(\
                        f"Proceeding with using `{oc_display_name}` because it was first in the list.")
                    vcs_repo['oauth-token-id'] = ot_id
            else:
                self._logger.error(\
                    "An unknown error occured determining which OAuth Client and/or OAuth Token ID to use.")
                exit
        else:
            self._logger.debug(\
                "No VCS repo identifier specified. Creating Workspace without VCS.")
        
        if len(vcs_repo) > 0:
            attributes['vcs-repo'] = vcs_repo
        data['attributes'] = attributes
        payload['data'] = data
        
        path = f'/organizations/{self.org}/workspaces/'
        return self._requestor.post(path=path, payload=payload)

    @utils.validate_ws_is_set
    def update(self, name=None, **kwargs):
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
                    vcs_repo[key] = value
            else:
                self._logger.warning(\
                    f"`{key}` is an invalid key for Workspaces API.")

        if kwargs.get('vcs_repo') == 'null':
            attributes['vcs-repo'] = None
        elif len(vcs_repo) > 0:
            attributes['vcs-repo'] = vcs_repo

        data['attributes'] = attributes
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
        return self._requestor._list_all(path=path, search=search,
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