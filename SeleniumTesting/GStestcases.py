'''
Module created on 26/11/2014

@author: Regina Zhang

'''

import unittest
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#from GStestexceptions import *
from constants import *
#import sys
import time
from abc import ABCMeta, abstractmethod
#from pip._vendor.requests.models import Response
from registration_login import RegistrationLogin
from mount_disconnect import CloudStorage
from data_manipulation import DataManipulation
from data_sharing import DataSharing
from data_storing import DataStoring
from data_to_GVL import DataToGVL
from data_test_preparation import DataTestPreparation


#base_window = None

class GSTestCases(RegistrationLogin, CloudStorage, DataManipulation, DataSharing, DataStoring, DataToGVL):

    __metaclass__ = ABCMeta

    

