def test_create_run(client):
    ws_id = client.workspaces.get_ws_id(name='pytfc-pytest-stateful')
    response = client.runs.create(ws_id=ws_id, auto_apply=True)
    
    assert response.status_code == 201