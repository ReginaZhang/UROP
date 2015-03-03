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
    
    #@unittest.skip("Skip to save time.")
    def test_4a_import_url(self):
        """
        The test for testing importing data using the public URL.
        
        The public URL is fixed to a certain URL at the moment.
        Need to change every two days.
        
        Skipped if the login test was failed.
        """
        if not rl.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        self.dismiss_dialogs()
        function = js_func["import_url"] % ("https://swift.rc.nectar.org.au:8888/v1/AUTH_f0d7c5b248004e80ae6f6afa8452d70c/UROP/subdir1%2Ffile_to_share.txt?temp_url_sig=86f1307755aec7340432f2467d5906e3c0511ca0&temp_url_expires=1418446695")
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
    
    #@unittest.skip("Skip to save time.")
    def test_4b_drag_and_drop(self):
        """
        The test for uploading functionality in GenomeSpace 
        using drag-and-drop method.
        This test is conducted by sending Http Request with
        file content as the request body to imitate the process.
        
        Skipped if the login test was failed.
        """
        if not rl.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        self.dismiss_dialogs()
        function = js_func["upload_file"] % test_file["file_to_upload_path"]
        try:
            self.send_request(function, "upload_file()")
        except Exception as e:
            raise DragAndDropException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
        except AssertionError:
            raise DragAndDropException("Failed at 'GET' request: " + response)
        try:
            time.sleep(2)
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise DragAndDropException("Failed at 'PUT' request: " + response)
        
    