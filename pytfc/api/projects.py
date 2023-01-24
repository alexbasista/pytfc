"""TFC/E Projects API endpoints module."""
from pytfc.tfc_api_base import TfcApiBase


class Projects(TfcApiBase):
    """
    TFC/E Projects methods.
    """
    def create(self, name):
        """
        POST /organizations/:organization_name/projects
        """
        payload = {}
        data = {}
        data['type'] = 'projects'
        attributes = {}
        attributes['name'] = name
        data['attributes'] = attributes
        payload['data'] = data

        path = f'/organizations/{self.org}/projects'
        return self._requestor.post(path=path, payload=payload)

    def update(self, project_id):
        """
        PATCH /projects/:project_id
        """
        print('coming soon')

    def list(self, page_number=None, page_size=None, query=None, filters=None):
        """
        GET /organizations/:organization_name/projects
        """
        path = f'/organizations/{self.org}/projects'
        return self._requestor.get(path=path, page_number=page_number,
                                   page_size=page_size, query=query,
                                   filters=filters)

    def show(self, project_id):
        """
        GET /projects/:project_id
        """
        path = f'/projects/{project_id}'
        return self._requestor.get(path=path)

    def delete(self, project_id):
        """
        DELETE /projects/:project_id
        """
        path = f'/projects/{project_id}'
        return self._requestor.delete(path=path)

    def get_project_id(self, name):
        """
        Helper method to return Project ID
        based on Project name.
        """
        project = self.list(query=name).json()
        if project['data'] == []:
            project_id = None
        else:
            project_id = project['data'][0]['id']
        
        return project_id