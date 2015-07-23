#from mount_disconnect import CloudStorage
from constants import *
from selenium.webdriver.support.ui import WebDriverWait
import time
from GStestexceptions import *

from genome_space_test import GenomeSpaceTest as GST


class DataTestPreparation(GST):

	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, 60)

	#@staticmethod
	def containers(self):
		#self.mounting(container_names["for data tests"][1])
		try:
			time.sleep(10)
			assert "swift:" + GST.container_names["for data tests"][0] in self.driver.page_source
		except AssertionError:
			self.mounting(GST.container_names["for data tests"][0])
			time.sleep(8)
			self.refresh_page()
			time.sleep(8)
		try:
			assert "swift:" + GST.container_names["for data tests"][1] in self.driver.page_source
			#global data_testing_swift_mounted
			#GST.data_testing_swift_mounted = True
		except AssertionError:
			self.mounting(GST.container_names["for data tests"][1])
			time.sleep(8)
			self.refresh_page()
			time.sleep(8)
			#GST.data_testing_swift_mounted = True
		try:
			assert "swift:" + GST.container_names["for data tests"][0] in self.driver.page_source
			assert "swift:" + GST.container_names["for data tests"][1] in self.driver.page_source
			GST.data_testing_swift_mounted = True
			#self.refresh_page()
		except AssertionError:
			raise PreparationException("Containers for file tests are not connected and failed to mount them.")

	def check_dir(self, path, dir_name):
		try:
			function1 = js_func["check_existence"] % path
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
			function2 = js_func["create_subdir"] % path
			try:
				self.send_request(function2, "create_subdir()")
				response = self.get_response()
				assert "Success" in response
			except AssertionError:
				raise PreparationException("Failed to create %s; response is not successful." % dir_name)
		elif "Success" not in response:
			#print 3
			raise PreparationException(("Failed to check the existence of %s; failed with status code not 404." % dir_name) + response)
		try:
			#print 4
			self.send_request(function1, "check_existence()")
			response = self.get_response()
			assert "Success" in response
		except AssertionError:
			#print 5
			raise PreparationException("Failed to create %s." % dir_name)

	def subdirs(self):
		self.check_dir(GST.gs_folder_paths["dir1_path"], "dir1")
		GST.dir1_exists = True
		self.check_dir(GST.gs_folder_paths["dir2_path"], "dir2")
		GST.dir2_exists = True
		if GST.default_folder_to_be_used:
			self.check_dir(default_folder_paths["dir1_path"], "default dir1")
			self.check_dir(default_folder_paths["dir2_path"], "default dir2")
			GST.default_folders_exists = True

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

	def upload_test_file(self, filename, local_path, gs_path, testname):
		try:
			f = open(local_path, "r")
			data = f.read()
			print data
		except Exception as e:
			raise PreparationException(("Failed to prepare for the %s test. " + e.__class__.__name__ + " " + e.__str__() ) % testname)
		try:
			self.uploading(filename, gs_path, data)
		except Exception as e:
			if not ("Overriding an existing object" in e.__str__()):
				raise PreparationException(("Failed to prepare for the %s test." + e.__str__() ) % testname)

	def get_file_name(self, path):
		tokens = path.split("/")
		name = tokens[-1]
		return name

	def files(self):
		failures = []
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_upload_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_upload_path"], "uploading")
			GST.upload_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["after_rename_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["after_rename_path"], "changing file name")
			file_name = self.get_file_name(GST.gs_file_paths["file_to_rename_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_rename_path"], "changing file name")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_rename_path"], GST.gs_file_paths["file_to_rename_path"], "changing file name")
			GST.rename_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_generate_public_URL_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_generate_public_URL_path"], "generating public URL")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_generate_public_URL_path"], GST.gs_file_paths["file_to_generate_public_URL_path"], "generating public URL")
			GST.generate_public_URL_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_copy_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_copy_source_path"], "copying data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_copy_source_path"], GST.gs_file_paths["file_to_copy_source_path"], "copying data")
			file_name = self.get_file_name(GST.gs_file_paths["copy_to_folder_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["copy_to_folder_target_path"], "copying data")
			file_name = self.get_file_name(GST.gs_file_paths["copy_to_container_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["copy_to_container_target_path"], "copying data")
			GST.copying_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_move_to_folder_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_move_to_folder_source_path"], "moving data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_move_to_folder_source_path"], GST.gs_file_paths["file_to_move_to_folder_source_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["file_to_move_to_container_source_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_move_to_container_source_path"], "moving data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_move_to_container_source_path"], GST.gs_file_paths["file_to_move_to_container_source_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["move_to_folder_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["move_to_folder_target_path"], "moving data")
			file_name = self.get_file_name(GST.gs_file_paths["move_to_container_target_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["move_to_container_target_path"], "moving data")
			GST.moving_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_delete_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_delete_path"], "deleting data")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_delete_path"], GST.gs_file_paths["file_to_delete_path"], "deleting data")
			GST.deleting_data_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_publish_path"])
			#self.remove_test_file(file_name, GST.gs_file_paths["file_to_publish_path"], "getting DOI")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_publish_path"], GST.gs_file_paths["file_to_publish_path"], "getting DOI")
			GST.publishing_file_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_import_with_URL_path"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_import_with_URL_path"], "importing file using public url")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_import_with_URL_path"], GST.gs_file_paths["file_to_import_with_URL_path"], "importing file using public url")
			GST.importing_url_test_ready = True
		except Exception as e:
			failures.append(e)
		try:
			file_name = self.get_file_name(GST.gs_file_paths["file_to_launch_GVL_with"])
			self.remove_test_file(file_name, GST.gs_file_paths["file_to_launch_GVL_with"], "launching Galaxy with file")
			self.upload_test_file(file_name, GST.local_file_paths["file_to_launch_GVL_with"], GST.gs_file_paths["file_to_launch_GVL_with"], "launching Galaxy with file")
			GST.launch_GVL_with_file_test_ready = True
		except Exception as e:
			failures.append(e)
		if failures != []:
			report = ""
			for item in failures:
				report = report + item.__class__.__name__ + ": " + item.__str__() + "\n"
			raise PreparationException(report)

	#@staticmethod
	def test_3_setting_up(self):
		#self.driver = driver
		self.containers()
		self.subdirs()
		self.files()


