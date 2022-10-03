# Examples
The following sections display examples of how to call each API endpoint that is supported by **pytfc**.

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
```python
# List Configuration Versions
client.configuration_versions.list().json()

# Show a Configuration Version
client.configuration_versions.show(cv_id='cv-abcdefghijklmnop').json()

# Show a Configuration Version's Commit Information
client.configuration_versions.show_commit(cv_id='cv-abcdefghijklmnop').json()

# Create and Upload a Configuration Version (returns Configuration Version ID)
# Requires 'ws_id' parameter if Workspace not already set
client.configuration_versions.create(source_tf_dir='./terraform/main', auto_queue_runs='false', speculative='false')
```


## Runs
```python

```

## Plans
```python
# Requires an Org and Workspace to be set (if they aren't already)
client.set_org(name='my-existing-tfe-org')
cilent.set_ws(name='my-existing-tfe-ws')

# Show a Plan by Plan ID
client.plans.show(plan_id='plan-abcdefghijklmnop').json()

# Show a Plan by Run ID
client.plans.show(run_id='run-abcdefghijklmnop').json()

# Show a Plan by latest Run
client.plans.show(run_id='latest').json()

# Show a Plan by Commit Message of Run
client.plans.show(commit_message='this is a commit message').json()

# Show JSON output of Plans
# Use the following method with any of the four parameters above
client.plans.get_json_output(...)
```


## Applies
```python
# Requires an Org and Workspace to be set (if they aren't already)
client.set_org(name='my-existing-tfe-org')
cilent.set_ws(name='my-existing-tfe-ws')

# Show an Apply
client.applies.show(apply_id='apply-abcdefghijklmnop')
```


## Plan Exports (Sentinel Mocks)
```python
# Requires an Org and Workspace to be set (if they aren't already)
client.set_org(name='my-existing-tfe-org')
cilent.set_ws(name='my-existing-tfe-ws')

# Download Sentinel mock data into specific directory
client.plan_exports.download(destination_folder='./sentinel/test/policy1')
```