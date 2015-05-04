'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GSTestCases
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from constants import common
import pickle
import chrome_path
from genome_space_test import GenomeSpaceTest
from data_test_preparation import DataTestPreparation

#chrome_path = "D:\Softwares\Python2.7.5\New Folder\Scripts\chromedriver.exe"
chrome_driver_path = chrome_path.driver_path


class GSChrome(unittest.TestCase, GSTestCases):

    @classmethod
    def setUpClass(cls):
        '''if GStestcases.base_window != None:
            print "Hello"
            self.driver.switch_to_window(GStestcases.base_window)
        else:
            print "World"'''
        cls.driver_name = "chrome"
        cls.driver = webdriver.Chrome()#executable_path = chrome_path)
        driver = cls.driver
        driver.implicitly_wait(10)
        cls.wait = WebDriverWait(driver,60)
        driver.maximize_window()
        home_page = common["base_url"] + common["home_suffix"]
        try:
            driver.get(home_page)
            driver.implicitly_wait(20)
            assert "No results found." not in driver.page_source
            #print 1
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.accept()
            print ("Unexpected alert present: " + text)
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + home_page)
        try:
            cookie_file_name = "cookies_" + cls.driver_name + ".pkl"
            #print 2
            cookies = pickle.load(open(cookie_file_name,"rb"))
            #print "Hello"
            #print type(cookies), cookies
            #print "world"
            for cookie in cookies:
                driver.add_cookie(cookie)
            GenomeSpaceTest.logged_in = True
        except IOError:
            GenomeSpaceTest.logged_in = False
        try:
            driver.get(home_page)
            driver.implicitly_wait(20)
            assert "No results found." not in driver.page_source
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + home_page)
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.accept()
            print ("Unexpected alert present: " + text)

    @classmethod
    def tearDownClass(cls):
        #cls.driver.close()
        #cls.driver.quit()
        pass

if __name__ == "__main__":
    unittest.main()
