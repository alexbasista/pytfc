"""
Module for TFC/E Agent Pools API endpoint.
"""
from .exceptions import InvalidQueryParam


class AgentPools:
    """
    TFC/E State Versions methods.
    """
    def __init__(self, client):
        self.client = client

    def list(self, include=None):
        """
        GET /organizations/:organization_name/agent-pools
        """
        base_url = '/'.join([self.client._base_uri_v2, 'organizations',
            self.client.org, 'agent-pools'])

        if include is not None:
            if include != 'workspaces':
                raise InvalidQueryParam
        
        return self.client._requestor.get(url=base_url, include=include)
    
    def list_agents(self, agent_pool_id):
        """
        GET /agent-pools/:agent_pool_id/agents
        """
        print('coming soon')

    def show(self, agent_pool_id, include=None):
        """
        GET /agent-pools/:id
        """
        base_url = '/'.join([self.client._base_uri_v2, 'agent-pools',
            agent_pool_id])

        if include is not None:
            if include != 'workspaces':
                raise InvalidQueryParam            
        
        return self.client._requestor.get(url=base_url, include=include)

    def show_agent(self, agent_id):
        """
        GET /agent-pools/:id
        """
        print('coming soon')

    def delete_agent(self, agent_id):
        """
        DELETE /agents/:id
        """
        print('coming soon')

    def create(self, name, scope=True, ws_ids=None):
        """
        POST /organizations/:organization_name/agent-pools
        """
        print('coming soon')

    def update(self, **kwargs):
        """
        PATCH /agent-pools/:id
        """
        print('coming soon')
    
    def delete(self, agent_pool_id):
        """
        DELETE /agent-pools/:agent_pool_id
        """
        print('coming soon')

    def list_workspaces(self, agent_pool_id):
        """
        Utility method to list all Workspaces
        associated with an Agent Pool.
        """
        url = '/'.join([self.client._base_uri_v2, 'agent-pools',
            agent_pool_id])
        
        ap = self.client._requestor.get(url=url)

        ws_list = []
        for ws in ap.json()['data']['relationships']['workspaces']['data']:
            ws_list.append(ws['id'])
        
        return ws_list
