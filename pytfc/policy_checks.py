"""
Module for TFC/E Policy Checks API endpoint.
"""
from .exceptions import InvalidQueryParam


class PolicyChecks:
    """
    TFC/E Policy Checks methods.
    """
    def __init__(self, client):
        self.client = client

    def list(self, run_id, page_number=None, page_size=None):
        """
        GET /runs/:run_id/policy-checks
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'runs', run_id, 'policy-checks']),
            page_number=page_number, page_size=page_size)
    
    def show(self, polchk_id, include=None):
        """
        GET /policy-checks/:id
        """
        if include is not None:
            if include not in ['run', 'run.workspace']:
                raise InvalidQueryParam
        
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'policy-checks', polchk_id]),
            include=include)
    
    def override(self, polchk_id):
        """
        POST /policy-checks/:id/actions/override
        """
        return self.client._requestor.post(url='/'.join([
            self.client._base_uri_v2, 'policy-checks', polchk_id,
            'actions', 'override']))

    def show_outcome(self):
        """
        GET /policy-set-outcomes/:policy_set_outcome_id
        """
        print('coming soon')
    
    def list_policy_evals(self, page_number=None, page_size=None):
        """
        GET /task-stages/:task_stage_id/policy-evaluations

        Only available for OPA policies.
        """
        print('coming soon')

    def list_policy_outcomes(self, page_number=None, page_size=None):
        """
        GET /policy-evaluations/:policy_evaluation_id/policy-set-outcomes
        """
        print('coming soon')
    
    def show_policy_outcome(self, pso_id):
        """
        GET /policy-set-outcomes/:policy_set_outcome_id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'policy-set-outcomes', pso_id]))