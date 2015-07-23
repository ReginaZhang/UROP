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

from genome_space_test import GenomeSpaceTest as GST

class DataStoring(GST):
    
    __metaclass__ = ABCMeta
    
    #@unittest.skip("Skip to save time.")
    def test_4a_import_url(self):
        """
        The test for testing importing data using the public URL.
        
        The public URL is fixed to a certain URL at the moment.
        Need to change every two days.
        
        Skipped if the login test was failed.
        """
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.importing_url_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare importing file using public URL test.")
        self.dismiss_dialogs()
        function = js_func["import_url"] % (GST.gs_file_paths["file_to_import_with_URL_path"], GST.gs_folder_paths["dir1_path"])
        print
        print
        print
        print function
        print
        print
        print
        try:
            self.send_request(function, "import_url()")
        except Exception as e:
            raise ImportURLException(e.__str__())
        try:
            response = self.get_response()
            print response
            assert "Success" in response
        except AssertionError:
            raise ImportURLException("Failed to generate public URL for importing. " + response)
        try:
            response = self.get_response()
            print response
            assert "Success" in response
        except AssertionError:
            raise ImportURLException("Failed to import data using public URL. " + response)
    
    #@unittest.skip("problem. Skip to save time.")
    def test_4b_upload_file(self):
        """
        The test for uploading functionality in GenomeSpace 
        using drag-and-drop method.
        This test is conducted by sending Http Request with
        file content as the request body to imitate the process.
        
        Skipped if the login test was failed.
        """
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.upload_file_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare uploading test.")
        self.dismiss_dialogs()
        try:
            f = open(GST.local_file_paths["file_to_upload_path"], "r")
            data = f.read()
            self.uploading("file_to_upload.txt", GST.gs_file_paths["file_to_upload_path"], data)
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
        
    
