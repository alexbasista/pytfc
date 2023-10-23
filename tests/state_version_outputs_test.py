import time

def test_list_sv_outputs(client, tfe_ghain):
    ws = client.workspaces.create(
        name='pytest-list-svo',
        project_id='prj-ju6pfT7sp5gA84U4',
        identifier='alexbasista/pytfc',
        github_app_installation_id=tfe_ghain,
        working_directory='tests/testdata',
        queue_all_runs = True,
        auto_apply = True,
        branch = 'f-state-version-outputs'
    )
    ws_id = ws.json()['data']['id']
    
    current_state = None
    while True:
        try:
            current_state = client.state_versions.get_current(ws_id=ws_id).json()
            if current_state['data']['attributes']['resources-processed'] == True:
                break
            print("Waiting for outputs to be processed...")
        except Exception as e:
            if str(e).startswith('404 Client Error: Not Found for url:'):
                time.sleep(2)
            else:
                print(f"An unexpected exception occurred: {e}")

    sv_id = current_state['data']['id']
    response = client.state_version_outputs.list(sv_id=sv_id)
    
    client.workspaces.delete(name='pytest-list-svo')
    
    assert response.status_code == 200
    assert response.json()['data'][0]['attributes']['name'] == 'test0'
    assert response.json()['data'][1]['attributes']['name'] == 'test1'

    