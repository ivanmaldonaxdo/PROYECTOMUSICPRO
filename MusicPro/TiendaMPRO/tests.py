from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
import time
# Create your tests here.
class Hosttest(LiveServerTestCase):
    def testhomepage(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/login/')
        assert " hello , world" in driver.title
    # pass
