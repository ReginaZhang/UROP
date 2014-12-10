'''
Created on 10/12/2014

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

class DataToGVL():
    
    __metaclass__ = ABCMeta
    
    def test_7b_launch_with_file(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["launch_with_file"]
        try:
            self.send_request(function, "launch_with_file()")
        except Exception as e:
            raise LauchWithFileException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise LauchWithFileException(response)
        
        