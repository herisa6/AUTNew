import time
import unittest
from selenium import webdriver

class Test_Chrome (unittest.TestCase):
        
    @classmethod
    def setUpClass(self):
        options = webdriver. ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser = webdriver.Remote(   
        command_executor='http://localhost:4444/wd/hub',
        options=options
        )

    def test_chrome (self):
        self.browser.get("https://www.google.com")
        self.browser.save_screenshot('screenshot.png')
        self.assertIn('Google', self.browser.title)

    @classmethod
    def tearDownClass (self):
        self.browser.quit()
