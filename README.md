# pytfc
**pytfc** is an HTTP client library for the Terraform Cloud and Terraform Enterprise API.

```python
import pytfc
client = pytfc.Client(org='my-tfe-org')
client.workspaces.create(name='aws-base-vpc-dev')
client.set_ws(name='aws-base-vpc-dev')
client.workspace_variables.create(key='AWS_ACCESS_KEY_ID', value='ABCDEFGHIJKLMNOPQRST', category='env', sensitive='true')
client.workspace_variables.create(key='AWS_SECRET_ACCESS_KEY', value='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD', category='env', sensitive='true')
```
<p>&nbsp;</p>

## Usage
A _client_ object must be initialized with certain parameters. The parameters can be specified as environment variables or directly as function arguments. The only two parameters that are required at the time a client is initialized are the TFE hostname and an API token. Depending on what level you are working at, mainly Organization-level vs. Workspace-level, you can optionally set some of the other parameters either at the time the client is initialized or after the fact.

### Initializing a Client
With environment variables:
```
export TFE_HOSTNAME='tfe.whatever.com'
export TFE_TOKEN='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890'
```
```python
client = pytfc.Client(org='my-existing-tfe-org')
```

Directly as function arguments:
```python
client = pytfc.Client(hostname='tfe.whatever.com', token='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890', org='my-existing-tfe-org')
```

Setting the Organization and Workspace when a client is initialized:
```python
client = pytfc.Client(org='my-existing-tfe-org', ws='my-existing-tfe-ws')
```
> Assumes the TFE_HOSTNAME and TFE_TOKEN environment variables are set.

Setting the Organization and Workspace _after_ a client is initialized:
```python
client = pytfc.Client()
client.set_org(name='my-existing-tfe-org')
client.set_ws(name='my-existing-tfe-ws')
```
> Assumes the TFE_HOSTNAME and TFE_TOKEN environment variables are set.
<p>&nbsp;</p>







