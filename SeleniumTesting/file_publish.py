from genome_space_test import GenomeSpaceTest
from abc import ABCMeta
from constants import *
import unittest
from selenium.webdriver.support import expected_conditions as EC
import unicodedata

class FilePublish(GenomeSpaceTest):

	__metaclass__ = ABCMeta

	def test_8_get_DOI(self):
		if (not GenomeSpaceTest.logged_in):
			raise unittest.SkipTest("Skipped for failed login.")
		if (not GenomeSpaceTest.data_testing_swift_mounted):
			raise unittest.SkipTest("Skipped for failed mounting container.")
		function1 = js_func["get_tags"]
		try:
			self.send_request(function1, "get_tags()")
		except Exception as e:
			raise e
		try:
			self.wait.until(EC.alert_is_present())
			alert = self.driver.switch_to_alert()
			num_before = int(unicodedata.normalize('NFKD', alert.text).encode('ascii', 'replace'))
			alert.accept()
		except Exception as e:
			raise e
		function2 = js_func["get_doi"]
		try:
			self.send_request(function2, "get_doi()")
		except Exception as e:
			raise e
		try:
			response = self.get_response()
			assert "Success" in response
		except Exception as e:
			raise e
		try:
			self.send_request(function1, "get_tags()")
		except Exception as e:
			raise e
		try:
			self.wait.until(EC.alert_is_present())
			alert = self.driver.switch_to_alert()
			num_after = int(unicodedata.normalize('NFKD', alert.text).encode('ascii', 'replace'))
			alert.accept()
		except Exception as e:
			raise e