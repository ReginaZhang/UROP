'''
Module created on 26/11/2014

@author: Regina Zhang

'''

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
from data_sharing import DataSharing
from data_storing import DataStoring
from data_to_GVL import DataToGVL
from preparation import Preparation


#base_window = None

js = """var s=document.createElement(\'script\');
        s.innerHTML=\'{0}\';
        s.type=\'text/javascript\';
        document.head.appendChild(s);"""

class GenomeSpaceTest(Preparation, UseGS, CloudStorage, DataManipulation, DataSharing, DataStoring, DataToGVL):

    __metaclass__ = ABCMeta

    def send_request(self, function, function_call):
        driver = self.driver
        self.inject_js(function)
        driver.execute_script(function_call)
        time.sleep(5)
        
    def get_response(self):
        #print 1
        driver = self.driver
        #print 2
        wait = self.wait
        #print 3
        not_complete = True
        #print 4
        while not_complete:
            try:
                #print 5
                elem = wait.until(EC.alert_is_present())
                #print 6
                not_complete = False
                #print 7
            except TimeoutException:
                pass
        #print 8
        alert = driver.switch_to_alert()
        #print 9
        text = alert.text
        #print text
        #alert.dismiss()
        alert.accept()
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


