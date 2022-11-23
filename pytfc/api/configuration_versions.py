"""TFC/E Configuration Versions API endpoints module."""
import os
import time
import tarfile
import requests
from datetime import datetime
from pytfc.tfc_api_base import TfcApiBase
from pytfc.utils import validate_ws_id_is_set
from pytfc.exceptions import ConfigurationVersionUploadError


class ConfigurationVersions(TfcApiBase):
    """
    TFC/E Configuration Version methods.
    """
    @validate_ws_id_is_set
    def list(self, ws_id=None, page_number=None, page_size=None):
        """
        GET /workspaces/:workspace_id/configuration-versions
        """
        ws_id = ws_id if ws_id else self.ws_id
        path = f'/workspaces/{ws_id}/configuration-versions'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size)

    @validate_ws_id_is_set
    def _get_latest_cv_id(self, ws_id=None):
        """
        Helper method that returns latest Configuration 
        Version ID in Workspace.
        """
        ws_id = ws_id if ws_id else self.ws_id
        return self.list(ws_id=ws_id).json()['data'][0]['id']

    def show(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        path = f'/configuration-versions/{cv_id}'
        return self._requestor.get(path=path)

    def show_commit_info(self, cv_id):
        """
        GET /configuration-versions/:configuration-id/ingress-attributes
        """
        path = f'/configuration-versions/{cv_id}/ingress-attributes'
        return self._requestor.get(path=path)

    def get_cv_status(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        cv = self.show(cv_id=cv_id)
        return cv.json()['data']['attributes']['status']

    def get_cv_upload_url(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        try:
            cv_upload_url = self.show(cv_id=cv_id).json()\
                ['data']['attributes']['upload-url']
        except KeyError:
            self._logger.warning("Did not find `upload-url` in Config Version."
                                 " The status may already be 'uploaded'.")
            cv_upload_url = None
        
        return cv_upload_url

    @validate_ws_id_is_set
    def create(self, ws_id=None, auto_queue_runs=True, speculative=False):
        """
        POST /workspaces/:workspace_id/configuration-versions
        """
        ws_id = ws_id if ws_id else self.ws_id
        
        if not isinstance(auto_queue_runs, bool):
            self._logger.error("Invalid value for `auto_queue_runs`."
                               " Must provide a boolean.")
            raise ValueError
        
        if not isinstance(speculative, bool):
            self._logger.error(\
                "Invalid value for `speculative`. Must provide a boolean.")
            raise ValueError

        payload = {}
        data = {}
        data['type'] = 'configuration-versions'
        attributes = {}
        attributes['auto-queue-runs'] = auto_queue_runs
        attributes['speculative'] = speculative
        data['attributes'] = attributes
        payload['data'] = data
        
        path = f'/workspaces/{ws_id}/configuration-versions'
        return self._requestor.post(path=path, payload=payload)

    def _create_tf_tarball(self, source_dir, dest_dir='./'):
        """
        Helper method to create tarball of Terraform files from specified path.
        Configuration Versions API requires tar.gz file format for upload.
        """
        if not os.path.exists(source_dir):
            self._logger.error(f"Path `{source_dir}` not found.")
            raise FileExistsError
        
        if dest_dir[-1] != '/':
            dest_dir = dest_dir + '/'
        
        now = datetime.now()
        timestamp = now.strftime("%m%d%Y_%H%M%S")
        tf_tarfile_out = 'tf_{}.tar.gz'.format(timestamp)
        
        try:
            with tarfile.open(dest_dir + tf_tarfile_out, 'w:gz') as tar:
                tar.add(source_dir, arcname=os.path.sep)
            return(dest_dir + tf_tarfile_out)
        except Exception as e:
            self._logger.error(e)
            raise

    def upload(self, cv_upload_url, tf_tarball):
        """
        PUT https://archivist.<TFC/E HOSTNAME>/v1/object/<UNIQUE_OBJECT_ID>
        """
        try:
            resp = requests.put(url=cv_upload_url, data=tf_tarball)
            resp.raise_for_status()
            return resp.status_code
        except Exception as e:
            self._logger.error("Exception occurred uploading Terraform"
                               " configuration bundle to archivist:")
            self._logger.error(e)
            raise ConfigurationVersionUploadError
    
    def _cleanup_tf_tarball(self, path):
        if os.path.exists(path):
            os.remove(path)
        else:
            self._logger.warning(f"Path `{path}` not found.")
            pass
    
    @validate_ws_id_is_set
    def create_and_upload(self, source_tf_dir, dest_tf_dir='./',
                          auto_queue_runs=True, speculative=False,
                          cleanup=False, ws_id=None):
        """
        Method that wraps multiple other methods to more easily create
        and upload a Configuration Version in a Workspace in one call.
        
        Returns newly created Configuration Version ID.
        """
        # 0. Validate Workspace ID is present
        ws_id = ws_id if ws_id else self.ws_id

        # 1. Create Config Version and return its `upload-url`
        cv = self.create(auto_queue_runs=auto_queue_runs,
            speculative=speculative, ws_id=ws_id)
        cv_id=cv.json()['data']['id']
        cv_upload_url = cv.json()['data']['attributes']['upload-url']
        self._logger.debug(f"Created Configuration Version `{cv_id}`.")
        
        # 2. Create tarball of Terraform files
        tf_tarball = self._create_tf_tarball(source_dir=source_tf_dir,
                                             dest_dir=dest_tf_dir)
        self._logger.debug(f"Created Terraform tarball `{tf_tarball}`.")
        
        # 3. Upload Terraform tarball to Config Version
        with open(tf_tarball, 'rb') as tf_tarball_upload:
            self.upload(cv_upload_url=cv_upload_url,
                        tf_tarball=tf_tarball_upload)
        self._logger.debug(f"Uploaded Terraform tarball `{tf_tarball}`.")

        # 4. Check Config Version status
        cv_status = self.get_cv_status(cv_id=cv_id)
        self._logger.debug(f"Checking for 'uploaded' Config Version status.")
        while cv_status != 'uploaded':
            if self.get_cv_status(cv_id=cv_id) == 'uploaded':
                break
            else:
                cv_status = self.get_cv_status(cv_id=cv_id)
                self._logger.debug(f"Current Config Version status: `{cv_status}`")
                time.sleep(2)

        # 5. Cleanup
        if cleanup:
            self._logger.debug(\
                f"Deleting local Terraform tarball `{tf_tarball}`.")
            self._cleanup_tf_tarball(path=tf_tarball)
        else:
            self._logger.debug(\
                f"Did not cleanup local Terraform tarball `{tf_tarball}`.")
        
        return cv_id

