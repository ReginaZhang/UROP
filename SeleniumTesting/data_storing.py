'''
Created on 09/12/2014

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

class DataStoring():
    
    __metaclass__ = ABCMeta
    
    @unittest.skip("Skip to save time.")
    def test_4a_import_url(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["import_url"] % ("https://swift.rc.nectar.org.au:8888/v1/AUTH_f0d7c5b248004e80ae6f6afa8452d70c/UROP/file_to_share.txt?temp_url_sig=d6a4c505714369893ecd918e213083dd6bf033ea&temp_url_expires=1418200269")
        try:
            self.send_request(function, "import_url()")
        except Exception as e:
            raise ImportURLException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh()
        except AssertionError:
            raise ImportURLException(response)
    
    @unittest.skip("Not finished.")
    def test_4b_drag_and_drop(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["drag_and_drop"]
        try:
            self.send_request(function, "drag_and_drop()")
        except Exception as e:
            raise DragAndDropException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh()
        except AssertionError:
            raise DragAndDropException(response)
        
    