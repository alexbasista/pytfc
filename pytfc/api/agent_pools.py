"""TFC/E Agent Pools API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import InvalidQueryParam


class AgentPools(TfcApiBase):
    """
    TFC/E State Versions methods.
    """
    def list(self, include=None):
        """
        GET /organizations/:organization_name/agent-pools
        """
        if include is not None:
            if include != 'workspaces':
                raise InvalidQueryParam
        
        path = f'/organizations/{self.org}/agent-pools'
        return self._requestor.get(path=path, include=include)
    
    def list_agents(self, agent_pool_id):
        """
        GET /agent-pools/:agent_pool_id/agents
        """
        print('coming soon')

    def show(self, agent_pool_id, include=None):
        """
        GET /agent-pools/:id
        """
        if include is not None:
            if include != 'workspaces':
                raise InvalidQueryParam            
        
        path = f'/agent-pools/{agent_pool_id}'
        return self._requestor.get(path=path, include=include)

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
        path = f'/agent-pools/{agent_pool_id}'
        ap = self._requestor.get(path=path)

        ws_list = []
        for ws in ap.json()['data']['relationships']['workspaces']['data']:
            ws_list.append(ws['id'])
        
        return ws_list
