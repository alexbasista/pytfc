"""
Module for TFC/E Configuration Versions endpoint.
"""
import os
import tarfile
import requests
from datetime import datetime
from pytfc.exceptions import MissingWorkspace
from pytfc.exceptions import ConfigurationVersionUploadError


class ConfigurationVersions(object):
    """
    TFC/E Configuration Version methods.
    """

    def __init__(self, client, **kwargs):
        self.client = client
        
        if kwargs.get('ws'):
            self.ws = kwargs.get('ws')
        else:
            if self.client.ws:
                self.ws = self.client.ws
            else:
                raise MissingWorkspace
        
        self._ws_id = self.client.workspaces._get_ws_id(self.ws)
        self._cv_endpoint = '/'.join([self.client._base_uri_v2, 'workspaces', self._ws_id, 'configuration-versions'])


    def list(self):
        """
        GET /workspaces/:workspace_id/configuration-versions
        """
        return self.client._requestor.get(url=self._cv_endpoint)

    
    def _get_latest_cv_id(self):
        """
        Helper method that returns latest Configuration Version ID in Workspace.
        """
        cv_list = self.list()
        return cv_list['data'][0]['id']


    def show(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        return self.client._requestor.get(url="/".join([self.client._base_uri_v2, 'configuration-versions', cv_id]))


    def get_cv_status(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        resp = self.client._requestor.get(url="/".join([self.client._base_uri_v2, 'configuration-versions', cv_id]))
        return resp['data']['attributes']['status']


    def get_cv_upload_url(self, cv_id):
        """
        GET /configuration-versions/:configuration-id
        """
        resp = self.client._requestor.get(url="/".join([self.client._base_uri_v2, 'configuration-versions', cv_id]))
        return resp['data']['attributes']['upload-url']


    def create(self, auto_queue_runs='true', speculative='false', **kwargs):
        """
        POST /workspaces/:workspace_id/configuration-versions
        """
        if auto_queue_runs not in ['true', 'false']:
            raise ValueError("ERROR: Invalid argument for 'auto_queue_runs'. Valid arguments: 'true' or 'false'.")
        
        if speculative not in ['true', 'false']:
            raise ValueError("ERROR: Invalid argument for 'speculative'. Valid arguments: 'true' or 'false'.")

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
            return self.client._requestor.post(url=url, payload=payload)
        else:
            return self.client._requestor.post(url=self._cv_endpoint, payload=payload)


    def _create_tf_tarfile(self, source, dest='./'):
        """
        Helper method that creates tarball of Terraform configuration from specified path.
        Configuration Version API requires tar.gz file format for upload.
        """
        if dest[-1] != '/':
            dest = dest + '/'
        
        now = datetime.now()
        timestamp = now.strftime("%m%d%Y_%H%M%S")
        tf_tarfile_out = 'tf_{}.tar.gz'.format(timestamp)
        
        try:
            with tarfile.open(dest + tf_tarfile_out, 'w:gz') as tar:
                tar.add(source, arcname=os.path.sep)
            
            return(dest + tf_tarfile_out)
        
        except Exception as e:
            print(e)
            raise
    

    def _cleanup_tf_tarfile(self, path):
        if os.path.exists(path):
            print("INFO: deleting temporary Terraform bundle {}".format(path))
            os.remove(path)
        else:
            print("WARNING: {} not found.".format(path))
            pass


    def upload(self, cv_upload_url, tf_tarfile):
        """
        PUT https://archivist.<TFC/E HOSTNAME>/v1/object/<UNIQUE OBJECT ID>
        """
        try:
            resp = requests.put(url=cv_upload_url, data=tf_tarfile)
            resp.raise_for_status()
            return resp.status_code
        except Exception as e:
            raise ConfigurationVersionUploadError("ERROR: Exception occurred uploading Terraform configuration bundle to archivist: {}".format(e))


    def cv_tf_plan(self, source, dest='./', auto_queue_runs='true', speculative='false', cleanup='true', **kwargs):
        """
        Wraps multiple Configuration Versions functions
        into a workflow to execute a remote Terraform Run
        """
        # create Terraform tar.gz
        tf_tar = self._create_tf_tarfile(source=source, dest=dest)
        
        # handle if Workspace (ws) argument explicitly specified
        if kwargs.get('ws'):
            ws_id = self.client.workspaces._get_ws_id(kwargs.get('ws'))
        else:
            ws_id = self._ws_id
        
        # create Configuration Version
        cv = self.create(ws_id=ws_id, auto_queue_runs=auto_queue_runs, speculative=speculative)
        cv_id = cv['data']['id']
        cv_upload_url = cv['data']['attributes']['upload-url']

        # get Configuration Version status
        cv_status = self.get_cv_status(cv_id=cv_id)
        print(cv_status)

        # upload Terraform tar.gz to Configuration Version
        with open(tf_tar, 'rb') as tf_upload:
            self.upload(cv_upload_url=cv_upload_url, tf_tarfile=tf_upload)

        # delete temporary Terraform tar.gz after upload
        if cleanup == 'true':
            self._cleanup_tf_tarfile(path=tf_tar)
        elif cleanup == 'false':
            print("INFO: skipping cleanup of {}".format(tf_tar))
        else:
            raise ValueError("ERROR: '{}' is an invalid argument for 'cleanup' parameter. Valid arguments: 'true' or 'false'.".format(cleanup))

        return cv_id

