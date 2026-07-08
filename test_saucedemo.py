from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from pages.navbar import Navbar
import time

PASSWORD = "secret_sauce"


def test_standard_user_can_complete_checkout(driver, login_as):
    login_as("standard_user", PASSWORD)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_contains("inventory"))

    inventory_page = InventoryPage(driver)
    inventory_page.addToCart("sauce-labs-backpack")
    inventory_page.addToCart("sauce-labs-bike-light")
    assert inventory_page.getCartCount() == "1"

    inventory_page.goToCart()
    wait.until(EC.url_contains("cart"))

    checkout_page = CheckoutPage(driver)
    checkout_page.checkout()
    checkout_page.fillForm("bob", "kent", "ABCDEF")
    checkout_page.finish()

    confirmation = checkout_page.complete()
    assert "Your order has been dispatched, and will arrive just as fast as the pony can get there!" in confirmation.text


def test_locked_out_user_sees_error(login_as):
    login_page = login_as("locked_out_user", PASSWORD)

    assert "Sorry, this user has been locked out." in login_page.getErrorText()


def test_problem_user_has_known_bugs(driver, login_as):
    login_as("problem_user", PASSWORD)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_contains("inventory"))

    inventory_page = InventoryPage(driver)
    inventory_page.sortBy("lohi")
    prices = [float(p.text.replace("$", "")) for p in inventory_page.getPrices()]
    assert prices != sorted(prices), "problem_user's lohi sort should be broken, but it worked!"

    link4 = driver.find_element(By.ID, "item_4_img_link")
    src4 = link4.find_element(By.TAG_NAME, "img").get_attribute("src")

    link0 = driver.find_element(By.ID, "item_0_img_link")
    src0 = link0.find_element(By.TAG_NAME, "img").get_attribute("src")

    assert src4 == src0, "Items 0 and 4 should share the same wrong image for problem_user"

    name4 = driver.find_element(By.ID, "item_4_title_link").text
    link0.click()
    wait.until(EC.url_contains("inventory-item"))
    clicked_name = driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text

    assert name4 != clicked_name, "problem_user should navigate to the wrong item, but it didn't"



def test_performance_glitch_user_login_is_slow(driver, login_as):

    start = time.time()
    login_as("performance_glitch_user", PASSWORD)
    click_duration = time.time() - start

    assert click_duration > 2, f"Expected performance_glitch_user login to be slow, took {click_duration:.2f}s"

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory"))
