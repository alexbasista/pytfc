# pytfc
Python HTTP client library for the Terraform Cloud and Terraform Enterprise API.

```python
import pytfc
client = pytfc.Client(org='my-tfe-org')
client.workspaces.create(name='aws-base-vpc-dev')
client.set_ws(name='aws-base-vpc-dev')
client.workspace_variables.create(key='AWS_ACCESS_KEY_ID', value='ABCDEFGHIJKLMNOPQRST', category='env', sensitive='true')
client.workspace_variables.create(key='AWS_SECRET_ACCESS_KEY', value='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ABCD', category='env', sensitive='true')
```

## Usage
A _client_ object must be instantiated with certain parameters. The parameters can be specified as environment variables or directly as function arguments. The only parameter required at the time a client is instantiated is the API token. A hostname is also required if you are using TFE, and if a hostname is not specified it is assumed you are using TFC (`app.terraform.io`). Depending on what level you are working at, mainly Organization-level vs. Workspace-level, you can optionally set some of the other parameters either at the time the client is instantiated or after the fact.

### Instantiating a Client
With environment variables:
```python
os.environ['TFE_HOSTNAME']='tfe.whatever.com'
os.environ['TFE_TOKEN']='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890'

client = pytfc.Client(org='my-existing-tfe-org')
```

Directly as function arguments:
```python
client = pytfc.Client(hostname='tfe.whatever.com', token='abcdefghijklmn.atlasv1.opqrstuvwxyz012345678987654321abcdefghijklmnopqrstuvwxyz01234567890', org='my-existing-tfe-org')
```

Setting the Organization and Workspace when a client is instantiated:
```python
client = pytfc.Client(org='my-existing-tfe-org', ws='my-existing-tfe-ws')
```
> Assumes the TFE_HOSTNAME and TFE_TOKEN environment variables are set.

Setting the Organization and Workspace _after_ a client is instantiated:
```python
client = pytfc.Client()
client.set_org(name='my-existing-tfe-org')
client.set_ws(name='my-existing-tfe-ws')
```
> Assumes the TFE_HOSTNAME and TFE_TOKEN environment variables are set.

\
See the [docs](./docs/) for more details and examples on usage.
<p>&nbsp;</p>

---
> Note: this is repository is not officially supported or maintained by HashiCorp.
