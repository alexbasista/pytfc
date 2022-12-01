"""
TFE Admin Settings API endpoints module.
For Terraform Enterprise only.
"""
from pytfc.tfc_api_base import TfcApiBase


class AdminSettings(TfcApiBase):
    """
    TFE Admin Settings methods.
    """    
    def list_general(self):
        """
        GET /api/v2/admin/general-settings
        """
        return self._requestor.get(path='/admin/general-settings')

    def update(self, **kwargs):
        """
        PATCH /api/v2/admin/general-settings
        """
        print('coming soon')
    
    def list_cost_estimation(self):
        """
        GET /api/v2/admin/cost-estimation-settings
        """
        return self._requestor.get(path='/admin/cost-estimation-settings')
        
    def update_cost_estimation(self):
        """
        PATCH /api/v2/admin/cost-estimation-settings
        """
        print('coming soon')
    
    def list_saml(self):
        """
        GET /api/v2/admin/saml-settings
        """
        return self._requestor.get(path='/admin/saml-settings')

    def update_saml(self):
        """
        PATCH /api/v2/admin/saml-settings
        """
        print('coming soon')

    def revoke_saml_idp_cert(self):
        """
        POST /api/v2/admin/saml-settings/actions/revoke-old-certificate
        """
        print('coming soon')

    def list_smtp(self):
        """
        GET /api/v2/admin/smtp-settings
        """
        return self._requestor.get(path='/admin/smtp-settings')

    def update_smtp(self):
        """
        PATCH /api/v2/admin/smtp-settings
        """
        print('coming soon')

    def list_twilio(self):
        """
        GET /api/v2/admin/twilio-settings
        """
        return self._requestor.get(path='/admin/twilio-settings')
    
    def update_twilio(self):
        """
        PATCH /api/v2/admin/twilio-settings
        """
        print('coming soon')

    def verify_twilio(self):
        """
        POST /api/v2/admin/twilio-settings/verify
        """
        print('coming soon')

    def list_customization(self):
        """
        GET /api/v2/admin/customization-settings
        """
        return self._requestor.get(path='/admin/customization-settings')

    def update_customization(self):
        """
        PATCH /api/v2/admin/customization-settings
        """
        print('coming soon')