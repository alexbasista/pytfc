

def test_create_workspace(client):
    response = client.workspaces.create(
        name='pytest-create-workspace',
        project_id='prj-ju6pfT7sp5gA84U4'
    )
    client.workspaces.delete(name='pytest-create-workspace')
    assert response.status_code == 201

def test_delete_workspace(client):
    client.workspaces.create(
        name='pytest-delete-workspace',
        project_id='prj-ju6pfT7sp5gA84U4'
    )
    response = client.workspaces.delete(name='pytest-delete-workspace')
    assert response.status_code == 204

def test_create_workspace_vcs(client, tfe_ghain):
    response = client.workspaces.create(
        name='pytest-create-workspace-vcs',
        project_id='prj-ju6pfT7sp5gA84U4',
        identifier='alexbasista/terraform-random-thrones',
        github_app_installation_id=tfe_ghain
    )
    client.workspaces.delete(name='pytest-create-workspace-vcs')
    assert response.status_code == 201
