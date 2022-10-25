"""
Module for TFC/E Configuration Versions API endpoint.
"""
import os
import time
import tarfile
import requests
from datetime import datetime
from .exceptions import MissingWorkspace
from .exceptions import ConfigurationVersionUploadError


class ConfigurationVersions:
    """
    TFC/E Configuration Version methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws_id'):
            self.ws_id = kwargs.get('ws_id')
            self.ws = self.client.workspaces.get_ws_name(ws_id=self.ws_id)
        elif kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self.ws_id = self.client.workspaces.get_ws_id(name=self.ws)
        elif self.client.ws and self.client.ws_id:
            self.ws = self.client.ws
            self.ws_id = self.client.ws_id
        else:
            self.ws = None
            self.ws_id = None

    def list(self, page_number=None, page_size=None, ws_id=None):
        """
        GET /workspaces/:workspace_id/configuration-versions
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.client._requestor.get(url='/'.join([self.client._base_uri_v2,
            'workspaces', ws_id, 'configuration-versions']),
            page_number=page_number, page_size=page_size)

    def _get_latest_cv_id(self, ws_id=None):
        """
        Helper method that returns latest Configuration 
        Version ID in Workspace.
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        return self.list(ws_id=ws_id).json()['data'][0]['id']

    def show(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2, 'configuration-versions', cv_id]))

    def show_commit_info(self, cv_id):
        """
        GET /configuration-versions/:configuration-id/ingress-attributes
        """
        return self.client._requestor.get(url='/'.join([
            self.client._base_uri_v2,'configuration-versions', cv_id,
            'ingress-attributes']))

    def _get_cv_status(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        cv_object = self.show(cv_id=cv_id)
        return cv_object.json()['data']['attributes']['status']

    def get_cv_upload_url(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        cv_object = self.show(cv_id=cv_id)
        return cv_object.json()['data']['attributes']['upload-url']

    def create(self, auto_queue_runs=True, speculative=False, ws_id=None):
        """
        POST /workspaces/:workspace_id/configuration-versions
        """
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace

        if not isinstance(auto_queue_runs, bool):
            self._logger.error(\
                "Invalid value for `auto_queue_runs`. Must provide a boolean.")
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
        
        return self.client._requestor.post(url='/'.join([self.client._base_uri_v2,
            'workspaces', ws_id, 'configuration-versions']), payload=payload)

    def _create_tf_tarball(self, source_dir, dest_dir='./'):
        """
        Helper method to create tarball of Terraform files from specified path.
        Configuration Versions API requires tar.gz file format for upload.
        """
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
            self._logger.error(\
                "Exception occurred uploading Terraform configuration bundle to archivist:")
            self._logger.error(e)
            raise ConfigurationVersionUploadError
    
    def _cleanup_tf_tarball(self, path):
        if os.path.exists(path):
            os.remove(path)
        else:
            self._logger.warning(f"`{path}` path not found.")
            pass
    
    def create_and_upload(self, source_tf_dir, dest_tf_dir='./',
            auto_queue_runs=True, speculative=False, cleanup=False,
            ws_id=None):
        """
        Method that wraps multiple other methods to more easily create
        and upload a Configuration Version in a Workspace in one call.
        
        Returns newly created Configuration Version ID.
        """
        # 0. Validate Workspace ID is present
        if ws_id is not None:
            ws_id = ws_id
        elif self.ws_id:
            ws_id = self.ws_id
        else:
            raise MissingWorkspace
        
        # 1. Create CV and return `upload-url`
        cv = self.create(auto_queue_runs=auto_queue_runs,
            speculative=speculative, ws_id=ws_id)
        cv_id=cv.json()['data']['id']
        cv_upload_url = cv.json()['data']['attributes']['upload-url']
        self._logger.info(f"Created Configuration Version `{cv_id}`")
        
        # 2. Create tarball of TF files
        tf_tarball = self._create_tf_tarball(source_dir=source_tf_dir, dest_dir=dest_tf_dir)
        self._logger.info(f"Created Terraform tarball `{tf_tarball}`.")
        
        # 3. Upload tarball to CV
        with open(tf_tarball, 'rb') as tf_tarball_upload:
            self.upload(cv_upload_url=cv_upload_url, tf_tarball=tf_tarball_upload)
        self._logger.info(f"Uploaded Terraform tarball `{tf_tarball}`.")

        # 4. Check CV status
        cv_status = self._get_cv_status(cv_id=cv_id)
        self._logger.info(\
            f"Checking for 'uploaded' Configuration Version status: `{cv_status}`.")
        while cv_status != 'uploaded':
            if self._get_cv_status(cv_id=cv_id) == 'uploaded':
                break
            else:
                cv_status = self._get_cv_status(cv_id=cv_id)
                self._logger.info(\
                    f"Checking for 'uploaded' Configuration Version status: {cv_status}")
                time.sleep(2)

        # 5. Cleanup
        if cleanup:
            self._logger.info(\
                f"Deleting local Terraform tarball `{tf_tarball}`.")
            self._cleanup_tf_tarball(path=tf_tarball)

        return cv_id

