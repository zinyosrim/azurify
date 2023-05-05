# Azure resource access library for Shopify Apps
The motivation for this library arose out of a data analysis project for a Shopify 
Store.

This package allows easy access to some Azure resources, particullarly:

- create/delete a keyvault
- populate keyvault with Shopify relevant secrets
- read secrets
- convert `list[dict]` data to JSON, CSV and Excel
- store data in Azure blob

[The source for this project is available here][src].

## Sample usage

Install package with `pip install azurify`

create your environment variables:

    AZURE_DEFAULT_OBJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_CLIENT_SECRET=xxxxxx-xxxxxxxxxxxx-xxxxxxxxxx-xxxxxxxx
    AZURE_DEFAULT_GROUP_NAME=my-resources
    AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    AZURE_DEFAULT_LOCATION=uscentral

Run:

    from azure.identity import DefaultAzureCredential
    from azurify.azsecrets import AzureSecrets

    AZURE_KEYVAULT_NAME = "enter your keyvault name here"

    def main():
        """Simple test case"""
        azsecrets = AzureSecrets(
            vault_url=f"https://{AZURE_KEYVAULT_NAME}.vault.azure.net/",
            credential=DefaultAzureCredential(),
        )

        print(azsecrets.SHOPDOMAIN)


    if __name__ == "__main__":
        main()

Prints `myshop.myshopify.com`

## Package structure
```
.
├── LICENSE
├── Readme.md
├── azurify
│   ├── Readme.md
│   ├── __init__.py
│   ├── azconverter.py
│   ├── azkeyvault.py
│   ├── azsecrets.py
│   ├── azstorage.py
│   ├── test_azconverter.py
│   ├── test_azkeyvault.py
│   ├── test_azsecrets.py
│   └── test_azstorage.py
├── requirements.txt
├── run.py
└── setup.py
```
## Package creation
Assuming package resides in directory `azurify`.
First run `run.py`to check everthing is functioning.

### Creating the package
    cd azurify
    pip install wheel
    python3 setup.py bdist_wheel sdist


### Local testing
Directory structure:
```
.
├── azurify
└── testazurify
```
    cd testazurify
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ../azurify


### Upload to test repository
    cd ../azurify
    pip install twine
    twine check dist/*
    twine upload -r testpypi dist/*

[src]: https://github.com/zinyosrim/azurify
