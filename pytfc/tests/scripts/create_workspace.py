import os
import argparse
import pytfc

TFE_HOSTNAME = os.getenv('TFE_HOSTNAME', 'app.terraform.io')
TFE_TOKEN = os.getenv('TFE_TOKEN')
TFE_ORG = os.getenv('TFE_ORG')


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
    parser.add_argument('--working-directory', dest='working_directory',
        help='Directory in repo that Workspace should be linked to.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    client = pytfc.Client(hostname=TFE_HOSTNAME, token=TFE_TOKEN, org=TFE_ORG)

    project_id = client.projects.get_project_id(name=args.project_name)

    new_ws = client.workspaces.create(
        name = args.name,
        project_id = project_id,
        identifier = args.vcs_repo,
        oauth_token_id = args.oauth_token_id
    )

if __name__ == "__main__":
    main()