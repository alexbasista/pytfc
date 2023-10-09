def test_create_varset(client):
    ws_id_1 = client.workspaces.create(name='pytest-varsets-tmp-1').json()['data']['id']
    ws_id_2 = client.workspaces.create(name='pytest-varsets-tmp-2').json()['data']['id']
    
    vars_list = \
    [
        {'key': 'tst_var_1', 'value': 'tst_val_1',},
        {'key': 'tst_var_2', 'value': 'tst_val_2', 'sensitive': True},
        {'key': 'TST_VAR_3', 'value': 'tst_val_3', 'category': 'env'},
        {'key': 'TST_VAR_4', 'value': 'tst_val_4', 'category': 'env', 'sensitive': True}
    ]

    response = client.variable_sets.create(
        name='pytest-varset',
        workspace_ids = [ws_id_1, ws_id_2],
        vars = vars_list
    )
    
    client.workspaces.delete(name='pytest-varsets-tmp-1')
    client.workspaces.delete(name='pytest-varsets-tmp-2')
    varset_id = response.json()['data']['id']
    client.variable_sets.delete(varset_id=varset_id)
    
    assert response.status_code == 201

def test_apply_varset_to_ws(client):
    ws_name     = "pytest-apply-varset-to-ws"
    project_id  = "prj-ju6pfT7sp5gA84U4"
    varset_name = "pytest"

    ws_id = client.workspaces.create(name=ws_name, project_id=project_id).json()['data']['id']
    varset_id = client.variable_sets.get_varset_id(name=varset_name)
    response = client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)
    client.workspaces.delete(name=ws_name)

    assert response.status_code == 204

def test_remove_varset_to_ws(client):
    ws_name     = "pytest-remove-varset-from-ws"
    project_id  = "prj-ju6pfT7sp5gA84U4"
    varset_name = "pytest"

    ws_id = client.workspaces.create(name=ws_name, project_id=project_id).json()['data']['id']
    varset_id = client.variable_sets.get_varset_id(name=varset_name)
    client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)
    response = client.variable_sets.remove_from_workspace(varset_id=varset_id, ws_id=ws_id)
    client.workspaces.delete(name=ws_name)

    assert response.status_code == 204

def test_apply_varset_to_project(client):
    varset_id = client.variable_sets.create(name='pytest-vs-prj-tst-1').json()['data']['id']
    prj_id_1 = client.projects.create(name='pytest-prj-vs-tst-1').json()['data']['id']
    prj_id_2 = client.projects.create(name='pytest-prj-vs-tst-2').json()['data']['id']
    
    response = client.variable_sets.apply_to_project(
        varset_id=varset_id,
        project_ids=[prj_id_1, prj_id_2]
    )

    client.projects.delete(project_id=prj_id_1)
    client.projects.delete(project_id=prj_id_2)
    client.variable_sets.delete(varset_id=varset_id)
    
    assert response.status_code == 204

def test_remove_varset_from_project(client):
    varset_id = client.variable_sets.create(name='pytest-vs-prj-tst-2').json()['data']['id']
    prj_id_1 = client.projects.create(name='pytest-prj-tmp-3').json()['data']['id']
    prj_id_2 = client.projects.create(name='pytest-prj-tmp-4').json()['data']['id']
    
    client.variable_sets.apply_to_project(
        varset_id=varset_id,
        project_ids=[prj_id_1, prj_id_2]
    )
    
    response = client.variable_sets.remove_from_project(
        varset_id=varset_id,
        project_ids=[prj_id_1, prj_id_2]
    )

    client.projects.delete(project_id=prj_id_1)
    client.projects.delete(project_id=prj_id_2)
    client.variable_sets.delete(varset_id=varset_id)
   
    assert response.status_code == 204
