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
	#generate_public_URL_test_ready = False
	default_folder_to_be_used = False

	user_details = {}
	local_file_paths = {}
	container_one = {}
	container_two = {}
	container_names = {}
	gs_file_paths = {}
	gs_folder_paths = {}
	doi_info = {}


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
		if GenomeSpaceTest.container_one["container"] == ctner_name:
			detail = str(GenomeSpaceTest.container_one)
		elif GenomeSpaceTest.container_two["container"] == ctner_name:
			detail = str(GenomeSpaceTest.container_two)
		else:
			raise MountingException("Container name is not one of the container names specified.")
		tokens = detail.split("'")
		detail = tokens[0]
		for elem in tokens[1:]:
			detail += '"' + elem
		print "\n\nin mounting", GenomeSpaceTest.user_details["username"]
		print type(detail), detail
		function = js_func["mount"] % (GenomeSpaceTest.user_details["username"], ctner_name, detail)
		print function
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

	def uploading(self, filename, file_path, data):
		function = js_func["upload_file"] % (file_path, data) #gs_file_paths["file_to_upload_path"]
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
		#global user_details, local_file_paths, container_one, container_two, container_names, gs_file_paths, gs_folder_paths, doi_info
		Config = ConfigParser.ConfigParser()
		Config.optionxform = str
		Config.read("./file_paths.cfg")
		errors = ""
		GenomeSpaceTest.user_details, errors = cls.make_dict(Config, "UserDetails",errors, default_user_details)
		GenomeSpaceTest.local_file_paths, errors = cls.make_dict(Config, "LocalFilePaths", errors, default_local_file_paths)
		print "local paths: ", GenomeSpaceTest.local_file_paths
		GenomeSpaceTest.container_one, errors = cls.make_dict(Config, "GSContainerOne", errors, default_container_one)
		GenomeSpaceTest.container_two, errors = cls.make_dict(Config, "GSContainerTwo", errors, default_container_two)
		GenomeSpaceTest.container_names = {"for mounting test" : GenomeSpaceTest.container_one["container"],
                           "for data tests" : [GenomeSpaceTest.container_one["container"], GenomeSpaceTest.container_two["container"]]}
		GenomeSpaceTest.gs_file_paths, errors = cls.make_dict(Config, "GSFilePaths", errors, default_gs_file_paths)
		if ((("GSFilePath" in errors) or ("GSFolderPath" in errors)) and ("default is to be used" in errors)):
			default_folder_to_be_used = True
		new_file_name = Config.get("Others", "new_file_name_for_renaming_test")
		tokens = GenomeSpaceTest.gs_file_paths["file_to_rename_path"].split("/")
		tokens = tokens[:-1]
		if new_file_name == "":
			new_file_name = default_file_name_for_renaming_test
			errors += "in Others, new_file_name is not provided; default is to be used.\n"
		tokens.append(new_file_name)
		GenomeSpaceTest.gs_file_paths["after_rename_path"] = "/".join(tokens)
		print GenomeSpaceTest.gs_file_paths
		GenomeSpaceTest.gs_folder_paths, error = cls.make_dict(Config, "GSFolderPaths", errors, default_gs_folder_paths)
		GenomeSpaceTest.doi_info, errors = cls.make_dict(Config, "DOIInfo", errors, default_doi_info)
		if errors != "":
			print >>sys.stderr, "Configeration Errors: \n"
			print >>sys.stderr, errors
			print >>sys.stderr, "="*70 + "\n"

	@classmethod
	def make_dict(cls, Config, sectionname, errors, default_dict):
		dictnry = {}
		for option in Config.options(sectionname):
			value = Config.get(sectionname, option)
			if value == "":
				errors = errors + ("in %s, %s is not provided; default is to be used.\n" % (sectionname, option))
				if (option != "copy_to_container_target_path") and (option != "move_to_container_target_path"):
					dictnry[option] = (default_dict[option] % container_one["container"])
				else:
					dictnry[option] = (default_dict[option] % container_two["container"])
			else:
				try:
					dictnry[option] = value
				except Exception as e:
					errors += e.__str__()
					errors += "\n"
		return (dictnry, errors)





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