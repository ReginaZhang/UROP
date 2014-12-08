'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from GStestcases import GenomeSpaceTest
import GStestcases
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class GSFirefox(unittest.TestCase, GenomeSpaceTest):
    @classmethod
    def setUpClass(cls):
        cls.driver_name = "firefox"
        cls.driver = webdriver.Firefox()
        '''if GStestcases.registered:
            print "Hello"
            self.driver.switch_to_window(GStestcases.base_window)
        else:'''
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver,20)
        cls.driver.maximize_window()

if __name__ == "__main__":
    unittest.main()
