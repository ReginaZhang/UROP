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
#from register_login import registered, logged_in
#from mount_disconnect import mounted

class DataManipulation():
    
    __metaclass__ = ABCMeta
    
    @unittest.skip("I just wanna skip it.")
    def test_6a_change_file_name(self):
        if (not rl.registered) or (not rl.logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["rename"]
        try:
            self.send_request(function, "rename()")
            #self.test_2a_mount_container()
            #print js.format(function)
            #print driver.page_source
            #s= driver.page_source
            #print s
        except Exception as e:
            raise RenameException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise RenameException(response)

    @unittest.skip("I just wanna skip it")
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
        
    @unittest.skip("I just wanna skip it")    
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
        
    @unittest.skip("I just wanna skip it")
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
    @unittest.skip("I just wanna skip it.")    
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
        