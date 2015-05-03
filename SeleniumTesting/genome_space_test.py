'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from constants import *
import time
from abc import ABCMeta, abstractmethod

js = """var s=document.createElement(\'script\');
        s.innerHTML=\'{0}\';
        s.type=\'text/javascript\';
        document.head.appendChild(s);"""

class GenomeSpaceTest():
	__metaclass__ = ABCMeta

	logged_in = False
	data_testing_swift_mounted = False
	subdir1_exists = False
	subdir2_exists = False

	#@staticmethod
	def send_request(self, function, function_call):
		driver = self.driver
		self.inject_js(function)
		driver.execute_script(function_call)
		time.sleep(5)

	#@staticmethod
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

	#@staticmethod
	def inject_js(self, function):
		driver = self.driver
		driver.execute_script(js.format(js_func["get_response"]))
		driver.execute_script(js.format(function))

	#@staticmethod
	def refresh_page(self):
		driver = self.driver
		driver.execute_script("refreshDirectoryList(function(e) {\
					rootDirectoryCallback(e);\
					openOnDirectoryFromUrl();\
					$('#splashScreen').trigger('click');\
					});")

	#@staticmethod
	def dismiss_dialogs(self):
		elemts = self.driver.find_elements_by_tag_name("Button")
		for elem in elemts:
			if elem.text == "Close" and elem.is_enabled():
				elem.click()

	#@staticmethod
	def mounting(self, ctner_name):
		t_mount_container["container"] = ctner_name
		detail = str(t_mount_container)
		tokens = detail.split("'")
		detail = tokens[0]
		for elem in tokens[1:]:
			detail += '"' + elem
		function = js_func["mount"] % (ctner_name, detail)
		#print function
		try:
			self.send_request(function,"mount()")
		except Exception as e:
			raise e
		try:
			#print "trying to get response"
			response = self.get_response()
			assert "Success" in response
			self.refresh_page()
		except AssertionError as e:
			raise e
