'''
Module created on 08/12/2014

@author: Regina Zhang

'''

import unittest
from abc import ABCMeta
from GStestexceptions import *
from constants import *
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from _codecs import register
from selenium.webdriver.common.action_chains import ActionChains
import register_login as rl

class DataSharing():
    
    __metaclass__ = ABCMeta
    
    def test_5a_generate_public_URL(self):
        