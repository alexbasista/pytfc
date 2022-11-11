"""
Module for TFE Admin Settings API endpoints.
For Terraform Enterprise only.
"""


class AdminSettings:
    """
    TFE Admin Settings methods.
    """
    def __init__(self, client):
        self.client = client
        self._logger = client._logger
        self._base_endpoint = '/'.join([self.client._base_uri_v2, 'admin'])
    
    def list_general(self):
        """
        GET /api/v2/admin/general-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'general-settings']))

    def update(self, **kwargs):
        """
        PATCH /api/v2/admin/general-settings
        """
    
    def list_cost_estimation(self):
        """
        GET /api/v2/admin/cost-estimation-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'cost-estimation-settings']))
        
    def update_cost_estimation(self):
        """
        PATCH /api/v2/admin/cost-estimation-settings
        """
    
    def list_saml(self):
        """
        GET /api/v2/admin/saml-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'saml-settings']))

    def update_saml(self):
        """
        PATCH /api/v2/admin/saml-settings
        """
    
    def revoke_saml_idp_cert(self):
        """
        POST /api/v2/admin/saml-settings/actions/revoke-old-certificate
        """
    
    def list_smtp(self):
        """
        GET /api/v2/admin/smtp-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'smtp-settings']))

    def update_smtp(self):
        """
        PATCH /api/v2/admin/smtp-settings
        """
    
    def list_twilio(self):
        """
        GET /api/v2/admin/twilio-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'twilio-settings']))
    
    def update_twilio(self):
        """
        PATCH /api/v2/admin/twilio-settings
        """

    def verify_twilio(self):
        """
        POST /api/v2/admin/twilio-settings/verify
        """
    
    def list_customization(self):
        """
        GET /api/v2/admin/customization-settings
        """
        return self.client._requestor.get(url='/'.join([self._base_endpoint,
            'customization-settings']))

    def update_customization(self):
        """
        PATCH /api/v2/admin/customization-settings
        """