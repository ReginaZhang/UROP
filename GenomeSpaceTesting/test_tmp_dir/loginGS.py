from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import sys

class LoginGS:
    """ Log in to GenomeSpace using webdriver """
    def __init__(self, driver_type):
        """
        Param:
            driver_type - the browser name ("firefox"/"chrome")
        """
        self.driver_type = driver_type
    
    def setUp(self):
        '''
        setUp()
        
        Description:
            to set up the webdriver
        '''
        driver_type = self.driver_type
        if driver_type == "firefox":
            self.driver = webdriver.Firefox()
        elif driver_type == "chrome":
            path = "D:\Softwares\Python2.7.5\New Folder\Scripts\chromedriver.exe"
            self.driver = webdriver.Chrome(executable_path = path)
        else:
            print "Invalid browser: " + driver_type
            sys.exit()

        # wait for the web driver to start
        self.driver.implicitly_wait(10)
        # set variables for later use
        self.base_url = "https://genomespace-dev.genome.edu.au/jsui"
        self.wait = WebDriverWait(self.driver, 20)
    
    def do_login(self):
        '''
        do_login()

        Description:
            to do the login process
        '''
        driver = self.driver
        wait = self.wait
        driver.get(self.base_url)
        assert "No results found." not in driver.page_source
        try:
            # try if an alert popped up
            alert = driver.switch_to_alert()
        except NoAlertPresentException:
            print alert.text
            alert.dismiss()
        try:
            # wait until the page is loaded and ready
            elem = wait.until(EC.element_to_be_clickable((By.ID, "identity")))
            elem = driver.find_element_by_id("identity")
            elem.clear()
            elem.send_keys("test")
            elem = driver.find_element_by_id("password")
            elem.clear()
            elem.send_keys("test")
            elem = driver.find_element_by_id("signin_button")
            elem.click()
        except TimeoutException:
            # failed to load the right page
            print "Timed out loading page."
        except NoSuchElementException, e:
            print e
        driver.close()
        
    def done(self):
        '''
        done()

        Description:
            to clear up after do_login
        '''
        self.driver.quit()

    def login(self):
        '''
        login()

        Description:
            run the test from setting-up to cleaning-up
        '''
        self.setUp()
        self.do_login()
        self.done()
    
