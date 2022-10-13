"""
Module for TFC/E Configuration Versions endpoint.
"""
import os
import time
import tarfile
import requests
from datetime import datetime
from .exceptions import MissingWorkspace
from .exceptions import ConfigurationVersionUploadError


class ConfigurationVersions(object):
    """
    TFC/E Configuration Version methods.
    """
    def __init__(self, client, **kwargs):
        self.client = client
        self._logger = client._logger
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
            self._ws_id = self.client.workspaces._get_ws_id(name=self.ws)
        else:
            if self.client.ws:
                self.ws = self.client.ws
                self._ws_id = self.client._ws_id
            else:
                raise MissingWorkspace

        self._cv_endpoint = '/'.join([self.client._base_uri_v2, 'workspaces',
                                      self._ws_id, 'configuration-versions'])

    def list(self):
        """
        GET /workspaces/:workspace_id/configuration-versions
        """
        return self.client._requestor.get(url=self._cv_endpoint)

    def _get_latest_cv_id(self):
        """
        Helper method that returns latest Configuration Version ID in Workspace.
        """
        return self.list().json()['data'][0]['id']

    def show(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        return self.client._requestor.get(url="/".join([self.client._base_uri_v2,
                                                        'configuration-versions', cv_id]))

    def show_commit(self, cv_id):
        """
        GET /configuration-versions/:configuration-id/ingress-attributes
        """
        return self.client._requestor.get(url="/".join([self.client._base_uri_v2,
                                                        'configuration-versions',
                                                        cv_id, 'ingress-attributes']))

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

    def create(self, auto_queue_runs='true', speculative='false', **kwargs):
        """
        POST /workspaces/:workspace_id/configuration-versions
        
        Only returns Configuration Version `upload-url`.
        """
        if auto_queue_runs not in ['true', 'false']:
            raise ValueError("[ERROR] Invalid argument for 'auto_queue_runs'. Valid arguments: 'true' or 'false'.")
        
        if speculative not in ['true', 'false']:
            raise ValueError("[ERROR] Invalid argument for 'speculative'. Valid arguments: 'true' or 'false'.")

        payload = {}
        data = {}
        data['type'] = 'configuration-versions'
        attributes = {}
        attributes['auto-queue-runs'] = auto_queue_runs
        attributes['speculative'] = speculative
        data['attributes'] = attributes
        payload['data'] = data

        if kwargs.get('ws_id'):
            url = '/'.join([self.client._base_uri_v2, 'workspaces', kwargs.get('ws_id'), 'configuration-versions'])
            cv_object = self.client._requestor.post(url=url, payload=payload)
        else:
            cv_object = self.client._requestor.post(url=self._cv_endpoint, payload=payload)
        
        return cv_object

    def _create_tf_tarball(self, source_dir, dest_dir='./'):
        """
        Helper method to create tarball of Terraform files from specified path.
        Configuration Version API requires tar.gz file format for upload.
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
            self._logger.exception(e)
            raise

    def upload(self, cv_upload_url, tf_tarball):
        """
        PUT https://archivist.<TFC/E HOSTNAME>/v1/object/<UNIQUE OBJECT ID>
        """
        try:
            resp = requests.put(url=cv_upload_url, data=tf_tarball)
            resp.raise_for_status()
            return resp.status_code
        except Exception as e:
            raise ConfigurationVersionUploadError("[ERROR] Exception occurred uploading Terraform configuration bundle to archivist: {}".format(e))
    
    def _cleanup_tf_tarball(self, path):
        if os.path.exists(path):
            os.remove(path)
        else:
            self._logger.warning(f"`{path}` path not found.")
            pass
    
    def create_and_upload(self,  source_tf_dir, dest_tf_dir='./',
                          auto_queue_runs='true', speculative='false', **kwargs):
        """
        Method that wraps multiple other methods to more easily create
        and upload a Configuration Version in a Workspace in one call.
        Returns newly created Configuration Version ID.
        """
        # 1. Create CV and return upload-url
        cv_object = self.create(auto_queue_runs=auto_queue_runs, speculative=speculative)
        cv_id=cv_object.json()['data']['id']
        cv_upload_url = cv_object.json()['data']['attributes']['upload-url']
        self._logger.info(f"Created Configuration Version `{cv_id}`")
        
        # 2. Create tarball of TF files
        tf_tarball = self._create_tf_tarball(source_dir=source_tf_dir, dest_dir=dest_tf_dir)
        self._logger.info(f"Created Terraform tarball `{tf_tarball}`.")
        
        # 3. Upload tarball to CV
        with open(tf_tarball, 'rb') as tf_tarball_upload:
            self.upload(cv_upload_url=cv_upload_url, tf_tarball=tf_tarball_upload)
        self._logger.info(f"Uploaded Terraform tarball `{tf_tarball}`.")

        # 4. Check Configuration Version status
        cv_status = self._get_cv_status(cv_id=cv_id)
        self._logger.info(f"Checking for 'uploaded' Configuration Version status: `{cv_status}`.")
        while cv_status != 'uploaded':
            if self._get_cv_status(cv_id=cv_id) == 'uploaded':
                break
            else:
                cv_status = self._get_cv_status(cv_id=cv_id)
                self._logger.info(f"Checking for 'uploaded' Configuration Version status: {cv_status}")
                time.sleep(2)

        # 5. Cleanup
        if kwargs.get('cleanup', 'true'):
            self._logger.info(f"Deleting local Terraform tarball `{tf_tarball}`.")
            self._cleanup_tf_tarball(path=tf_tarball)

        return cv_id

