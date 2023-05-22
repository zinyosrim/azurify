import os
import sys
import random
import re
import string
import logging

from typing import Protocol
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.resource import ResourceManagementClient

from azurify.azsecrets import AzSecretKeys
from azurify.azenv import AzEnv


@dataclass
class Secrets:
    secrets: dict()


@dataclass
class Secret:
    key: AzSecretKeys
    value: str


def resource_client(
    group_name: str = AzEnv.AZURE_DEFAULT_GROUP_NAME, location: str = AzEnv.AZURE_DEFAULT_LOCATION
) -> ResourceManagementClient:
    resource_client = ResourceManagementClient(
        credential = DefaultAzureCredential(),
        subscription_id = AzEnv.AZURE_SUBSCRIPTION_ID,
    )
    resource_client.resource_groups.create_or_update(group_name, {"location": location})
    return resource_client


def keyvault_client() -> KeyVaultManagementClient:
    return KeyVaultManagementClient(
        credential = DefaultAzureCredential(),
        subscription_id = AzEnv.AZURE_SUBSCRIPTION_ID,
    )


def shopify_store_name(shop_url: str) -> str:
    """Parse shop URL and return 1st part 

    Args:
        shop_url (str): xxx.myshopify.com URL

    Raises:
        ValueError: if structure not xxx.myshopify.com
        ValueError: if 1st part nor alphanumeric

    Returns:
        str: 1st part of URL
    """
    
    url_parts = shop_url.split(".")
    if len(url_parts) != 3 or url_parts[1] != "myshopify" or url_parts[2] != "com":
        raise ValueError(f"`{shop_url}` doesn't seem to be a Shopify URL. Must be `<name>.myshopify.com`.")

    store_name = url_parts[0]
    if re.match(store_name, "^[\w-_]+$") == False:
        raise ValueError(f"Can not create an Azure keyvault from the shop_url `{shop_url}`. Only alphanumeric and hyphens are allowed")

    return store_name


def generate_shopify_keyvault_name(shop_url: str) -> str:
    """Generate randomized name for keyvault of length 24

    Args:
        kv_name (str): desired name

    Returns:
        str: name with structure `kv-<name>-<random string>`eg. kv-aaaabbbb-mdgmbzynpbax 
    """
    kv_name = shopify_store_name(shop_url)

    # Create Azure compliant keyvault name. Shorten name if too long. Otherwise add random characters
    kv_name_length = len(kv_name)
    if kv_name_length > 20:
        return f"kv-{kv_name[:21]}"
    else:
        random_str_length = 20 - kv_name_length
        random_str = "".join(random.choices(string.ascii_lowercase, k=random_str_length))
        return f"kv-{kv_name[:kv_name_length]}-{random_str}"


class Tresor(Protocol):
    def create() -> None:
        ...

    def delete() -> None:
        ...


class Keyvault:
    def __init__(self, kv_name, keyvault_client=keyvault_client()):
        self.kv_name = kv_name
        self.keyvault_client = keyvault_client

    def create(self) -> None:
        self.keyvault_client.vaults.begin_create_or_update(
            AzEnv.AZURE_DEFAULT_GROUP_NAME,
            self.kv_name,
            {
                "location": AzEnv.AZURE_DEFAULT_LOCATION,
                "properties": {
                    "tenant_id": AzEnv.AZURE_TENANT_ID,
                    "sku": {"family": "A", "name": "standard"},
                    "access_policies": [
                        {
                            "tenant_id": AzEnv.AZURE_TENANT_ID,
                            "object_id": AzEnv.AZURE_DEFAULT_OBJECT_ID,
                            "permissions": {
                                "secrets": [
                                    "get",
                                    "list",
                                    "set",
                                    "delete",
                                    "purge",
                                ],
                            },
                        }
                    ],
                    "enabled_for_deployment": True,
                    "enabled_for_disk_encryption": True,
                    "enabled_for_template_deployment": True,
                },
            },
        ).result()

    @property
    def keyvault(self):
        return self.keyvault_client.vaults.get(AzEnv.AZURE_DEFAULT_GROUP_NAME, self.kv_name)

    def delete(self) -> None:
        self.keyvault_client.vaults.delete(AzEnv.AZURE_DEFAULT_GROUP_NAME, self.kv_name)


def main(shop_url: str) -> None:
    """Create a keyvault out of a Shopify URL

    Args:
        shop_url (str): e.g. myshop.myshopify.com
    """
    kv_name = generate_shopify_keyvault_name(shop_url)
    kv = Keyvault(kv_name=kv_name)
    kv.create()

    print(f"Created keyvault `https://{kv.keyvault.name}.vault.azure.net`in `{kv.keyvault.location}`.")
    logging.info(f"Created keyvault `https://{kv.keyvault.name}.vault.azure.net`in `{kv.keyvault.location}`.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2 and args[0] in ["-kv", "--kv", "-kvname", "--kvname", "-keyvault-name", "--keyvault-name"]:
        main(args[1])
    else:
        print("Keyvault not created! Usage: `python create_keyvault.py -kvname test`")