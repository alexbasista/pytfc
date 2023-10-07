import pytest


# --- create basic Workspace --- #
def test_create_workspace(client):
    name       = "pytest-create-workspace"
    project_id = "prj-ju6pfT7sp5gA84U4"

    response = client.workspaces.create(
        name=name,
        project_id=project_id
    )

    assert response.status_code == 201

    client.workspaces.delete(name=name)

# --- create Workspace with VCS --- #
def test_create_workspace_vcs(client, tfe_ghain):
    name       = "pytest-create-workspace-vcs"
    project_id = "prj-ju6pfT7sp5gA84U4"
    repo       = "alexbasista/terraform-random-thrones"
    ghain      = tfe_ghain

    response = client.workspaces.create(
        name=name,
        project_id=project_id,
        identifier=repo,
        github_app_installation_id=ghain
    )

    assert response.status_code == 201

    client.workspaces.delete(name=name)

# --- Update basic Workspace --- #
def test_update_worksace(client):
    ""

# --- Update Workspace with VCS --- #
def test_update_workspace_vcs(client):
    ""