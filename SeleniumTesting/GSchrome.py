import unittest
from GStestcases import GenomeSpaceTest
import GStestcases
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

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
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver,60)
        cls.driver.maximize_window()

if __name__ == "__main__":
    unittest.main()
