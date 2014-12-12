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
        try:
            driver.get(common['base_url'])
            assert "No results found." not in driver.page_source
        except AssertionError:
            driver.close()
            raise Exception("Page not found: " + common['base_url'])
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            raise Exception("Unexpected alert present: " + text)

if __name__ == "__main__":
    unittest.main()
