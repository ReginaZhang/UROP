import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from GStestexceptions import *
from constants import *
import sys
import time
from abc import ABCMeta, abstractmethod

registered = False
logged_in = False
mounted = False
#base_window = None
"""jq = '''$.ajax({
            type:"{0}",
            url:"{1}",
            contentType:"{2}",
            {3}
            success: function (data, status, jqXHR){
                {4}
            },
            error: function (jqXHR, status){
                {5}
            }
        });'''"""
js = """var s=document.createElement(\'script\');
        s.innerHTML='{0}';
        s.type='text/javascript';
        document.head.appendChild(s)"""

class GenomeSpaceTest():
    '''def setUp(self):
        self.driver_type = args[0]
        driver_type = self.driver_type.lower()
        if driver_type == "firefox":
            self.driver = webdriver.Firefox()
        elif driver_type == "chrome":
            self.driver = webdriver.Chrome(executable_path = chrome_path)
        else:
            print "Not supported browser: " + self.driver_type
            sys.exit()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver,20)'''

    __metaclass__ = ABCMeta
    
    '''@abstractmethod
    @classmethod
    def setUpClass(cls):
        pass'''

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
        '''global base_window
        base_window = driver.current_window_handle
        print base_window'''

    #@unittest.skipUnless(registered, )
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
            '''elemts = driver.find_elements_by_tag_name("a")
            print elemts
            for elem in elemts:
                print elem.text
                if elem.text == "Disconnect" and elem.is_enabled():
                    print "found it"
                    action.move_to_element(elem).click().perform()
                    print "and clicked"'''
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
            raise DissconnectContainerException("An unexpected alert popped up.")
        except Exception, e:
            self.dismiss_dialogs()
            raise DisconnectContainerException(type(e).__name__ + ": " + e.__str__())
        try:
            time.sleep(5)
            assert "swift:" + container not in driver.page_source
            time.sleep(20)
        except AssertionError:
            raise DissconnectContainerException("The container is still shown.")
        except UnexpectedAlertPresentException:
            raise DissconnectContainerException("An unexpected alert popped up.")
        except Exception, e:
            self.dismiss_dialogs()
            raise DisconnectContainerException(type(e).__name__ + ": " + e.__str__())

    '''def test_3a_connect_Galaxy(self):
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        try:
    
    def test_4b_'''

    def test_6a_change_file_name(self):
        if (not registered) or (not logged_in):
            raise unittest.SkipTest("Skipped for failed registration or login.")
        driver = self.driver
        wait = self.wait
        self.dismiss_dialogs()
        '''try:
            elem = driver.find_element_by_xpath(test_folder["GS-Demo_xpath"])
            elem.click()
            time.sleep(3)
            elem = driver.find_element_by_xpath(test_folder["test1_xpath"])
            elem.click()
            time.sleep(6)
            #elem = wait.until(EC.element_to_be_clickable((By.ID, page_file["sort_filename"])))
            elem = driver.find_element_by_id(page_file["sort_filename"])
            assert elem.text == "Filename"
            aciton = ActionChains(driver).move_to_element(elem).context_click().perform
            #elem.click()
            time.sleep(2)
            elem = driver.find_element_by_xpath(test_file["before_rename_xpath"])
            except AssertionError:
            raise Exception("not in the folder")
        except NoSuchElementException, e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise Exception("cannot find the directory or file before renaming!" + messages[0])
        try:
            driver.maximize_window()
            action = ActionChains(driver).move_to_element(elem)
            action.click(elem).perform()
            time.sleep(5)
            elemts = driver.find_elements_by_xpath("//a[contains(text(),'Rename')]")
            print len(elemts)
            index = 0
            for item in elemts:
                print item.text
                if item.is_enabled():
                    print index
                    elem = item
                    break
                index += 1
            action.move_to_element(elem)
            action.click().perform()
            elem = driver.find_element_by_id(common["menu_file"])
            hover = ActionChains(driver).move_to_element(elem)
            elem = driver.find_element_by_id(page_file["rename"])
            hover.move_to_element(elem)
            hover.click().perform()
            elemts = driver.find_elements_by_tag_name("input")
            count = 0
            for item in elemts:
                if item.is_enabled():
                    count += 1
                    #print item.get_attribute("@value")
                    #assert item.get_attribute("@placeholder") == test_file["before_rename"]
                    #item.clear()
                    #time.sleep(2)
                    #item.send_keys(test_file["after_rename"])
                    #print item.get_attribute("@value")
            print count
        except NoSuchElementException, e:
            messages = e.__str__().split("\n")
            self.dismiss_dialogs()
            raise Exception(messages[0])'''
        try:
            function = '''function rename() {\
                var xmlhttp=new XMLHttpRequest();\
                xmlhttp.open("GET", "https://genomespace.genome.edu.au/datamanager/v1.0/tags/file/Home/swift:UROP/test1",false);\
                xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");\
                xmlhttp.onreadystatechange=function(){\
                            alert(xmlhttp.readyState+";"+xmlhttp.status);\
                    };\
                xmlhttp.send();\
            }'''
            #print js.format(function)
            #print driver.page_source
            driver.execute_script(js.format(function))
            #s= driver.page_source
            #print s
            driver.execute_script("rename()")
            time.sleep(5)
            rs_s = {}
            unexpected_alert = []
            while True:
                try:
                    alert = driver.switch_to_alert()
                    contents = alert.text.split(";")
                    if contents[0].isdigit() and contents[1].isdigit():
                        rs_s[contents[0]] = contents[1]
                    else:
                        unexpected_alert.append(alert.text)
                    alert.dismiss()
                    time.sleep(3)
                except NoAlertPresentException:
                    break
            print rs_s
            print unexpected_alert
            driver.close()
        except Exception as e:
            print e.__str__()
            

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
