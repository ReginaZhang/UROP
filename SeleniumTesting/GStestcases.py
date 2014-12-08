import unittest
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#from GStestexceptions import *
from constants import *
#import sys
import time
from abc import ABCMeta, abstractmethod
#from pip._vendor.requests.models import Response
from register_login import UseGS
from mount_disconnect import CloudStorage
from data_manipulation import DataManipulation



#base_window = None

js = """var s=document.createElement(\'script\');
        s.innerHTML=\'{0}\';
        s.type=\'text/javascript\';
        document.head.appendChild(s);"""

class GenomeSpaceTest(UseGS, CloudStorage, DataManipulation):

    __metaclass__ = ABCMeta

    

    def send_request(self, function, function_call):
        driver = self.driver
        self.inject_js(function)
        driver.execute_script(function_call)
        time.sleep(5)
        
    def get_response(self):
        driver = self.driver
        wait = self.wait
        not_complete = True
        while not_complete:
            try:
                elem = wait.until(EC.alert_is_present())
                not_complete = False
            except TimeoutException:
                pass
        alert = driver.switch_to_alert()
        text = alert.text
        alert.dismiss()
        return text

    def inject_js(self, function):
        driver = self.driver
        driver.execute_script(js.format(js_func["get_response"]))
        driver.execute_script(js.format(function))

    def refresh_page(self):
        driver = self.driver
        driver.execute_script("refreshDirectoryList(function(e) {\
                    rootDirectoryCallback(e);\
                    openOnDirectoryFromUrl();\
                    $('#splashScreen').trigger('click');\
                });")

    def dismiss_dialogs(self):
        elemts = self.driver.find_elements_by_tag_name("Button")
        for elem in elemts:
            if elem.text == "Close" and elem.is_enabled():
                elem.click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()


'''if __name__ == "__main__":
    args = sys.argv[1:]
    del sys.argv[1:]
    unittest.main()'''

#my_args = sys.argv[1:]
#del sys.argv[1:]
#print sys.argv[1]
