'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GenomeSpaceTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from constants import common
import register_login as rl
import pickle

chrome_path = "D:\Softwares\Python2.7.5\New Folder\Scripts\chromedriver.exe"

class GSChrome(unittest.TestCase, GenomeSpaceTest):
    @classmethod
    def setUpClass(cls):
        '''if GStestcases.base_window != None:
            print "Hello"
            self.driver.switch_to_window(GStestcases.base_window)
        else:
            print "World"'''
        cls.driver_name = "chrome"
        cls.driver = webdriver.Chrome(executable_path = chrome_path)
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
            rl.logged_in = True
        except IOError:
            rl.logged_in = False
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

if __name__ == "__main__":
    unittest.main()
