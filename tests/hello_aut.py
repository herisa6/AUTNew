import unittest, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor

def initialize_firefox():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    server = 'http://localhost:4444'
    return webdriver.Remote(command_executor=server, options=options)

def initialize_chrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    server = 'http://localhost:4444'
    return webdriver.Remote(command_executor=server, options=options)

def initialize_edge():
    options = webdriver.EdgeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    server = 'http://localhost:4444'
    return webdriver.Remote(command_executor=server, options=options)

def run_test(browser, url):
    browser.get(url)
    browser.save_screenshot(f'screenshot_{browser.capabilities["browserName"].lower()}.png')
    expected_result = "Welcome back, Guest!"
    actual_result = browser.find_element(By.TAG_NAME, 'p')
    assert expected_result in actual_result.text

class AutTest(unittest.TestCase):

    def setUp(self):
        self.browser_firefox = initialize_firefox()
        self.addCleanup(self.browser_firefox.quit)

        self.browser_chrome = initialize_chrome()
        self.addCleanup(self.browser_chrome.quit)

        self.browser_edge = initialize_edge()
        self.addCleanup(self.browser_edge.quit)

    def test_parallel_execution(self):
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = "http://localhost"

        with ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(run_test, self.browser_firefox, url)
            executor.submit(run_test, self.browser_chrome, url)
            executor.submit(run_test, self.browser_edge, url)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
