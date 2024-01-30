import unittest, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

class AutTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        server = 'http://localhost:4444'

        # Firefox
        self.browser_firefox = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_firefox.quit)

        # Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser_chrome = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_chrome.quit)

        # Edge
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        self.browser_edge = webdriver.Remote(command_executor=server, options=options)
        self.addCleanup(self.browser_edge.quit)

    def run_test(self, browser, url):
        browser.get(url)
        browser.save_screenshot(f'screenshot_{browser.name.lower()}.png')
        expected_result = "Welcome back, Guest!"
        actual_result = browser.find_element(By.TAG_NAME, 'p')
        self.assertIn(expected_result, actual_result.text)

    def test_parallel_execution(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(self.run_test, self.browser_firefox, url)
            executor.submit(self.run_test, self.browser_chrome, url)
            executor.submit(self.run_test, self.browser_edge, url)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
