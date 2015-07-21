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
			print function1
			self.send_request(function1, "check_existence()")
			#print "there"
		except Exception as e:
			#print 1
			print e.__str__()
			raise e #PreparationException("Failed to check the existence of %s" % dir_name)
		response = self.get_response()
		if "404" in response:
			#print 2
			function2 = js_func["create_subdir"] % test_folder["%s_path" % dir_name]
			try:
				self.send_request(function2, "create_subdir()")
				response = self.get_response()
				assert "Success" in response
			except AssertionError:
				raise PreparationException("Failed to create %s; response is not successful." % dir_name)
		elif "Success" not in response:
			#print 3
			raise PreparationException("Failed to check the existence of %s; failed with status code not 404." % dir_name)
		try:
			#print 4
			self.send_request(function1, "check_existence()")
			response = self.get_response()
			assert "Success" in response
		except AssertionError:
			#print 5
			raise PreparationException("Failed to create %s." % dir_name)

	def subdirs(self):
		self.check_dir("subdir1")
		GenomeSpaceTest.subdir1_exists = True
		self.check_dir("subdir2")
		GenomeSpaceTest.subdir2_exists = True

	def remove_test_file(self, filename, file_path, testname):
		'''try:
			function1 = js_func["check_existence"] % file_path
			print function1
			self.send_request(function1, "check_existence()")
		except Exception as e:
			print "a"
			print e.__str__()
			raise PreparationException(e.__str__() + "Failed to check the existence of %s." % filename)
		response = self.get_response()
		print response
		if "Success" in response:'''
		function_d = js_func["delete"] % file_path
		try:
			#print "exists"
			self.send_request(function_d, "delete_data()")
			response = self.get_response()
			assert (("Success" in response) or ("404" in response))
		except Exception:
			raise PreparationException("Failed to delete the existing %s." % filename)
		try:
			#print "second check"
			function_c = js_func["check_existence"] % file_path
			self.send_request(function_c, "check_existence()")
			response = self.get_response()
			assert "404" in response
		except Exception as e:
			#print "b"
			raise PreparationException("Failed to prepare for the %s test." % testname)
		'''elif "404" not in response:
			raise PreparationException("Failed to check the existence of %s." % filename)'''

	def upload_test_file(self, filename, file_path, testname):
		try:
			self.uploading(filename, file_path)
		except Exception as e:
			if "Overriding an existing object" not in e.__str__():
				raise PreparationException(("Failed to prepare for the %s test." + e.__str__() ) % testname)

	def files(self):
		failures = []
		try:
			self.remove_test_file("file_to_upload.txt", gs_file_paths["file_to_upload_path"], "uploading")
			GenomeSpaceTest.upload_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.remove_test_file("after_rename.txt", gs_file_paths["after_rename_path"], "changing file name")
			self.upload_test_file("before_rename.txt", gs_file_paths["before_rename_path"], "changing file name")
			GenomeSpaceTest.rename_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.upload_test_file("file_for_pURL.txt", gs_file_paths["file_to_generate_public_URL_path"], "generating public URL")
			GenomeSpaceTest.generate_public_URL_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.upload_test_file("file_to_copy.txt", gs_file_paths["copy_source_path"], "copying data")
			self.remove_test_file("file_to_copy.txt", gs_file_paths["copy_target_path"]["folder"], "copying data")
			self.remove_test_file("file_to_copy.txt", gs_file_paths["copy_target_path"]["container"], "copying data")
			GenomeSpaceTest.copying_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.upload_test_file("file_to_move1.txt", gs_file_paths["move_source_path"]["folder"], "moving data")
			self.upload_test_file("file_to_move2.txt", gs_file_paths["move_source_path"]["container"], "moving data")
			self.remove_test_file("file_to_move1.txt", gs_file_paths["move_target_path"]["folder"], "moving data")
			self.remove_test_file("file_to_move2.txt", gs_file_paths["move_target_path"]["container"], "moving data")
			GenomeSpaceTest.moving_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.upload_test_file("file_to_delete.txt", gs_file_paths["file_to_delete_path"], "deleting data")
			GenomeSpaceTest.deleting_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			self.upload_test_file("file_to_publish.txt", gs_file_paths["file_to_publish_path"], "getting DOI")
			GenomeSpaceTest.publishing_file_test_ready = True
		except Exception as e:
			failures.append(e)
		if failures != []:
			report = ""
			for item in failures:
				report += item.__str__()
				report += "\n"
			raise PreparationException(report)

	#@staticmethod
	def test_3_setting_up(self):
		#self.driver = driver
		self.containers()
		self.subdirs()
		self.files()


