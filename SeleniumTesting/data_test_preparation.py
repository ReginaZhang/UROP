#from mount_disconnect import CloudStorage
from constants import *
from selenium.webdriver.support.ui import WebDriverWait
import time

from genome_space_test import GenomeSpaceTest


class DataTestPreparation(GenomeSpaceTest):

	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(driver, 60)

	#@staticmethod
	def container(self):
		self.mounting(container_names["for data tests"][1])
		try:
			assert "swift:" + container_names["for data tests"][0] in self.driver.page_source
		except AssertionError:
			time.sleep(8)
			self.mounting(container_names["for data tests"][0])
		try:
			assert "swift:" + container_names["for data tests"][1] in self.driver.page_source
			#global data_testing_swift_mounted
			GenomeSpaceTest.data_testing_swift_mounted = True
		except AssertionError:
			time.sleep(8)
			self.mounting(container_names["for data tests"][1])
			GenomeSpaceTest.data_testing_swift_mounted = True

	#@staticmethod
	def prepare_for_tests(self):
		#self.driver = driver
		self.container()

