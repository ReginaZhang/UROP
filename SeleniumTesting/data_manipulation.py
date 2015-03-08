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
        """
        The test case for testing file renaming functionality
        of GenomeSpace. 
        
        Skipped if the login test was failed.
        """
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        self.dismiss_dialogs()
        file_sizes = ["small"]
        failure = {}
        failure_keys = []
        for size in file_sizes:
            function = js_func["rename"] % (test_file["before_rename_path"][size], test_file["after_rename_path"][size])
            try:
                self.send_request(function, "rename()")
            except Exception as e:
                failure[size] = e.__str__()
                failure_keys.append(size)
            try:
                response = self.get_response()
                assert "Success" in response
                self.refresh_page()
            except AssertionError:
                failure[size] = response
                failure_keys.append(size)
            time.sleep(8)
        cleanup_report = ""
        for size in file_sizes:
            try:
                function = js_func["rename"] % (test_file["after_rename_path"][size], test_file["before_rename_path"][size])
                self.send_request(function, "rename()")
                response = self.get_response()
                assert "Success" in response
                self.refresh_page()
            except AssertionError:
                if size in failure_keys:
                    try:
                        assert "404" in response
                    except AssertionError:
                        cleanup_report += "Failed to rename the " + size + " file back: " + response + " \n"
                cleanup_report += "Failed to rename the " + size + " file back: " + response + " \n"
            except Exception as e:
                cleanup_report += "Failed to rename the " + size + "file back: " + e.__str__() + "\n"
        if failure:
            report  = ""
            for size in failure.keys():
                report += "Failed to rename the " + size + "File: " + failure[size] + "\n"
            raise RenameException(report + "\n" + cleanup_report)

    @unittest.skip("Skip to save time.")
    def test_6b_copy_data_btw_folders(self):
        """
        The test case for testing file copying between folders
        functionality in GenomeSpace.
        
        Skipped if the Login test was failed.
        """
        print "copying data between folders"
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        self.dismiss_dialogs()
        function = js_func["copy_btw_folders"] % (test_file["copy_target_path"]["folder"], test_file["copy_source_path"]["folder"])
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
        """
        The test case for testing copying file between containers 
        functionality in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        print "copying data between containers"
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        self.dismiss_dialogs()
        function = js_func["copy_btw_containers"] % (test_file["copy_target_path"]["container"], test_file["copy_source_path"]["container"])
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
        """
        The test case for testing file deletion functionality
        in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        print "deleting file"
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        self.dismiss_dialogs()
        function = js_func["delete"] % test_file["file_to_delete_path"]
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
        """
        The test for testing moving data between folders 
        functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        print "moving data between folders"
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
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
        """
        The test for testing moving data between containers
        functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        print "moving data between containers"
        if (not rl.logged_in) or (not md.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
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
        