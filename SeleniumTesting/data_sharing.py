'''
Module created on 08/12/2014

@author: Regina Zhang

'''

import unittest
from abc import ABCMeta
from GStestexceptions import *
from constants import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from _codecs import register
from selenium.webdriver.common.action_chains import ActionChains
import register_login as rl

class DataSharing():
    
    __metaclass__ = ABCMeta
    
    @unittest.skip("Not finished")
    def test_5a_generate_public_URL(self):
        """
        The test for testing generating public URL of the file in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        if not rl.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        self.dismiss_dialogs()
        function = js_func["generate_public_url"]
        try:
            self.send_request(function, "generate_public_url()")
        except Exception as e:
            raise PublicURLException("Failed to generate public URL.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            time.sleep(2)
        except AssertionError:
            raise PublicURLException("Failed to generate public URL.\n" + response)
        try:
            self.wait.until(EC.alert_is_present())
            alert = self.driver.switch_to_alert()
            assert "Public URL" in alert.text
        except TimeoutException:
            raise PublicURLException("Failed to catch public URL pop-up.")
        except AssertionError:
            raise PublicURLException("Failed to get generated public URL.")
        try:
            public_url = alert.text.lstrip("Public URL: ")
            function = js_func["share_data"].format(public_url)
            self.send_request(function, "share_data()")
        except Exception as e:
            raise PublicURLException("Failed to share data using public URL generated.\n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise PublicURLException("Failed to share data using public URL generated.\n" + response)
        
    @unittest.skip("Skip to save time.")
    def test_5d_generate_private_url(self):
        """
        The test for testing generating private URL of the file in GenomeSpace.
        
        Skipped if the login test was failed.
        """
        if not rl.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        self.dismiss_dialogs()
        driver = self.driver
        wait = self.wait
        try:
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, test_folder["UROP_xpath"])))
            elem = driver.find_element_by_xpath(test_folder["UROP_xpath"])
            elem.click()
            time.sleep(8)
            elem = wait.until(EC.element_to_be_clickable((By.XPATH, test_file["file_to_share_xpath"])))
            elem = driver.find_element_by_xpath(test_file["file_to_share_xpath"])
            elem.click()
            elem = driver.find_element_by_id(common["menu_file"])
            hover = ActionChains(driver).move_to_element(elem)
            elem = driver.find_element_by_id(page_file["view_private_link"])
            hover.move_to_element(elem).click().perform()
            elem = driver.find_element_by_xpath(page_file["private_url_dialog_xpath"])
            private_link = elem.get_attribute("value")
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise PrivateURLException(messages[0])
        except Exception as e:
            raise PrivateURLException(e.__str__())
        function = js_func["share_data"] % (private_link)
        try:
            self.send_request(function, "share_data()")
        except Exception as e:
            raise PrivateURLException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.dismiss_dialogs()
            self.refresh_page()
        except AssertionError:
            raise PrivateURLException(response)
        try:
            elem = driver.find_element_by_xpath(common["Home_xpath"])
            mouse = ActionChains(driver).move_to_element(elem)
            mouse.click().perform()
            time.sleep(5)
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise Exception("Failed to return to Home directory.\n" + messages[0])
        except Exception as e:
            raise Exception("Failed to return to Home directory.\n" + e.__str__())
            