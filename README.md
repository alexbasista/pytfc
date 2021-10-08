# pytfc
**pytfc** is an HTTP client library for the Terraform Cloud and Terraform Enterprise API.

```python
>>> import pytfc
>>> client = pytfc.Client(org='my-tfe-org')
>>> client.workspaces.create(name='aws-base-vpc-dev')
>>> client.set_ws(name='aws-base-vpc-dev')
>>> client.workspace_variables.create(key='AWS_ACCESS_KEY_ID', value='ABCDEFGHIJKLMNOPQRST', category='env', sensitive='true')
>>> client.workspace_variables.create(key='AWS_SECRET_ACCESS_KEY', value='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD', category='env', sensitive='true')
```

**pytfc** is intended to be imported into build, configuration, or deployment scripts to simplify and enhance workflows that interact with Terraform Cloud or Terraform Enterprise. It can also be used interactively in the REPL for local development/testing scenarios. All CRUD operations exposed within the API are supported.
<p>&nbsp;</p>


## Install
**pytfc** is available on PyPI:
```
$ python -m pip install pytfc
```
<p>&nbsp;</p>


## Usage
In order to use **pytfc** a _client_ object must be initialized with certain parameters. The parameters can be specified as environment variables. The only two parameters that are required at the time a _client_ is initialized are the TFE hostname and an API token. Depending on what level you are working at, mainly Organization-level vs. Workspace-level, you can optionally set some of the other parameters either at the time the _client_ is initialized or after the fact.

### Initializing a Client
With environment variables:
```
export TFE_HOSTNAME='tfe.whatever.com'
export TFE_TOKEN='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890'
```
```python
>>> import pytfc
>>> client = pytfc.Client(org='my-existing-tfe-org')
```

Without environment variables:
```python
>>> import pytfc
>>> client = pytfc.Client(hostname='tfe.whatever.com', token='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890', org='my-existing-tfe-org')
```

Setting the Organization and Workspace when the _client_ is instantiated:
```python
>>> import pytfc
>>> client = pytfc.Client(org='my-existing-tfe-org', ws='my-existing-tfe-ws')
```

Setting the Organization and Workspace **after** the _client_ is instantiated:
```python
>>> import pytfc
>>> client = pytfc.Client()
>>> client.set_org(name='my-existing-tfe-org')
>>> client.set_ws(name='my-existing-tfe-ws')
```
<p>&nbsp;</p>

In the following sections and examples, it is assumed that a _client_ has already been initialized like so:
```
export TFE_HOSTNAME='tfe.whatever.com'
export TFE_TOKEN='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890'
```
```python
>>> import pytfc
>>> client = pytfc.Client()
```
<p>&nbsp;</p>

### Organizations

```python
# List all Organizations
>>> orgs = client.organizations.list()
>>> orgs.json()

# Show an Organization
>>> org = client.organizations.show(name='my-existing-tfe-org')
>>> org.json()

# Create an Organization
>>> client.organizations.create(name='my-new-tfe-org', email='tfe-admins@whatever.com', owners_team_saml_role_id='my-tfe-owners-team')

# Update an Organization
>>> client.organizations.update(name='my-existing-tfe-org', owners_team_saml_role_id='new-tfe-owners-team')

# Destroy an Organization
>>> client.organizations.delete(name='my-existing-tfe-org')

# Show the Entitlement Set
>>> es = client.organizations.show_entitlement_set(name='my-existing-tfe-org')
>>> es.json()
```
<p>&nbsp;</p>

### Workspaces
```python
# Set the Org attribute on the client object
>>> client.set_org(name='my-existing-tfe-org')

# List all Workspaces
>>> workspaces = client.workspaces.list()
>>> workspaces.json()

# Show a Workspace
>>> ws = client.workspaces.show(name='my-existing-tfe-ws')
>>> ws.json()

# Create a Workspace with no VCS repo
>>> client.workspaces.create(name='my-new-tfe-ws')

# Create a Workspace with a VCS repo
>>> client.workspaces.create(name='my-new-tfe-ws-dev', identifier='alexbasista/terraform-vcs-repo', working_directory='/dev')

# Update a Workspace
>>> client.workspaces.update(name='my-existing-tfe-ws', terraform_version='0.13.5')

# Rename a Workspace
>>> client.workspaces.update(name='my-existing-tfe-ws', new_name='my-existing-tfe-ws-2')

# Destroy a Workspace
>>> client.workspaces.delete(name='my-existing-tfe-ws')

# Lock a Workspace
>>> client.workspaces.lock(name='my-existing-tfe-ws')

# Unlock a Workspace
>>> client.workspaces.unlock(name='my-existing-tfe-ws')

# Force unlock a Workspace
>>> client.workspaces.force_unlock(name='my-existing-tfe-ws')

# Assign an SSH Key to a Workspace
>>> client.workspaces.assign_ssh_key(name='my-existing-tfe-ws', ssh_key_id='sshkey-aBcDeFgHiJkLmNoP')

# Unassign an SSH Key from a Workspace
>>> client.workspaces.unassign_ssh_key(name='my-existing-tfe-ws')
```
<p>&nbsp;</p>

### Workspace Variables

### Runs





