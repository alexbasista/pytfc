"""TFC/E Policy Checks API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import InvalidQueryParam


class PolicyChecks(TfcApiBase):
    """
    TFC/E Policy Checks methods.
    """
    def list(self, run_id, page_number=None, page_size=None):
        """
        GET /runs/:run_id/policy-checks
        """
        path = f'/runs/{run_id}/policy-checks'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)
    
    def show(self, polchk_id, include=None):
        """
        GET /policy-checks/:id
        """
        if include is not None:
            if include not in ['run', 'run.workspace']:
                raise InvalidQueryParam

        path = f'/policy-checks/{polchk_id}'
        return self._requestor.get(path=path, include=include)
    
    def override(self, polchk_id):
        """
        POST /policy-checks/:id/actions/override
        """
        path = f'/policy-checks/{polchk_id}/actions/override'
        return self._requestor.post(path=path, payload=None)

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
        path = f'/policy-set-outcomes/{pso_id}'
        return self._requestor.get(path=path)