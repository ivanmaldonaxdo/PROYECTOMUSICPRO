from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time
# Create your tests here.
class Hosttest(LiveServerTestCase):
    def testhomepage(self):
        options = options()
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.live_server_url)
        driver.get('http://127.0.0.1:8000')
        assert "hello , world" in driver.title
    # pass
