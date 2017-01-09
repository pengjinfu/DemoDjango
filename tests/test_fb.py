import unittest
from facebookads.api import FacebookAdsApi
from facebookads import objects
import json

class TestFBMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertNotEqual(1,0);

    # 可以连接FB的
    def test_fb(self):
        try:
            config_file = open('./autogen_docs_config.json')
        except IOError:
            print("No config file found, skipping docs tests")
            exit()
        config = json.load(config_file)
        my_app_id = config['app_id']
        my_app_secret = config['app_secret']
        my_access_token = config['access_token']
        FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
        self.assertIsNotNone(FacebookAdsApi.API_VERSION);
        me = objects.AdUser(fbid='me')
        my_accounts = list(me.get_ad_accounts())
        self.assertGreater(len(my_accounts),0,'账号数大于0个')
        config_file.close()


if __name__ == '__main__':
    unittest.main()