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
import mount_disconnect as md

class DataManipulation():
    
    __metaclass__ = ABCMeta
    
    @unittest.skip("Skip to save time")
    def test_6a_change_file_name(self):
        '''
        The test case for testing file rename functionality
        of GenomeSpace. 
        '''
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["rename"] % (test_file["before_rename_url"], test_file["after_rename_path"])
        try:
            self.send_request(function, "rename()")
        except Exception as e:
            raise RenameException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise RenameException(response)

    @unittest.skip("Skip to save time.")
    def test_6b_copy_data_btw_folders(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["copy_btw_folders"]
        try:
            self.send_request(function, "copy_btw_folders()")
        except Exception as e:
            raise CopyException("Failed to copy the file between folders. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between folders. \n" + response)
        
    @unittest.skip("Skip to save time.")    
    def test_6c_copy_data_btw_containers(self):
        if (not rl.registered) or (not rl.logged_in) or(not md.mounted):
            raise unittest.SkipTest("Skipped for failed registration, login or mounting.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["copy_btw_containers"]
        try:
            self.send_request(function, "copy_btw_containers()")
        except Exception as e:
            raise CopyException("Failed to copy the file between containers. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between containers. \n" + response)
        
    @unittest.skip("Skip to save time.")
    def test_6d_delete_file(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["delete"]
        try:
            self.send_request(function, "delete_data()")
        except Exception as e:
            raise DeleteException(e.__str__()) 
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise DeleteException(response)
        
    @unittest.skip("Skip to save time.")    
    def test_6e_move_data_btw_folders(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["move_btw_folders"]
        try:
            self.send_request(function, "move_btw_folders()")
        except Exception as e:
            raise MoveException("Failed to move the data between folders. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise MoveException("Failed to move the data between folders. \n" + response)
    @unittest.skip("Skip to save time.")    
    def test_6f_move_data_btw_containers(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        self.dismiss_dialogs()
        function = js_func["move_btw_containers"]
        try:
            self.send_request(function, "move_btw_containers()")
        except Exception as e:
            raise MoveException("Failed to move the data between containers. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise MoveException("Failed to move the data between containers. \n" + response)
        