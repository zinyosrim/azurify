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
