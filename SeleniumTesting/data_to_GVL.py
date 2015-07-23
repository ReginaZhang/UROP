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
#import register_login as rl
#import mount_disconnect as md

from genome_space_test import GenomeSpaceTest as GST

class DataToGVL(GST):
    
    __metaclass__ = ABCMeta
    
    #@unittest.skip("The two request are not clear.")
    def test_7b_launch_with_file(self):
        """
        The test for testing launching the connected Galaxy with file.
        No Galaxy connection test at the moment.
        The Galaxy used in this test was the default Galaxy.
        
        Skipped if the login test was failed.
        """
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.launch_GVL_with_file_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare launch Galaxy with file test.")
        #file_url = "https://genomespace.genome.edu.au:443/datamanager/file/Home/swift:UROP/file_to_share.txt"
        #file_url_escaped = "https%3A%2F%2Fgenomespace.genome.edu.au%3A443%2Fdatamanager%2Ffile%2FHome%2Fswift%3AUROP%2Ffile_to_share.txt"
        function = js_func["launch_with_file"] % (GST.gs_file_paths["file_to_launch_GVL_with"], GST.user_details["username"])
        print function
        try:
            self.send_request(function, "launch_with_file()")
        except Exception as e:
            raise LaunchWithFileException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
        except AssertionError:
            raise LaunchWithFileException("Failed at POST: " + response)
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise LaunchWithFileException("Failed at GET: " + response)
        
        
