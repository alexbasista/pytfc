"""
Module for TFC/E Plan Exports endpoint.
"""
import requests
import tarfile
from .exceptions import MissingWorkspace
from .exceptions import MissingRunId


class PlanExports(object):
    """
    TFC/E Plan Exports methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
        else:
            if self.client.ws:
                self.ws = self.client.ws
            else:
                raise MissingWorkspace

        self.plan_exports_endpoint = '/'.join([self.client._base_uri_v2, 'plan-exports'])
    
    def _get_plan_export_id(self, **kwargs):
        if kwargs.get('plan_id'):
            plan_object = self.client.plans.show(plan_id=kwargs.get('plan_id'))
        else:
            plan_object = self.client.plans.show(run_id='latest')
        
        if plan_object.json()['data']['relationships']['exports']['data'] == []:
            pe_id = None
        else:
            pe_id = plan_object.json()['data']['relationships']['exports']['data'][0]['id']
        
        return pe_id
            
    def _get_download_url(self, plan_export_id):
        """
        GET /plan-exports/:id/download
        """
        return self.client._requestor.get(url='/'.join([self.plan_exports_endpoint, plan_export_id, 'download'])).url
    
    def create(self, **kwargs):
        """
        POST /plan-exports
        """
        if kwargs.get('plan_id'):
            plan_id = self.client.plans.show(plan_id=kwargs.get('plan_id')).json()['data']['id']
        else:
            plan_id = self.client.plans._get_plan_id(run_id='latest')

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

        pe_object = self.client._requestor.post(url=self.plan_exports_endpoint, payload=payload)
        self._logger.info(f"Plan Export `{pe_object.json()['data']['id']}` has been created.")
        return pe_object

    def show(self, **kwargs):
        """
        GET /plan-exports/:id
        """
        if kwargs.get('plan_export_id'):
            pe_object = self.client._requestor.get(url='/'.join([self.plan_exports_endpoint,
                                                    kwargs.get('plan_export_id')]))
        elif self._get_plan_export_id() is None:
            self._logger.info("Plan Export ID not found in Plan.")
            self._logger.info("Plan Export must be created for Plan first.")
            pe_object = None
        else:
            self._logger.info(f"Found Plan Export ID `{self._get_plan_export_id()}`.")
            pe_object = self.client._requestor.get(url='/'.join([self.plan_exports_endpoint,
                                                                self._get_plan_export_id()]))
        
        return pe_object
    
    def _get_run_id_from_pe(self, pe_id):
        plan_id = self.show(plan_export_id=pe_id).json()['data']['relationships']['plan']['data']['id']
        
        runs_list = self.client.runs.list()
        for run in runs_list.json()['data']:
            if run['type'] == "runs" and run['relationships']['plan']['data']['id'] == plan_id:
                return run['id']
            else:
                raise MissingRunId
    
    def _extract_tarball(self, filepath, destination_folder):
        tarball = tarfile.open(filepath, 'r:gz')
        tarball.extractall(destination_folder)
        tarball.close()
    
    def download(self, destination_folder='./', **kwargs):
        """
        GET /plan-exports/:id/download
        """
        if kwargs.get('plan_export_id'):
            plan_export_id = kwargs.get('plan_export_id')
        elif kwargs.get('plan_id'):
            plan_id = kwargs.get('plan_id')
            plan_export_id = self._get_plan_export_id(plan_id=plan_id)
        else:
            plan_id = self.client.plans._get_plan_id(run_id='latest')
            plan_export_id = self._get_plan_export_id(plan_id=plan_id)

        if plan_export_id is None:
            pe_object = self.create(plan_id=plan_id)
            pe_id = pe_object.json()['data']['id']
            self._logger.info(f"Created Plan Export `{pe_id}`.")
        else:
            pe_id = plan_export_id
        
        data = requests.get(url=self._get_download_url(plan_export_id=pe_id))
        self._logger.info(f"Downloaded Plan Export `{pe_id}`.")

        run_id = self._get_run_id_from_pe(pe_id=pe_id)

        filename = run_id + '-sentinel-mocks.tar.gz'
        if destination_folder == './':
            destination_path = destination_folder + filename
        else:
            destination_path = destination_folder + '/' + filename

        with open(destination_path, 'wb') as file:
            file.write(data.content)
        self._logger.info(f"Created archive `{destination_path}`.")

        self._extract_tarball(filepath=destination_path, destination_folder=destination_folder)
        self._logger.info(f"Extracted archive `{destination_path}`.")

    


        