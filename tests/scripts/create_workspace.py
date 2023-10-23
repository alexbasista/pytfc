import os
import time
import argparse
import pytfc
import gitlab
import json

TFE_HOSTNAME = os.getenv('TFE_HOSTNAME', 'app.terraform.io')
TFE_TOKEN = os.getenv('TFE_TOKEN')
TFE_ORG = os.getenv('TFE_ORG')

GL_URL = os.getenv('GL_URL', 'https://gitlab.com')
GL_TOKEN = os.getenv('GL_TOKEN')
GL_PROJECT_ID = os.getenv('GL_PROJECT_ID')


def py_dict_to_hcl_map(py_dict):
    """
    Utility function to convert a Python
    dictionary to an HCL map.
    """
    max_key_length = max(len(k) for k in py_dict.keys())
    hcl_map = ["{"]
    
    for k, v in py_dict.items():
        kv_spacing = max_key_length - len(k) + 1
        if isinstance(v, str):
            fmt_val = f'"{v}"' if not v.startswith('"') else v
        else:
            fmt_val = v
        hcl_map.append(f'  {k}{" " * kv_spacing}= {fmt_val}')
    hcl_map.append("}")

    return "\n".join(hcl_map)

def inject_tfvars(template_path, vars):
    """
    Utility function to inject the input variable values
    into the terraform.tfvars.tpl template file.
    """
    tfvars_rendered = []
    max_key_length = max(len(key) for key in vars.keys())

    with open(template_path, 'r') as input_file:
        for line in input_file:
            parts = line.split('=')
            if len(parts) == 2:
                key = parts[0].strip()
                value = vars.get(key, None)
                
                if value is not None:
                    if isinstance(value, str):
                        fmt_line = f'{key.ljust(max_key_length)} = "{value}"\n'
                        tfvars_rendered.append(fmt_line)
                    elif isinstance(value, int):
                        fmt_line = f'{key.ljust(max_key_length)} = {value}\n'
                        tfvars_rendered.append(fmt_line)
                    elif isinstance(value, list):
                        value_str = f"{value}"
                        fmt_line = f'{key.ljust(max_key_length)} = {value_str}\n'
                        tfvars_rendered.append(fmt_line)
                    elif isinstance(value, dict):
                        hcl_map = py_dict_to_hcl_map(value)
                        fmt_line = f'{key.ljust(max_key_length)} = {hcl_map}\n'
                        tfvars_rendered.append(fmt_line)
                    else:
                        print(f"Unexpected format: {type(value)}:")
                        print(value)
                        print("Skipping this variable.")
    
    return ''.join(tfvars_rendered)

def gl_file_create(gl_project, content, dst_path):
    """
    Utility function to create and commit a file in GitLab.
    """
    folder_name = os.path.basename(os.path.dirname(dst_path))
    try:
        gl_project.files.create(
            {
                'file_path': dst_path,
                'branch': 'main',
                'content': content,
                'commit_message': f"Creating new '{folder_name}' config."
            }
        )
    except gitlab.exceptions.GitlabCreateError as e:
        print(f"An exception occurred creating the new directory: {e}")
        exit()

def gitlab_stuff(gl_client, gl_project_id, templates_dir, folder_name, input_vars):
    """
    Function to create new folder in existing GitLab project.
    """
    gl_project = gl_client.projects.get(gl_project_id)
    src_main_tf_path = f'{templates_dir}/main.tf'
    dst_main_tf_path = f'{folder_name}/main.tf'
    src_tfvars_path = f'{templates_dir}/template.tfvars.tpl'
    dst_tfvars_path = f'{folder_name}/terraform.auto.tfvars'
    
    print("[gl] Injecting variable values into new TFVARS file...")
    tfvars_rendered = inject_tfvars(src_tfvars_path, input_vars)

    print("[gl] Creating new folder and TF files in repo...")
    gl_file_create(gl_project, open(src_main_tf_path, 'r').read(), dst_main_tf_path) # main.tf
    gl_file_create(gl_project, tfvars_rendered, dst_tfvars_path) # terraform.auto.tfvars

def tfc_ws_create(tfc_client, name, project_name, vcs_repo, oauth_token_id, working_dir, varset_name, outputs):
    """
    Function to create new TFC Workspace,
    trigger a Terraform plan/apply,
    and return any outputs specified.
    """
    is_vcs_workflow = True if vcs_repo is not None else False
    project_id = tfc_client.projects.get_project_id(name=project_name)
    working_dir = name if working_dir is None else working_dir
    # TODO:
    # Determine if workflow is VCS-driven or API-driven
    # before creating Workspace.
    print(f"[tfc] Creating workspace '{name}'...")
    ws = tfc_client.workspaces.create(
        name = name,
        project_id = project_id,
        identifier = vcs_repo,
        oauth_token_id = oauth_token_id,
        working_directory = working_dir
    )
    ws_id = ws.json()['data']['id']

    if varset_name is not None:
        print("[tfc] Fetching variable set ID...")
        varset_id = tfc_client.variable_sets.get_varset_id(name=varset_name)
        print("[tfc] Applying variable set to workspace...")
        tfc_client.variable_sets.apply_to_workspace(varset_id=varset_id, ws_id=ws_id)

    # TODO:
    # API-driven workflow logic would go here
    
    # create Run safely after varset assignment to Workspace
    script_name = os.path.basename(__file__)
    run = tfc_client.runs.create(ws_id=ws_id, message=f'Triggered by {script_name}.')
    run_id = run.json()['data']['id']

    # while True:
    #     try:
    #         run_id = tfc_client.runs.get_latest_run_id(ws_id=ws_id)
    #         break
    #     except IndexError:
    #         print("[tfc] Waiting for run to start...")
    #         time.sleep(2)
    
    while True:
        plan_status = tfc_client.runs.show(run_id=run_id).json()['data']['attributes']['status']
        if plan_status == 'planned' or plan_status == 'planned_and_finished' or plan_status == 'policy_checked':
            break
        elif plan_status == 'errored':
            print(f"[tfc] Plan errored. Exiting.")
            exit()
        print(f"[tfc] Waiting for plan to finish... {plan_status}")
        # TODO: add timeout value and logic
        time.sleep(5)
    
    tfc_client.runs.apply(run_id=run_id, comment=f'Triggered by {script_name}.')
    while True:
        apply_status = tfc_client.runs.show(run_id=run_id).json()['data']['attributes']['status']
        if apply_status == 'applied' or apply_status == 'planned_and_finished':
            break
        elif apply_status == 'errored':
            print(f"[tfc] Apply errored. Exiting.")
            exit()
        print(f"[tfc] Waiting for apply to finish... {apply_status}")
        # TODO: add timeout value and logic
        time.sleep(5)
    
    if outputs is not None:
        outputs_list = [item.strip(',') for item in outputs]
        while True:
            try:
                current_state = tfc_client.state_versions.get_current(ws_id=ws_id).json()
                if current_state['data']['attributes']['resources-processed'] == True:
                    break
                print("[tfc] Waiting for outputs to be processed...")
            except Exception as e:
                if str(e).startswith('404 tfc_client Error: Not Found for url:'):
                    time.sleep(2)
                else:
                    print(f"[tfc] An unexpected exception occurred: {e}")
                    print("[tfc] Exiting script.")
                    exit()

        sv_id = current_state['data']['id']
        sv_outputs = tfc_client.state_version_outputs.list(sv_id=sv_id).json()
        outputs_data = {}
        for i in sv_outputs['data']:
            if i['attributes']['name'] in outputs_list:
                outputs_data[i['attributes']['name']] = i['attributes']['value']

        if outputs_data:
            print("[tfc] Printing outputs:")
            print(outputs_data)
        
        return outputs_data

def parse_args():
    parser = argparse.ArgumentParser(
        description='TFC Workspace creation and GitLab file creation arguments.')
    parser.add_argument('--name', dest='name',
        help='Name of Workspace to create in TFC.'),
    parser.add_argument('--project-name', dest='project_name', default='Default Project',
        help='Name of TFC Project to place Workspace in.'),
    parser.add_argument('--vcs-repo', dest='vcs_repo', default=None,
        help='Reference to VCS repository in format of :org/:repo.'),
    parser.add_argument('--oauth-token-id', dest='oauth_token_id', default=None,
        help='OAuth Token ID of VCS provider connection in TFC.'),
    parser.add_argument('--working-dir', dest='working_dir', default=None,
        help='Directory in repo that TFC Workspace should be linked to.'),
    parser.add_argument('--varset-name', dest='varset_name', default=None,
        help='Name of TFC Variable Set to apply to Workspace.'),
    parser.add_argument('--templates-dir', dest='templates_dir', default='./templates',
        help='Name of directory where Terraform templates reside.')
    parser.add_argument('--var', nargs='+', action='append', metavar=('key', 'value'),
        default=None, help='User-defined Terraform input variable values.'),
    parser.add_argument('--outputs', nargs='+', dest='outputs', default=None,
        help='List of Terraform outputs to return after the apply.')
    args = parser.parse_args()
    
    return args

def main():
    args = parse_args()

    input_vars = {}
    if args.var is not None:
        for var in args.var:
            key, value = var
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
            input_vars[key] = value
    else:
        input_vars = None

    tfc_client = pytfc.Client(hostname=TFE_HOSTNAME, token=TFE_TOKEN, org=TFE_ORG, log_level='debug')
    gl_client = gitlab.Gitlab(url=GL_URL, private_token=GL_TOKEN)
    
    gitlab_stuff(
        gl_client=gl_client,
        gl_project_id=GL_PROJECT_ID,
        templates_dir=args.templates_dir,
        folder_name=args.name,
        input_vars=input_vars
    )
    
    tfc_ws_create(
        tfc_client=tfc_client,
        name=args.name,
        project_name=args.project_name,
        vcs_repo=args.vcs_repo,
        oauth_token_id=args.oauth_token_id,
        working_dir=args.working_dir,
        varset_name=args.varset_name,
        outputs=args.outputs
    )

if __name__ == "__main__":
    main()