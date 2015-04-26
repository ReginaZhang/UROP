'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GSTestCases
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from constants import common
from selenium.common.exceptions import *
import register_login as rl
import pickle

#driver = None

class GSFirefox(unittest.TestCase, GSTestCases):
    @classmethod
    def setUpClass(cls):
        #global driver
        #if driver==None:
        print 1
        cls.driver_name = "firefox"
        print 2
        cls.driver = webdriver.Firefox()
        print 3
        driver = cls.driver
        driver.implicitly_wait(10)
        cls.wait = WebDriverWait(driver,20)
        driver.maximize_window()
        home_page = common["base_url"] + common["home_suffix"]
        try:
            driver.get(home_page)
            driver.implicitly_wait(20)
            assert "No results found." not in driver.page_source
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
            cookies = pickle.load(open(cookie_file_name,"rb"))
            print "Hello"
            print type(cookies), cookies
            print "world"
            for cookie in cookies:
                driver.add_cookie(cookie)
            rl.logged_in = True
        except IOError:
            rl.logged_in = False
        try:
            driver.get(home_page)
            assert "No results found." not in driver.page_source
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + home_page)
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            print "Unexpected alert present: " + text

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
