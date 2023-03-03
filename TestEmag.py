import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException

class TestEMag(unittest.TestCase):
    def setUp(self):
        self.chrome = webdriver.Chrome()
        self.chrome.maximize_window()
        self.chrome.get("https://www.emag.ro/")

#Test- Verificati ca noul url e corect
    def test_login_page_url(self):
        self.chrome.get("https://auth.emag.ro/user/login")
        self.assertEqual(self.chrome.current_url, "https://auth.emag.ro/user/login")

#Test verificare url cos este corect
    def test_cart_page(self):
        self.chrome.get("https://www.emag.ro/cart/products?ref=cart")
        self.assertEqual(self.chrome.current_url, "https://www.emag.ro/cart/products?ref=cart")

#Test -Verificare page title e corect
    def test_title(self):
        self.chrome.get('https://auth.emag.ro/user/login')
        time.sleep(5)  # wait for the page to fully load
        actual = self.chrome.title
        expected = "eMAG.ro - Libertate în fiecare zi"
        self.assertEqual(expected, actual, 'Page title is incorrect')

#Test verificare Emag se afiseaza pe pagina
    def test_element(self):
        self.chrome.get("https://www.emag.ro/")
        element = WebDriverWait(self.chrome, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='navbar-brand']/img[@alt='eMAG']")))
        assert element.is_displayed()

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
        select_product = self.chrome.find_element(By.XPATH, "//button[@data-offer-id='112924935']")
        select_product.click()
        wait = WebDriverWait(self.chrome, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-offer-id='112924935']")))
        actual = WebDriverWait(self.chrome, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h4[text()='Produsul a fost adaugat in cos']"))).text
        expected = "Produsul a fost adaugat in cos"
        self.assertEqual(expected, actual, 'Produsul nu a fost adaugat in cos')

#Test stergere produs din cos
    def test_remove_product_from_cart(self):
        self.chrome.get("https://www.emag.ro/cart/products?ref=cart")
        wait = WebDriverWait(self.chrome, 10)
        remove_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn-remove-product[data-line='112924935']")))
        remove_btn.click()

#Test afisare mesaj cos gol
    def test_empty_cart(self):
        self.chrome.get("https://www.emag.ro/cart/products?ref=cart")
        wait = WebDriverWait(self.chrome, 10)
        empty_cart_msg = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='cart-products']/div/div[1]/div[2]/div/div/p")))
        assert "Cosul tau de cumparaturi nu contine produse" in empty_cart_msg.text

# Test verificare buton donatie 5 lei este afisat
    def test_newsletter(self):
        self.chrome.get("https://www.emag.ro/")
        try:
            newsletter = self.chrome.find_element(By.CSS_SELECTOR, "h3.h1.mrg-sep-none")
            print("newsletter found: ", newsletter.text)
        except NoSuchElementException:
            print("newsletter not found on the page")

#Test "Oferta zilei" banner is present:
    def test_DailyOffer(self):
        self.chrome.get("https://www.emag.ro/")
        banner = self.chrome.find_element(By.CSS_SELECTOR, 'img[title="Rabla"]')
        assert banner.get_attribute("alt") == "Rabla"

#Test asistenta site
    def test_Help(self):
        self.chrome.get("https://www.emag.ro/help/?ref=hdr_help")
        search_box = self.chrome.find_element(By.NAME, "q")
        search_box.send_keys("retururi")
        search_box.send_keys(Keys.RETURN)
        self.assertIn("Help", self.chrome.title)

    def tearDown(self):
        self.chrome.quit()


if __name__ == '__main__':
    unittest.main()
