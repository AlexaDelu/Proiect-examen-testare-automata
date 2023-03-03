import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestEmag2(unittest.TestCase):
    def setUp(self):
        self.chrome = webdriver.Chrome()
        self.chrome.maximize_window()

 # Test login
    def test_login_account(self):
        self.chrome.get("https://auth.emag.net/login?adk=lT0TiUXFdv34SxlS")
        # Wait for the email input field to be visible
        email_input = WebDriverWait(self.chrome, 10).until(EC.visibility_of_element_located
                                                           ((By.ID, "_username")))
        email_input.send_keys("lxa_alexa@yahoo.com")
        submit_button = self.chrome.find_element(By.ID, "_username")
        submit_button.click()
        inainte_button = WebDriverWait(self.chrome, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn.btn-next")))
        inainte_button.click()
        password_input = WebDriverWait(self.chrome, 30).until(EC.visibility_of_element_located
                                                              ((By.ID, "_password")))
        password_input.send_keys("oriceparola")
        login_button= WebDriverWait(self.chrome, 20).until(EC.visibility_of_element_located
                                                           ((By.CSS_SELECTOR, ".btn.btn-primary")))
        login_button.click()

    def teardown(self):
        self.chrome.quit()

    if __name__ == '__main__':
        unittest.main()

