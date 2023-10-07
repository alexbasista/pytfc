

def test_apply_varset_to_ws(client):
    ws_name     = "pytest-apply-varset-to-ws"
    project_id  = "prj-ju6pfT7sp5gA84U4"
    varset_name = "pytest"

    ws_id = client.workspaces.create(name=ws_name, project_id=project_id).json()['data']['id']
    varset_id = client.variable_sets.get_varset_id(name=varset_name)
    response = client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)

    assert response.status_code == 204
    print('after the assert')
    client.workspaces.delete(name=ws_name)

def test_remove_varset_to_ws(client):
    ws_name     = "pytest-remove-varset-from-ws"
    project_id  = "prj-ju6pfT7sp5gA84U4"
    varset_name = "pytest"

    ws_id = client.workspaces.create(name=ws_name, project_id=project_id).json()['data']['id']
    varset_id = client.variable_sets.get_varset_id(name=varset_name)
    client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)
    response = client.variable_sets.remove_from_workspace(varset_id=varset_id, ws_id=ws_id)

    assert response.status_code == 204
    print('after the assert')
    client.workspaces.delete(name=ws_name)