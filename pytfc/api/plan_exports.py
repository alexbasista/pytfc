"""TFC/E Plan Exports API endpoints module."""
import requests
import tarfile
from time import sleep
from pytfc.tfc_api_base import TfcApiBase
from pytfc.exceptions import MissingPlan, PlanExportDownloadError
from .plans import Plans

class PlanExports(TfcApiBase):
    """
    TFC/E Plan Exports methods.
    """
    def get_plan_export_id(self, plan_id):
        """
        Helper method to return Plan Export ID based on `plan_id`.
        
        Returns `None` if one does not exist.
        """
        plans_client = Plans(
            self._requestor,
            self.org,
            self.ws,
            self.ws_id,
            self.log_level
        )
        plan = plans_client.show(plan_id=plan_id).json()
        del plans_client

        if plan['data']['relationships']['exports']['data'] == []:
            self._logger.info(\
                f"Did not detect Plan Export on Plan `{plan_id}`.")
            pe_id = None
        else:
            pe_id = plan['data']['relationships']['exports']['data'][0]['id']

        return pe_id
            
    def get_download_url(self, pe_id):
        """
        GET /plan-exports/:id/download
        """
        path = f'/plan-exports/{pe_id}/download'
        return self._requestor.get(path=path).url
    
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

        pe = self._requestor.post(path='/plan-exports', payload=payload)
        return pe

    def show(self, pe_id):
        """
        GET /plan-exports/:id
        """
        path = f'/plan-exports/{pe_id}'
        return self._requestor.get(path=path)

    def _extract_tarball(self, filepath, dest_folder):
        tarball = tarfile.open(filepath, 'r:gz')
        tarball.extractall(dest_folder)
        tarball.close()
    
    def download(self, pe_id=None, plan_id=None, dest_folder='./',
                 tarball_prefix=None, extract=True):
        """
        Utility method to download and optionally extract a Sentinel
        Mock (Plan Export) tarball based on either Plan Export ID
        (`pe_id`) or Plan ID (`plan_id`). If a Plan Export does not
        already exist on the Plan ID specified, one will be created.

        Returns path of tarball downloaded as a string.
        """
        if pe_id is not None:
            pe_id = pe_id
        elif plan_id is not None:
            plan_id = plan_id
            pe_id = self.get_plan_export_id(plan_id=plan_id)
        else:
            self._logger.error(\
                "Either `pe_id` or `plan_id` is required.")
            raise MissingPlan

        if pe_id is None:
            self._logger.info(f"Creating new Plan Export.")
            new_pe = self.create(plan_id=plan_id)
            pe_id = new_pe.json()['data']['id']
            self._logger.info(f"Created Plan Export `{pe_id}`.")
        else:
            pe_id = pe_id
        
        pe_dl_url = self.get_download_url(pe_id=pe_id)
        pe_bytes_data = requests.get(url=pe_dl_url, stream=True).content
        retry_count = 0
        while len(pe_bytes_data) == 0:
            self._logger.debug("Detected Plan Export download from"
                               f" `{pe_id}` was empty. Retrying...")
            sleep(1)
            pe_bytes_data = requests.get(url=pe_dl_url, stream=True).content
            retry_count += 1
            if retry_count == 60:
                self._logger.error(f"Exceeded max download retries on `{pe_id}`.")
                raise PlanExportDownloadError
        self._logger.debug(f"Downloaded Plan Export `{pe_id}`.")

        if tarball_prefix is not None:
            filename = tarball_prefix + '-sentinel-mocks.tar.gz'
        else:
            filename = pe_id + '-sentinel-mocks.tar.gz'

        if dest_folder == './':
            dest_path = dest_folder + filename
        else:
            dest_path = dest_folder + '/' + filename

        with open(dest_path, 'wb') as file:
            file.write(pe_bytes_data)
        self._logger.debug(f"Created archive `{dest_path}`.")

        if extract:
            self._logger.debug(f"Extracting tarball from `{dest_path}`.")
            self._extract_tarball(filepath=dest_path, dest_folder=dest_folder)
            self._logger.debug(f"Extracted archive `{dest_path}`.")

        return dest_path
    
    def delete(self, pe_id):
        """
        DELETE /plan-exports/:id
        """
        path = f'/plan-exports/{pe_id}'
        return self._requestor.delete(path=path)



        