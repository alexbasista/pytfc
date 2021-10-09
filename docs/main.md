# How To
The following sections display examples of how to use each API endpoint supported by **pytfc**.

## Organizations
```python
# List all Organizations
orgs = client.organizations.list()
orgs.json()

# Show an Organization
org = client.organizations.show(name='my-existing-tfe-org')
org.json()

# Create an Organization
client.organizations.create(name='my-new-tfe-org', email='tfe-admins@whatever.com', owners_team_saml_role_id='my-tfe-owners-team')

# Update an Organization
client.organizations.update(name='my-existing-tfe-org', owners_team_saml_role_id='new-tfe-owners-team')

# Destroy an Organization
client.organizations.delete(name='my-existing-tfe-org')

# Show the Entitlement Set
es = client.organizations.show_entitlement_set(name='my-existing-tfe-org')
es.json()
```


## Workspaces
```python
# Set the Org attribute on the client object
client.set_org(name='my-existing-tfe-org')

# List all Workspaces
workspaces = client.workspaces.list()
workspaces.json()

# Show a Workspace
ws = client.workspaces.show(name='my-existing-tfe-ws')
ws.json()

# Create a Workspace with no VCS repo
client.workspaces.create(name='my-new-tfe-ws')

# Create a Workspace with a VCS repo
client.workspaces.create(name='my-new-tfe-ws-dev', identifier='alexbasista/terraform-vcs-repo', working_directory='/dev')

# Update a Workspace
client.workspaces.update(name='my-existing-tfe-ws', terraform_version='0.13.5')

# Rename a Workspace
client.workspaces.update(name='my-existing-tfe-ws', new_name='my-existing-tfe-ws-2')

# Destroy a Workspace
client.workspaces.delete(name='my-existing-tfe-ws')

# Lock a Workspace
client.workspaces.lock(name='my-existing-tfe-ws')

# Unlock a Workspace
client.workspaces.unlock(name='my-existing-tfe-ws')

# Force unlock a Workspace
client.workspaces.force_unlock(name='my-existing-tfe-ws')

# Assign an SSH Key to a Workspace
client.workspaces.assign_ssh_key(name='my-existing-tfe-ws', ssh_key_id='sshkey-aBcDeFgHiJkLmNoP')

# Unassign an SSH Key from a Workspace
client.workspaces.unassign_ssh_key(name='my-existing-tfe-ws')
```


## Workspace Variables


## Configuration Versions


## Runs