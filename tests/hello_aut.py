import unittest, sys
from selenium import webdriver
from selenium.webdriver.common.by import By

class AutTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = 'http://localhost:4444'

        # Testing with Firefox
        self.browser_firefox = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_firefox.quit)

        # Testing with Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser_chrome = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_chrome.quit)

        # Testing with Edge
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser_edge = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_edge.quit)

    def test_homepage(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"

        # Testing with Firefox
        self.browser_firefox.get(url)
        self.browser_firefox.save_screenshot('screenshot_firefox.png')
        expected_result = "Welcome back, Guest!"      
        actual_result = self.browser_firefox.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result.text)

        # Testing with Chrome
        self.browser_chrome.get(url)
        self.browser_chrome.save_screenshot('screenshot_chrome.png')
        actual_result_chrome = self.browser_chrome.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result_chrome.text)

        # Testing with Edge
        self.browser_edge.get(url)
        self.browser_edge.save_screenshot('screenshot_edge.png')
        actual_result_edge = self.browser_edge.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result_edge.text)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
