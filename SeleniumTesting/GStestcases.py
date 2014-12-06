import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from GStestexceptions import *
from constants import *
import sys
import time
from abc import ABCMeta, abstractmethod
from pip._vendor.requests.models import Response

registered = False
logged_in = False
mounted = True
#base_window = None

js = """var s=document.createElement(\'script\');
        s.innerHTML=\'{0}\';
        s.type=\'text/javascript\';
        document.head.appendChild(s);"""

class GenomeSpaceTest():

    __metaclass__ = ABCMeta

    def test_1a_register(self):
        driver = self.driver
        wait = self.wait
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
        try:
            link = page_register['registration_link_text']
            elem = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link)))
            elem = driver.find_element_by_link_text(link)
            elem.click()
            driver.get(common["base_url"])
        except AssertionError:
            raise Exception("Failed to assert!")
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            raise Exception("Unexpected alert present: " + text)
        global registered
        registered = True

    #@unittest.skip("for testing")
    def test_1b_login(self):
        if not registered:
            raise unittest.SkipTest("Skipped for failed registration.")
        driver = self.driver
        wait = self.wait
        try:
            # try if an alert popped up
            alert = driver.switch_to_alert()
            print "Alert popped up and dismissed: " + alert.text
            alert.dismiss()
        except NoAlertPresentException:
            pass
        try:
            # wait until the page is loaded and ready
            elem = wait.until(EC.element_to_be_clickable((By.ID, page_login['login_name'])))
        except TimeoutException:
            driver.close()
            raise LoginException("Timed out loading page before login.")
        try:
            elem = driver.find_element_by_id(page_login['login_name'])
            elem.clear()
            elem.send_keys(test_login['login_name'])
            elem = driver.find_element_by_id(page_login['login_pw'])
            elem.clear()
            elem.send_keys(test_login['login_pw'])
            elem = driver.find_element_by_id(page_login['login_signin'])
            elem.click()
            driver.implicitly_wait(10)
            assert "Invalid username or password" not in driver.page_source
            elem = wait.until(EC.element_to_be_clickable((By.ID, common["menu_file"])))
            time.sleep(20)
        except AssertionError as e:
            driver.close()
            raise LoginException("Invalid username or password", test_login['login_name'], test_login['login_pw'])
        except TimeoutException:
            # failed to load the page after logging in
            driver.close()
            raise LoginException("Timed out loading page when logging in.", test_login['login_name'], test_login['login_pw'])
        except NoSuchElementException as e:
            messages = e.__str__().split("\n")
            driver.close()
            raise LoginException(messages[0])
        except UnexpectedAlertPresentException:
            alert = driver.switch_to_alert()
            text = alert.text
            alert.dismiss()
            raise LoginException("Unexpected alert present: " + text)
        except Exception as e:
            driver.close()
            raise LoginException("Failed logging in: "+e.__str__(), test_login['login_name'], test_login['login_pw'])
        global logged_in
        logged_in = True

    @unittest.skip("I just wanna skip it.")
    def test_2a_mount_container(self):
        if (not registered) or (not logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        try:
            elem = driver.find_element_by_id(page_container["menu_connect"])
            hover = ActionChains(driver).move_to_element(elem)
            elem = driver.find_element_by_id(page_container["swift_container"])
            hover.move_to_element(elem)
            hover.click().perform()
            form = page_container["mount_container"]
            keys = test_container["mount_container"]
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
            assert alert.text == form["successful_popup"]
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
        global mounted
        mounted = True

    @unittest.skip("I just wanna skip it.")
    def test_2b_disconnect_container(self):
        if (not registered) or (not logged_in) or (not mounted):
            raise unittest.SkipTest("Skipped for failed registration, loggin or mounting.")
        driver = self.driver
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

    '''def test_3a_connect_Galaxy(self):
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        try:
    
    def test_4b_'''

    @unittest.skip("I just wanna skip it.")
    def test_6a_change_file_name(self):
        if (not registered) or (not logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["rename"]
        try:
            self.send_request(function, "rename()")
            #self.test_2a_mount_container()
            #print js.format(function)
            #print driver.page_source
            #s= driver.page_source
            #print s
        except Exception as e:
            raise RenameException(e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise RenameException(response)

    @unittest.skip("I just wanna skip it")
    def test_6b_copy_data_btw_folders(self):
        if (not registered) or (not logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["copy_btw_folders"]
        try:
            self.send_request(function, "copy_btw_folders()")
        except Exception as e:
            raise CopyException("Failed to copy the file between folders. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between folders. \n" + response)
        
    def test_6c_copy_data_btw_containers(self):
        if (not registered) or (not logged_in) or(not mounted):
            raise unittest.SkipTest("Skipped for failed registration, login or mounting.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["copy_btw_containers"]
        try:
            self.send_request(function, "copy_btw_containers()")
        except Exception as e:
            raise CopyException("Failed to copy the file between containers. \n" + e.__str__())
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise CopyException("Failed to copy the file between containers. \n" + response)
        
    def test_6d_delete_file(self):
        if (not registered) or (not logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        function = js_func["delete"]
        try:
            self.send_request(function, "delete()")
        except Exception as e:
            raise DeleteException(e.__str__()) 
        try:
            response = self.get_response()
            assert "Success" in response
            self.refresh_page()
        except AssertionError:
            raise DeleteException(response)

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
