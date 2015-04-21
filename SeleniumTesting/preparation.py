from mount_disconnect import CloudStorage
from constants import *

def container(driver):
	CloudStorage.mounting(container_names["for data tests"][1])
	try:
		assert "swift:" + container_names["for data tests"][0] in driver.page_source
	except AssertionError:
		time.sleep(8)
		mounting(container_names["for data tests"][0])
	try:
		assert "swift:" + container_names["for data tests"][1] in driver.page_source
		global data_testing_swift_mounted
		data_testing_swift_mounted = True
	except AssertionError:
		time.sleep(8)
		mounting(container_names["for data tests"][1])
		data_testing_swift_mounted = True

class Preparation:

	@classmethod
	def prepare_for_tests(cls):
		driver = cls.driver
		container(driver)

