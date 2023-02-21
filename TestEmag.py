import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TestEMag(unittest.TestCase):
    def setUp(self):
        self.chrome = webdriver.Chrome()
        self.chrome.maximize_window()
        self.chrome.get("https://www.emag.ro/")

#Test- Verificati ca noul url e corect
    def test_login_page_url(self):
        self.chrome.get("https://auth.emag.ro/user/login")
        self.assertEqual(self.chrome.current_url, "https://auth.emag.ro/user/login")

#Test -Verificare page title e corect
    def test_title(self):
        self.chrome.get('https://auth.emag.ro/user/login')
        time.sleep(5)  # wait for the page to fully load
        actual = self.chrome.title
        expected = "eMAG.ro - Libertate în fiecare zi"
        self.assertEqual(expected, actual, 'Page title is incorrect')

#Test- cautare produs
    def test_search_laptop(self):
        search_box = self.chrome.find_element(By.NAME, "query")
        search_box.send_keys("laptop lenovo v15 g2")
        search_box.send_keys(Keys.RETURN)
        wait = WebDriverWait(self.chrome, 10)
        wait.until(EC.title_contains("laptop lenovo v15 g2"))
        actual = self.chrome.current_url
        expected = "https://www.emag.ro/search/laptop%20lenovo%20v15%20g2?ref=effective_search"
        self.assertEqual(expected, actual, ' Url is incorrect')

#Test- adaugare produs in cos
    def test_add_to_cart(self):
        self.chrome.get("https://www.emag.ro/search/laptop%20lenovo%20v15%20g2?ref=effective_search%22")
        select_product = self.chrome.find_element(By.XPATH, "//button[@data-offer-id='9479361']")
        select_product.click()
        wait = WebDriverWait(self.chrome, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-offer-id='9479361']")))
        actual = WebDriverWait(self.chrome, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h4[text()='Produsul a fost adaugat in cos']"))).text
        expected = "Produsul a fost adaugat in cos"
        self.assertEqual(expected, actual, 'Produsul nu a fost adaugat in cos')

#Test stergere produs din cos
    def test_remove_product_from_cart(self):
        self.chrome.get("https://www.emag.ro/cart/products?ref=cart")
        wait = WebDriverWait(self.chrome, 10)
        remove_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-remove-product[data-line='9479361']")))
        remove_btn.click()
        empty_cart_msg = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cart-empty")))
        assert "Cosul tau de cumparaturi este gol" in empty_cart_msg.text


#Test "Oferta zilei" banner is present:
    def test_DailyOffer(self):
        self.chrome.get("https://www.emag.ro/")
        banner = self.chrome.find_element(By.CSS_SELECTOR, 'img[title="Rabla"]')
        assert banner.get_attribute("alt") == "Rabla"

#Test login nereusit deoarece site-ul utilizeaza captcha
    def test_login_account(self):
        self.chrome.get("https://auth.emag.ro/user/login")
        # Wait for the email input field to be visible
        email_input = WebDriverWait(self.chrome, 10).until(
            EC.visibility_of_element_located((By.ID, "user_login_email"))
        )
        email_input.send_keys("lxa_alexa@yahoo.com")
        submit_button = self.chrome.find_element(By.ID, "user_login_continue")
        submit_button.click()
        password_input = WebDriverWait(self.chrome, 10).until(
            EC.visibility_of_element_located((By.ID, "user_login_password"))
        )
        password_input.send_keys("oriceparola")
        submit_button = self.chrome.find_element(By.ID, "user_login_continue")
        submit_button.click()

    def tearDown(self):
        self.chrome.quit()


if __name__ == '__main__':
    unittest.main()
