from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://genomespace.genome.edu.au")
assert "GenomeSpace" in driver.title
driver.close()
