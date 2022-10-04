"""
Module for TFC/E Workspace endpoints.
"""
#import sys
from pytfc.exceptions import MissingOrganization
from pytfc.exceptions import MissingWorkspace
#from pytfc.exceptions import MissingOauthClient
from pytfc.exceptions import MissingVcsProvider
from pytfc.oauth_clients import OauthClients


class Workspaces(object):
    """
    TFC/E Workspaces methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        if kwargs.get('org'):
            self.org = kwargs.get('org')
        else:
            if self.client.org:
                self.org = self.client.org
            else:
                raise MissingOrganization
        
        self.workspaces_endpoint = '/'.join([self.client._base_uri_v2, 'organizations', self.org, 'workspaces'])
        self.ws_attributes_list = [
            'name',
            'agent_pool_id',
            'allow_destroy_plan',
            'auto_apply',
            'description',
            'execution_mode',
            'file_triggers_enabled',
            'source_name',
            'source_url',
            'queue_all_runs',
            'speculative_enabled',
            'terraform_version',
            'trigger_prefixes',
            'working_directory'
        ]
        self.ws_vcs_attributes_list = [
            'oauth_token_id',
            'branch',
            'default_branch',
            'ingress_submodules',
            'identifier'
        ]
    
    def _get_ws_id(self, name):
        """
        Helper method that returns Workspace ID based on Workspace name.
        """
        ws = self.client._requestor.get(url='/'.join([self.workspaces_endpoint, name]))
        return ws.json()['data']['id']

    def create(self, name=None, **kwargs):
        """
        POST /organizations/:organization_name/workspaces
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        vcs_repo = {}
        attributes['name'] = name
        kwargs.pop('new_name', None)
        for key, value in kwargs.items():
            if key in self.ws_attributes_list:
                attributes[key] = value
            elif key in self.ws_vcs_attributes_list:
                vcs_repo[key] = value
            else:
                print("[WARNING] '{}' is an invalid key for Workspaces API.".format(key))
        
        # handle multiple scenarios with obtaining the OAuth Token ID attribute
        if kwargs.get('identifier'):
            print("[INFO] VCS repo identifier '{}' was specified.".format(kwargs.get('identifier')))
            oc = OauthClients(client=self.client)
            try: # validate an OAuth Client (VCS Provider) actually exists in the Org
                print("[INFO] Retrieving list of OAuth Clients (VCS Providers) in '{}' Organization.".format(self.org))
                oc_list = oc.list()
                if len(oc_list.json()['data']) < 1:
                    print("[ERROR] VCS repo identifier '{}' was specified but no OAuth Client (VCS Provider) was found in '{}' Organization.".format(kwargs.get('identifier'), self.org))
                    raise MissingVcsProvider
                elif len(oc_list.json()['data']) >= 1:
                    oc_display_name = oc_list.json()['data'][0]['attributes']['name']
                    ot_id = oc_list.json()['data'][0]['relationships']['oauth-tokens']['data'][0]['id']
            except Exception as e:
                print("[ERROR] Unable to retrieve OAuth Clients (VCS Providers) list from '{}' Organization.".format(self.org))
                print(e)
            
            # explicitly specifying an OAuth Token ID gets first priority
            if kwargs.get('oauth_token_id'):
                print("[INFO] An OAuth Token ID was specified directly.")
                vcs_repo['oauth-token-id'] = kwargs.get('oauth_token_id')
            
            # explicitly specifying an OAuth Client (VCS Provider) Display Name gets second priority
            elif kwargs.get('oauth_client_name'):
                print("[INFO] An OAuth Client Display Name was specified directly.")
                oauth_client = oc.show(name=kwargs.get('oauth_client_name'))
                vcs_repo['oauth-token-id'] = oauth_client.json()['data']['relationships']['oauth-tokens']['data'][0]['id']
            
            # if neither are specified and there's only one OAuth Client in the Org just default to using that
            elif kwargs.get('oauth_token_id') is None and kwargs.get('oauth_client_name') is None and len(oc_list.json()['data']) == 1:
                print("[INFO] Detected '{}' is the only OAuth Client. Proceeding with using this one.".format(oc_display_name))
                vcs_repo['oauth-token-id'] = ot_id
            
            # if neither are specified and there's multiple OAuth Clients in the Org,
            # print a warning but default to the first OAuth Client returned in the list
            elif kwargs.get('oauth_token_id') is None and kwargs.get('oauth_client_name') is None and len(oc_list.json()['data']) > 1:
                print("[WARNING] Detected multiple OAuth Clients exist but a specific one was not specified.".format(self.org))
                print("[INFO] Proceeding with using '{}' OAuth Client because it was first in the list.".format(oc_display_name))
                vcs_repo['oauth-token-id'] = ot_id
            else:
                print("[ERROR] An unknown error occured determining which OAuth Client and/or OAuth Token ID to use.")
                exit
        else:
            print("[INFO] No VCS repo identifier specified. Proceeding to Workspace creation without VCS integration.")
        
        if len(vcs_repo) > 0:
            attributes['vcs-repo'] = vcs_repo
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.post(url=self.workspaces_endpoint, payload=payload)

    def update(self, name=None, **kwargs):
        """
        PATCH /organizations/:organization_name/workspaces/:name
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        vcs_repo = {}
        if kwargs.get('new_name'):
            attributes['name'] = kwargs.get('new_name')
            kwargs.pop('new_name')
        for key, value in kwargs.items():
            if key in self.ws_attributes_list:
                attributes[key] = value
            elif key in self.ws_vcs_attributes_list:
                vcs_repo[key] = value
            else:
                print("[WARNING] '{}' is an invalid key for Workspaces API.".format(key))
        if len(vcs_repo) > 0:
            attributes['vcs-repo'] = vcs_repo
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.patch(url='/'.join([self.workspaces_endpoint, name]),
                                           payload=payload)

    def list(self):
        """
        GET /organizations/:organization_name/workspaces
        """
        return self.client._requestor.get(url=self.workspaces_endpoint)

    def show(self, name=None):
        """
        GET /organizations/:organization_name/workspaces/:name
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        return self.client._requestor.get(url='/'.join([self.workspaces_endpoint, name]))

    def delete(self, name=None):
        """
        DELETE /organizations/:organization_name/workspaces/:name
        """
        if name is None:
            raise MissingWorkspace
        
        return self.client._requestor.delete(url='/'.join([self.workspaces_endpoint, name]))

    def lock(self, name=None, **kwargs):
        """
        POST /workspaces/:workspace_id/actions/lock
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        ws_id = self._get_ws_id(name=name)
        reason = kwargs.pop('reason', 'Locked by pytfc')
        payload = { 'reason': reason }
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
                                          'workspaces', ws_id, 'actions', 'lock']),
                                          payload=payload)

    def unlock(self, name=None):
        """
        POST /workspaces/:workspace_id/actions/unlock
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        ws_id = self._get_ws_id(name=name)
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
                                          'workspaces', ws_id, 'actions', 'unlock']))

    def force_unlock(self, name=None):
        """
        POST /workspaces/:workspace_id/actions/force-unlock
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        ws_id = self._get_ws_id(name=name)
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
                                          'workspaces', ws_id, 'actions', 'force-unlock']))

    def assign_ssh_key(self, ssh_key_id, name=None):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        ws_id = self._get_ws_id(name=name)
        
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        attributes['id'] = ssh_key_id
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.patch(url='/'.join([self.client._base_uri_v2,
                                           'workspaces', ws_id, 'relationships',
                                           'ssh-key']), payload=payload)

    def unassign_ssh_key(self, name=None):
        """
        PATCH /workspaces/:workspace_id/relationships/ssh-key
        """
        if name is None:
            if self.client.ws:
                name = self.client.ws
            else:
              raise MissingWorkspace
        
        ws_id = self._get_ws_id(name=name)
        
        payload = {}
        data = {}
        data['type'] = 'workspaces'
        attributes = {}
        attributes['id'] = 'null'
        data['attributes'] = attributes
        payload['data'] = data
        
        return self.client._requestor.patch(url='/'.join([self.client._base_uri_v2,
                                           'workspaces', ws_id, 'relationships',
                                           'ssh-key']), payload=payload)