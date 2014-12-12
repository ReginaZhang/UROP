'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GenomeSpaceTest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from constants import common
from selenium.common.exceptions import *

class GSFirefox(unittest.TestCase, GenomeSpaceTest):
    @classmethod
    def setUpClass(cls):
        cls.driver_name = "firefox"
        cls.driver = webdriver.Firefox()
        driver = cls.driver
        driver.implicitly_wait(10)
        cls.wait = WebDriverWait(driver,20)
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
            print "Unexpected alert present: " + text

if __name__ == "__main__":
    unittest.main()
