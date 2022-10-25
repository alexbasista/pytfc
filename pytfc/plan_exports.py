"""
Module for TFC/E Plan Exports API endpoint.
"""
import requests
import tarfile
from. exceptions import MissingPlan


class PlanExports:
    """
    TFC/E Plan Exports methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger

        self.pe_endpoint = '/'.join([self.client._base_uri_v2, 'plan-exports'])

    def _get_plan_export_id(self, plan_id):
        """
        Helper method to return Plan Export ID
        based on `plan_id` arg specified.

        Returns `None` if one does not exist.
        """
        plan = self.client.plans.show(plan_id=plan_id)

        if plan.json()['data']['relationships']['exports']['data'] == []:
            self._logger.info(\
                f"Did not detect Plan Export on Plan `{plan_id}`.")
            pe_id = None
        else:
            pe_id = plan.json()['data']['relationships']['exports']['data'][0]['id']

        return pe_id
            
    def _get_download_url(self, pe_id):
        """
        GET /plan-exports/:id/download
        """
        return self.client._requestor.get(url='/'.join([
            self.pe_endpoint, pe_id, 'download'])).url
    
    def create(self, plan_id):
        """
        POST /plan-exports
        """
        payload = {}
        data = {}
        data['type'] = 'plan-exports'
        attributes = {}
        attributes['data-type'] = 'sentinel-mock-bundle-v0'
        data['attributes'] = attributes
        relationships = {}
        plan = {}
        plan_data = {}
        plan_data['id'] = plan_id
        plan_data['type'] = 'plans'
        plan['data'] = plan_data
        relationships['plan'] = plan
        data['relationships'] = relationships
        payload['data'] = data

        pe = self.client._requestor.post(url=self.pe_endpoint, payload=payload)
        self._logger.info(\
            f"Plan Export `{pe.json()['data']['id']}` has been created.")

        return pe

    def show(self, pe_id):
        """
        GET /plan-exports/:id
        """
        return self.client._requestor.get(url='/'.join([self.pe_endpoint, pe_id]))

    def _extract_tarball(self, filepath, dest_folder):
        tarball = tarfile.open(filepath, 'r:gz')
        tarball.extractall(dest_folder)
        tarball.close()
    
    def download(self, pe_id=None, plan_id=None, dest_folder='./',
            tarball_prefix=None):
        """
        GET /plan-exports/:id/download
        """
        if pe_id is not None:
            pe_id = pe_id
        elif plan_id is not None:
            plan_id = plan_id
            pe_id = self._get_plan_export_id(plan_id=plan_id)
        else:
            self._logger.error(\
                "Either `pe_id` or `plan_id` must be specified.")
            raise MissingPlan

        if pe_id is None:
            self._logger.info(f"Did not detect Plan Export on Plan.")
            new_pe = self.create(plan_id=plan_id)
            pe_id = new_pe.json()['data']['id']
            self._logger.info(f"Created Plan Export `{pe_id}`.")
        else:
            pe_id = pe_id
        
        data = requests.get(url=self._get_download_url(pe_id=pe_id))
        self._logger.info(f"Downloaded Plan Export `{pe_id}`.")

        # Remove dependency of Workspace name or ID? Yes for now.
        #run_id = self._get_run_id_from_pe(pe_id=pe_id)

        # Use Run ID or Plan Export ID in file name?
        # (if user does not pass `tarball_prefix` arg)
        # Plan Export ID is much easier for now.
        if tarball_prefix is not None:
            filename = tarball_prefix + '-sentinel-mocks.tar.gz'
        else:
            filename = pe_id + '-sentinel-mocks.tar.gz'

        if dest_folder == './':
            dest_path = dest_folder + filename
        else:
            dest_path = dest_folder + '/' + filename

        with open(dest_path, 'wb') as file:
            file.write(data.content)
        self._logger.info(f"Created archive `{dest_path}`.")

        self._extract_tarball(filepath=dest_path, dest_folder=dest_folder)
        self._logger.info(f"Extracted archive `{dest_path}`.")
    
    def delete(self, pe_id):
        """
        DELETE /plan-exports/:id
        """
        return self.client._requestor.delete(url='/'.join([
            self.pe_endpoint, pe_id]))
    


        