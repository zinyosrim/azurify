# Testing creation and deletion of an azure keyvault

import unittest
import random
import string

from azkeyvault import Keyvault, keyvault_client, generate_shopify_keyvault_name, shopify_store_name


class TestAzureKeyvault(unittest.TestCase):
    """Test creation an deletion of an azure keyvault

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        # create a random name for the keyvault
        random_str = "".join(random.choices(string.ascii_lowercase, k=10))
        self.kv_name = f"test-kv-{random_str}"
        # create keyvault_client and keyvault objects
        self.kv_client = keyvault_client()
        self.kv = Keyvault(kv_name=self.kv_name, keyvault_client=self.kv_client)

    def test_shopify_store_name(self):
        url = "mystore.myshopify.com"
        self.assertEqual(shopify_store_name(url), "mystore")
        url2 = "my-store.myshopify.com"
        self.assertEqual(shopify_store_name(url2), "my-store")
        url3 = "mystore.com"
        self.assertRaises(ValueError, shopify_store_name(url3))
        url4 = "my_store.myshopify.com"
        self.assertRaises(ValueError, shopify_store_name(url4))
        url5 = "mystore.myshopify.con"
        self.assertRaises(ValueError, shopify_store_name(url5))


    def test_generate_shopify_keyvault_name(self):
        kv_name = generate_shopify_keyvault_name("mystore.myshopify.com")
        self.assertEqual(kv_name[:11], "kv-mystore-")
        self.assertEqual(len(kv_name), 24)

    def test_keyvault_create(self):
        # create keyvault and check if it's lists in the azure keyvaults
        self.kv.create()
        kv_list = [kv.name for kv in self.kv_client.vaults.list()]
        self.assertIn(self.kv_name, kv_list)

    def test_keyvault_delete(self):
        # delete previously created keyvault and check if it's missing in the list of the azure keyvaults
        self.kv.delete()
        kv_list = [kv.name for kv in self.kv_client.vaults.list()]
        self.assertNotIn(self.kv_name, kv_list)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
