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
#import register_login as rl
import mount_disconnect as md

from genome_space_test import GenomeSpaceTest as GST

class DataManipulation(GST):
    
    __metaclass__ = ABCMeta
    
    #@unittest.skip("Skip to save time")
    def test_6a_change_file_name(self):
        """
        The test case for testing file renaming functionality
        of GenomeSpace. 
        
        Skipped if the login test was failed.
        """
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.rename_file_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare renaming test.")
        self.dismiss_dialogs()
        """file_sizes = ["small"]
        failure = {}
        failure_keys = []
        for size in file_sizes:"""
            #print 1
        function = js_func["rename"] % (GST.gs_file_paths["file_to_rename_path"], GST.gs_file_paths["after_rename_path"])
        print function
        try:
            self.send_request(function, "rename()")
            #print 2
        except Exception as e:
            raise RenameException("Failed to rename the file: " + e.__str__())
        try:
            response = self.get_response()
            #print 3
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise RenameException("Failed to rename the file: " + response)
        """time.sleep(8)
        #print 4
        cleanup_report = ""
        for size in file_sizes:
            try:
                function = js_func["rename"] % (gs_file_paths["after_rename_path"][size], gs_file_paths["before_rename_path"][size])
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
            raise RenameException(report + "\n" + cleanup_report)"""

    #@unittest.skip("Skip to save time.")
    def test_6b_copy_data_btw_folders(self):
        """
        The test case for testing file copying between folders
        functionality in GenomeSpace.
        
        Skipped if the Login test was failed.
        """
        #print "copying data between folders"
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.copying_data_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare copying data tests.")
        self.dismiss_dialogs()
        function = js_func["copy_file"] % (GST.gs_file_paths["copy_to_folder_target_path"], GST.gs_file_paths["file_to_copy_source_path"])
        try:
            self.send_request(function, "copy_file()")
        except Exception as e:
            raise CopyException("Failed to copy the file between folders. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between folders. \n" + response)
        
    #@unittest.skip("Skip to save time.")    
    def test_6c_copy_data_btw_containers(self):
        """
        The test case for testing copying file between containers 
        functionality in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        #print "copying data between containers"
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.copying_data_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare copying data tests.")
        self.dismiss_dialogs()
        function = js_func["copy_file"] % (GST.gs_file_paths["copy_to_container_target_path"], GST.gs_file_paths["file_to_copy_source_path"])
        try:
            self.send_request(function, "copy_file()")
        except Exception as e:
            raise CopyException("Failed to copy the file between containers. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between containers. \n" + response)
        
    #@unittest.skip("Skip to save time.")
    def test_6d_delete_file(self):
        """
        The test case for testing file deletion functionality
        in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        #print "deleting file"
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.deleting_data_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare deleting test.")
        self.dismiss_dialogs()
        function = js_func["delete"] % GST.gs_file_paths["file_to_delete_path"]
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
        
    #@unittest.skip("Skip to save time.")    
    def test_6e_move_data_btw_folders(self):
        """
        The test for testing moving data between folders 
        functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        #print "moving data between folders"
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.moving_data_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare moving data tests.")
        self.dismiss_dialogs()
        function = js_func["move_file"] % (GST.gs_file_paths["file_to_move_to_folder_source_path"], GST.gs_file_paths["move_to_folder_target_path"])
        try:
            self.send_request(function, "move_file()")
        except Exception as e:
            raise MoveException("Failed to move the data between folders. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise MoveException("Failed to move the data between folders. \n" + response)
    #@unittest.skip("Skip to save time.")    
    def test_6f_move_data_btw_containers(self):
        """
        The test for testing moving data between containers
        functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        #print "moving data between containers"
        if (not GST.logged_in) or (not GST.data_testing_swift_mounted):
            raise unittest.SkipTest("Skipped for failed login or failed mounting container.")
        elif not GST.moving_data_test_ready:
            raise unittest.SkipTest("Skipped for failed to prepare moving data tests.")
        self.dismiss_dialogs()
        function = js_func["move_file"] % (GST.gs_file_paths["file_to_move_to_container_source_path"], GST.gs_file_paths["move_to_container_target_path"])
        try:
            self.send_request(function, "move_file()")
        except Exception as e:
            raise MoveException("Failed to move the data between containers. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise MoveException("Failed to move the data between containers. \n" + response)
        
