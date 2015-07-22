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
#import register_login as rl
#import mount_disconnect as md

from genome_space_test import GenomeSpaceTest

class DataStoring(GenomeSpaceTest):
    
    __metaclass__ = ABCMeta
    
    #@unittest.skip("Skip to save time.")
    def test_4a_import_url(self):
        """
        The test for testing importing data using the public URL.
        
        The public URL is fixed to a certain URL at the moment.
        Need to change every two days.
        
        Skipped if the login test was failed.
        """
        if (not GenomeSpaceTest.logged_in) or (not GenomeSpaceTest.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        self.dismiss_dialogs()
        function = js_func["import_url"] % (container_one["container"],"https://swift.rc.nectar.org.au:8888/v1/AUTH_f0d7c5b248004e80ae6f6afa8452d70c/UROP/subdir1%2Ffile_to_share.txt?temp_url_sig=86f1307755aec7340432f2467d5906e3c0511ca0&temp_url_expires=1418446695")
        try:
            self.send_request(function, "import_url()")
        except Exception as e:
            raise ImportURLException(e.__str__())
        try:
            response = self.get_response()
            assert "Failure" in response
            assert "Malformed url" in response
            self.refresh_page()
        except AssertionError:
            raise ImportURLException(response)
    
    #@unittest.skip("problem. Skip to save time.")
    def test_4b_upload_file(self):
        """
        The test for uploading functionality in GenomeSpace 
        using drag-and-drop method.
        This test is conducted by sending Http Request with
        file content as the request body to imitate the process.
        
        Skipped if the login test was failed.
        """
        if (not GenomeSpaceTest.logged_in) or (not GenomeSpaceTest.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GenomeSpaceTest.upload_file_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare uploading test.")
        self.dismiss_dialogs()
        try:
            self.uploading("file_to_upload.txt", gs_file_paths["file_to_upload_path"])
        except Exception as e:
            raise DragAndDropException(e.__str__())
        '''function = js_func["upload_file"] % gs_file_paths["file_to_upload_path"]
        print function
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
            raise DragAndDropException("Failed at 'PUT' request: " + response)'''
        
    
