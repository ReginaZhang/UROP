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
from GStestexceptions import *
import ConfigParser
import sys

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
	upload_file_test_ready = False
	rename_file_test_ready = False
	copying_data_test_ready = False

	#@staticmethod
	def send_request(self, function, function_call):
		driver = self.driver
		self.inject_js(function)
		driver.execute_script(function_call)
		#time.sleep(5)

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
			raise MountingException(response)

	def uploading(self, filename, file_path):
		function = js_func["upload_file"] % file_path #gs_file_paths["file_to_upload_path"]
		#print function
		try:
			print "b"
			self.send_request(function, "upload_file()")
			print "a"
		except Exception as e:
			raise Exception(e.__str__())
		try:
			response = self.get_response()
			assert "Success" in response
		except AssertionError:
			raise Exception("Failed at 'GET' request: " + response)
		try:
			time.sleep(2)
			response = self.get_response()
			assert "Success" in response
			self.refresh_page()
		except AssertionError:
			raise Exception("Failed at 'PUT' request: " + response)

	@classmethod
	def parse_config(cls):
		Config = ConfigParser.ConfigParser()
		Config.read("./file_paths.cfg")
		#local_file_paths = {}
		errors = ""
		for option in Config.options("LocalFilePaths"):
			try:
				local_file_paths[option] = Config.get("LocalFilePaths", option)
			except Exception as e:
				errors += e.__str__()
				errors += "\n"
		print local_file_paths
		for option in Config.options("GSFilePaths"):
			try:
				gs_file_paths[option] = Config.get("GSFilePaths", option)
			except Exception as e:
				errors += e.__str__()
				errors += "\n"
		print gs_file_paths
		new_file_name = Config.get("Others", "new_file_name_for_renaming_test")
		tokens = gs_file_paths["before_rename_path"].split("/")
		tokens = tokens[:-1]
		if new_file_name == "":
			new_file_name = default_file_name_for_renaming_test
		tokens.append(new_file_name)
		gs_file_paths["after_rename_path"] = "/".join(tokens)
		print gs_file_paths
		if errors != "":
			print >>sys.stderr, "Configeration Errors: \n"
			print >>sys.stderr, errors
			print >>sys.stderr, "="*70 + "\n"




'''print "sections"
    print Config.sections()
    print "options"
    print Config.options("LocalSystemPaths")
    print "value to age"
    print Config.get("SectionOne", "age")
    print Config.options("SectionTwo")
    print Config.get("SectionTwo", "favorite color")
		pass
'''