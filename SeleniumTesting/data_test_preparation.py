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
		a = ("swift:" + container_names["for data tests"][0] in self.driver.page_source)
		b = ("swift:" + container_names["for data tests"][1] in self.driver.page_source)
		try:
			assert a
		except AssertionError:
			self.mounting(container_names["for data tests"][0])
			time.sleep(8)
		try:
			assert b
			#global data_testing_swift_mounted
			#GenomeSpaceTest.data_testing_swift_mounted = True
		except AssertionError:
			self.mounting(container_names["for data tests"][1])
			time.sleep(8)
			#GenomeSpaceTest.data_testing_swift_mounted = True
		try:
			print a
			print b
			assert a and b
			self.refresh_page()
		except AssertionError:
			raise PreparationException("Containers for file tests are not connected and failed to mount them.")

	#def folder

	#@staticmethod
	def prepare_for_tests(self):
		#self.driver = driver
		self.containers()

