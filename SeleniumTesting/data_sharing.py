'''
Module created on 08/12/2014

@author: Regina Zhang

'''

import unittest
from abc import ABCMeta
from GStestexceptions import *
from constants import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from _codecs import register
from selenium.webdriver.common.action_chains import ActionChains
import register_login as rl

class DataSharing():
    
    __metaclass__ = ABCMeta
    
    def test_5a_generate_public_URL(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["generate_public_url"]
        try:
            self.send_request(function, "generate_public_url()")
        except Exception as e:
            raise PublicURLException("Failed to generate public URL.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            time.sleep(2)
        except AssertionError:
            raise PublicURLException("Failed to generate public URL.\n" + response)
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            assert "Public URL" in alert.text
        except TimeoutException:
            raise PublicURLException("Failed to catch public URL pop-up.")
        except AssertionError:
            raise PublicURLException("Failed to get generated public URL.")
        try:
            public_url = alert.text.lstrip("Public URL: ")
            function = js_func["share_data"].format(public_url)
            self.send_request(function, "share_data()")
        except Exception as e:
            raise PublicURLException("Failed to share data using public URL generated.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise PublicURLException("Failed to share data using public URL generated.\n" + response)
        
        