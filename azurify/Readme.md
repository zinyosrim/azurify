# AZURIFY
Resource access library for Shopify Apps implemented as Azure Functions

## Installation
    mkdir <dir>
    cd <dir>
    python3 -m venv .venv
    source .venv/bin/activate
    pip install azurify

## Create your environment variables.
Required variables to run Azure functions in general:
    
    export AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    export AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    export AZURE_CLIENT_SECRET=xxxxxx-xxxxxxxxxxxx-xxxxxxxxxx-xxxxxxxx
    export AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    

Additionally create these:

    export AZURE_DEFAULT_GROUP_NAME=my-resources
    export AZURE_DEFAULT_OBJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    export AZURE_DEFAULT_LOCATION=uscentral

or run following Python script:

```python
import os

os.environ["AZURE_SUBSCRIPTION_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["AZURE_TENANT_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["AZURE_CLIENT_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
os.environ["AZURE_CLIENT_SECRET"] = "xxxxxx-xxxxxxxxxxxx-xxxxxxxxxx-xxxxxxxx"
os.environ["AZURE_DEFAULT_GROUP_NAME"] = "my-resources"
os.environ["AZURE_DEFAULT_LOCATION"] = "uscentral"
os.environ["AZURE_DEFAULT_OBJECT_ID"] = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

## Sample
```python
from azure.identity import DefaultAzureCredential

from azurify.azconverter import factory
from azurify.azsecrets import AzureSecrets
from azurify.azstorage import ObjectToStore, AzureBlobUploader


def main():
    """Simple test case"""

    my_data = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4},
        {"a": 5, "b": 6},
    ]
    print(f"my_data = {my_data}")

    my_converter = factory("csv")
    my_converted_data = my_converter.convert(my_data).data
    my_suffix = my_converter.convert(my_data).suffix
    print(f"my_converter = {my_converter}")
    print(f"my converted data: {my_converted_data}")
    print(f"my converted data's filetype: {my_suffix}")

    azsecrets = AzureSecrets(
        vault_url="https://kv-langerchen.vault.azure.net/",
        credential=DefaultAzureCredential(),
    )

    print(f"Checking Secrets access: azsecrets.SHOPDOMAIN = {azsecrets.SHOPDOMAIN}")

    my_ObjectToStore = ObjectToStore(
        object_name="mytestblob.csv",
        container_name="testcontainer",
        data_to_store=my_converted_data,
    )
    print(f"my_ObjectToStore: {my_ObjectToStore}")

    AzureBlobUploader(
        object_to_store=my_ObjectToStore, conn_str=azsecrets.AZSTORAGECONNSTR
    ).upload()


if __name__ == "__main__":
    main()
```
## Usage

### Create Keyvault

```python
from azurify.azkeyvault import Keyvault, generate_shopify_keyvault_name

shop_url = "mystore.myshopify.com"

# Generate a name including the 1st part of the URL + random characters
kv_name = generate_shopify_keyvault_name(shop_url)

kv = Keyvault(kv_name=kv_name)
kv.create()

print(f"Created keyvault `https://{kv.keyvault.name}.vault.azure.net`in `{kv.keyvault.location}`.")
```

### Get Keyvault Properties

```python
from azurify.azkeyvault import Keyvault, generate_shopify_keyvault_name
from azurify.azsecrets import AzureSecrets

shop_url = "mystore.myshopify.com"
kv_name = generate_shopify_keyvault_name(shop_url)
print(kv_name)
# kv-mystore-xxxxxxxxxxxxx
kv = Keyvault(kv_name=kv_name)

print(kv.keyvault)
# kv-mystore-xxxxxxxxxxxxx
```

### Create secrets from file

```python
"""content of mysecrets.json
{
    "SHOPDOMAIN": "mystore.myshopify.com",
    "APIVERSION": "2023-04",
    "APIACCESSTOKEN": "<api access token>",
    "APICLIENTSECRETKEY": "<api secret, starting with sh..>"
    "AZSTORAGECONNSTR": "<Azure storage connection string>"
}
"""

from azure.identity import DefaultAzureCredential
from azurify.azsecrets import AzureSecrets

vault_url = "https://kv-bingobongo-xhlfuyngyn.vault.azure.net"
secrets = AzureSecrets(vault_url = vault_url, credential=DefaultAzureCredential()
                        )
secrets.load_json("mysecrets.json")
```
    