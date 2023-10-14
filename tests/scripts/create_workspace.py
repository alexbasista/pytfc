import os
import time
import argparse
import pytfc

TFE_HOSTNAME = os.getenv('TFE_HOSTNAME', 'app.terraform.io')
TFE_TOKEN = os.getenv('TFE_TOKEN')
TFE_ORG = os.getenv('TFE_ORG')

def handle_list_input(arg):
    return [item.strip() for item in arg.split(',')]

def parse_args():
    parser = argparse.ArgumentParser(description='Workspace creation arguments.')
    parser.add_argument('--name', dest='name',
        help='Name of Workspace to create.'),
    parser.add_argument('--project-name', dest='project_name',
        help='Name of Project to place Workspace in.'),
    parser.add_argument('--vcs-repo', dest='vcs_repo',
        help='Reference to VCS repository in format of :org/:repo.'),
    parser.add_argument('--oauth-token-id', dest='oauth_token_id',
        help='OAuth Token ID from VCS provider connection in TFC.'),
    parser.add_argument('--working-directory', dest='working_directory', default=None,
        help='Directory in repo that Workspace should be linked to.'),
    parser.add_argument('--varset-name', dest='varset_name', default=None,
        help='Name of Variable Set to apply to Workspace.')
    parser.add_argument('--outputs', nargs='+', dest='outputs', default=None,
        help='List of outputs to return after the apply.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    client = pytfc.Client(hostname=TFE_HOSTNAME, token=TFE_TOKEN, org=TFE_ORG)

    project_id = client.projects.get_project_id(name=args.project_name)

    print(f"Creating workspace `{args.name}`...")
    ws = client.workspaces.create(
        name = args.name,
        project_id = project_id,
        identifier = args.vcs_repo,
        oauth_token_id = args.oauth_token_id,
        working_directory = args.working_directory,
        queue_all_runs = True
    )
    ws_id = ws.json()['data']['id']

    if args.varset_name is not None:
        print("Fetching variable set ID...")
        varset_id = client.variable_sets.get_varset_id(name=args.varset_name)
        print("Applying variable set to workspace...")
        client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)

    while True:
        try:
            run_id = client.runs.get_latest_run_id(ws_id=ws_id)
            break
        except IndexError:
            print("Waiting for run to start...")
            time.sleep(2)
    
    while True:
        plan_status = client.runs.show(run_id=run_id).json()['data']['attributes']['status']
        if plan_status == 'planned':
            break
        print("Waiting for plan to finish...")
        time.sleep(5)
    
    client.runs.apply(run_id=run_id)
    while True:
        apply_status = client.runs.show(run_id=run_id).json()['data']['attributes']['status']
        if apply_status == 'applied':
            break
        print("Waiting for apply to finish...")
        time.sleep(5)
    
    if args.outputs is not None:
        outputs_list = [item.strip(',') for item in args.outputs]
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
                    print("Exiting script.")
                    exit()

        sv_id = current_state['data']['id']
        sv_outputs = client.state_version_outputs.list(sv_id=sv_id).json()
        outputs_data = {}
        for i in sv_outputs['data']:
            if i['attributes']['name'] in outputs_list:
                outputs_data[i['attributes']['name']] = i['attributes']['value']

        return outputs_data

if __name__ == "__main__":
    main()