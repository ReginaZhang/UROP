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
#from register_login import registered, logged_in
import register_login as rl

mounted = True

class CloudStorage():
    
    __metaclass__ = ABCMeta
    
    #@unittest.skip("Skip to save time.")
    def test_2a_mount_container(self):
        """
        The test for mounting container functionality of GenomeSpace.
        
        Skipped if the login test was failed.
        """
        if not rl.logged_in:
            raise unittest.SkipTest("Skipped for failed login.")
        driver = self.driver
        wait = self.wait
        def mounting(ctner_name):
            try:
                elem = driver.find_element_by_id(page_container["menu_connect"])
                hover = ActionChains(driver).move_to_element(elem)
                elem = driver.find_element_by_id(page_container["swift_container"])
                hover.move_to_element(elem)
                hover.click().perform()
                form = page_container["mount_container"]
                keys = test_container["mount_container"]
                keys["container"] = ctner_name
                elem = wait.until(EC.element_to_be_clickable((By.ID, form['os_ep'])))
            except TimeoutException:
                raise MountingException("Timed out opening the form.")
            except NoSuchElementException as e:
                messages = e.__str__().split("\n")
                self.dismiss_dialogs()
                raise MountingException(messages[0])
            try:
                for input_ in form.keys():
                    if input_ not in ["submit", "successful_popup"]:
                        elem = driver.find_element_by_id(form[input_])
                        elem.clear()
                        elem.send_keys(keys[input_])
                elem = driver.find_element_by_id(form['submit'])
                elem.click()
                driver.implicitly_wait(5)
                elem = wait.until(EC.alert_is_present())
                alert = driver.switch_to_alert()
                assert alert.text == (form["successful_popup"] % (t_mount_container["container"]))
                time.sleep(3)
                alert.accept()
            except TimeoutException:
                self.dismiss_dialogs()
                raise MountingException()
            except AssertionError:
                text = alert.text
                alert.dismiss()
                self.dismiss_dialogs()
                raise MountingException("Alert: " + text)
            except NoSuchElementException as e:
                messages = e.__str__().split("\n")
                self.dismiss_dialogs()
                raise MountingException(messages[0])
            except Exception, e:
                self.dismiss_dialogs()
                raise MountingException(type(e).__name__ + ": " + e.__str__())
            try:
                time.sleep(10)
                assert "swift:" + keys["container"] in driver.page_source
            except AssertionError:
                raise MountingException("Newly mounted container is not shown.")
        mounting(container_names["for mounting test"])
        time.sleep(10)
        mounting(container_names["for data tests"])
        global mounted
        mounted = True

    #@unittest.skip("Skip to save time.")
    def test_2b_disconnect_container(self):
        """
        The test for testing the disconnect container functionality of GenomeSpace.
        
        Skipped if the login test or mounting container test was failed.
        """
        if (not rl.logged_in) or (not mounted):
            raise unittest.SkipTest("Skipped for failed login or mounting.")
        function = js_func["disconnect"]  % (container_names["for mounting test"])
        try:
            self.send_request(function, "disconnect()")
        except Exception as e:
            raise DisconnectContainerException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise DisconnectContainerException(response)
        '''driver = self.driver
        wait = self.wait
        container = test_container["mount_container"]["container"]
        try:
            xpath = "//*[@dirpath='/Home/swift:{0}']".format(container)
            elem = driver.find_element_by_xpath(xpath)
            action = ActionChains(driver).move_to_element(elem)
            action.context_click().perform()
            elem = driver.find_element_by_xpath("(//a[contains(text(),'Disconnect')])[2]")
            elem.click()
            elem = wait.until(EC.alert_is_present())
            alert = driver.switch_to_alert()
            assert alert.text == "Really unmount external storage swift:" + container
            time.sleep(3)
            alert.accept()
        except TimeoutException:
            raise DisconnectContainerException("Timed out waiting for the confirmation pop-up.")
        except AssertionError:
            text = alert.text
            alert.dismiss()
            raise DisconnectContainerException("Alert: "+text)
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise DisconnectContainerException(messages[0])
        except UnexpectedAlertPresentException:
            raise DisconnectContainerException("An unexpected alert popped up.")
        except Exception, e:
            self.dismiss_dialogs()
            raise DisconnectContainerException(type(e).__name__ + ": " + e.__str__())
        try:
            time.sleep(5)
            assert "swift:" + container not in driver.page_source
            time.sleep(20)
        except AssertionError:
            raise DisconnectContainerException("The container is still shown.")
        except UnexpectedAlertPresentException:
            raise DisconnectContainerException("An unexpected alert popped up.")
        except Exception, e:
            self.dismiss_dialogs()
            raise DisconnectContainerException(type(e).__name__ + ": " + e.__str__())
        '''