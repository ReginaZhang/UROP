#from mount_disconnect import CloudStorage
from constants import *
from selenium.webdriver.support.ui import WebDriverWait
import time
from GStestexceptions import *

from genome_space_test import GenomeSpaceTest


class DataTestPreparation(GenomeSpaceTest):

	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, 60)

	#@staticmethod
	def containers(self):
		#self.mounting(container_names["for data tests"][1])
		try:
			time.sleep(10)
			assert "swift:" + container_names["for data tests"][0] in self.driver.page_source
		except AssertionError:
			self.mounting(container_names["for data tests"][0])
			time.sleep(8)
			self.refresh_page()
			time.sleep(8)
		try:
			assert "swift:" + container_names["for data tests"][1] in self.driver.page_source
			#global data_testing_swift_mounted
			#GenomeSpaceTest.data_testing_swift_mounted = True
		except AssertionError:
			self.mounting(container_names["for data tests"][1])
			time.sleep(8)
			self.refresh_page()
			time.sleep(8)
			#GenomeSpaceTest.data_testing_swift_mounted = True
		try:
			assert "swift:" + container_names["for data tests"][0] in self.driver.page_source
			assert "swift:" + container_names["for data tests"][1] in self.driver.page_source
			GenomeSpaceTest.data_testing_swift_mounted = True
			#self.refresh_page()
		except AssertionError:
			raise PreparationException("Containers for file tests are not connected and failed to mount them.")

	def check_dir(self, dir_name):
		try:
			function1 = js_func["check_existence"] % test_folder["%s_path" % dir_name]
			self.send_request(function1, "check_existence()")
		except Exception as e:
			print e.__str__()
			raise e #PreparationException("Failed to check the existence of %s" % dir_name)
		response = self.get_response()
		if "404" in response:
			function2 = js_func["create_subdir"] % test_folder["%s_path" % dir_name]
			try:
				self.send_request(function2, "create_subdir()")
				response = self.get_response()
				assert "Success" in response
			except AssertionError:
				raise PreparationException("Failed to create %s; response is not successful." % dir_name)
		elif "Success" not in response:
			raise PreparationException("Failed to check the existence of %s; failed with status code not 404." % dir_name)
		try:
			self.send_request(function1, "check_existence()")
			response = self.get_response()
			assert "Success" in response
		except AssertionError:
			raise PreparationException("Failed to create %s." % dir_name)

	def subdirs(self):
		self.check_dir("subdir1")
		GenomeSpaceTest.subdir1_exists = True
		self.check_dir("subdir2")
		GenomeSpaceTest.subdir2_exists = True

	def remove_test_file(self, filename, file_path, testname):
		try:
			function1 = js_func["check_existence"]# % file_path
			print function1
			self.send_request(function1, "check_existence()")
		except Exception as e:
			print "a"
			print e.__str__()
			raise PreparationException(e.__str__() + "Failed to check the existence of %s." % filename)
		response = self.get_response()
		print response
		if "Success" in response:
			function2 = js_func["delete"] % file_path
			try:
				self.send_request(function2, "delete")
				response = self.get_response()
				assert "Success" in response
			except Exception:
				raise PreparationException("Failed to delete the existing %s." % filename)
			try:
				self.send_request(function1, "check_existence()")
				response = self. get_response()
				assert "404" in response
			except Exception:
				print "b"
				raise PreparationException("Failed to prepare for the %s test." % testname)
		elif "404" not in response:
			raise PreparationException("Failed to check the existence of %s." % filename)
		GenomeSpaceTest.upload_file_test_ready = True

	def files(self):
		self.remove_test_file("file_to_upload.txt", test_file["file_to_upload_path"], "uploading")

	#@staticmethod
	def test_3_setting_up(self):
		#self.driver = driver
		self.containers()
		#self.subdirs()
		#self.files()

