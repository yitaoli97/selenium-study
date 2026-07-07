from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time


driver = webdriver.Firefox()
driver.get("https://www.saucedemo.com")

wait = WebDriverWait(driver, 3)
wait.until(EC.presence_of_element_located((By.ID, "user-name")))

driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

wait.until(EC.url_contains("inventory"))

print(driver.current_url)


# Negative test: log in with locked_out_user and assert the correct error message appears.
driver.get("https://www.saucedemo.com")
wait.until(EC.presence_of_element_located((By.ID, "user-name")))

driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

error = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
assert "Sorry, this user has been locked out." in error.text


# Add items to cart: log in, add 2 specific products to the cart by name, and verify the cart badge shows "2".
driver.get("https://www.saucedemo.com")
wait.until(EC.presence_of_element_located((By.ID, "user-name")))

driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

wait.until(EC.url_contains("inventory"))

driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

cart = driver.find_element(By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
assert "2" in cart.text


# Sort products: use the dropdown to sort by "Price (low to high)" and assert the resulting list is actually sorted (pull all product prices via a list of elements and check programmatically, don't eyeball it).
driver.find_element(By.CSS_SELECTOR, '[value="lohi"]').click()

# Class for price is class="inventory_item_price"
# Get them in a list and convert them all to floats
items = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

# Assert that the list is in sorted order
for i in range(0, len(items) - 1):
    lower = float(items[i].text.replace("$", ""))
    higher = float(items[i + 1].text.replace("$", ""))
    assert lower <= higher


driver.find_element(By.ID, "react-burger-menu-btn").click()
wait.until(EC.presence_of_element_located((By.ID, "reset_sidebar_link")))
driver.find_element(By.ID, "reset_sidebar_link").click()
driver.find_element(By.ID, "logout_sidebar_link").click()

# Full checkout flow: log in → add items → go to cart → checkout → fill in the form → assert order confirmation text.
driver.get("https://www.saucedemo.com")
wait.until(EC.presence_of_element_located((By.ID, "user-name")))

driver.find_element(By.ID, "user-name").send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()

wait.until(EC.url_contains("inventory"))

driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

driver.find_element(By.CSS_SELECTOR, '[data-test="shopping-cart-link"]').click()
wait.until(EC.url_contains("cart"))

driver.find_element(By.ID, "checkout").click()
wait.until(EC.url_contains("checkout"))

driver.find_element(By.ID, "first-name").send_keys("bob")
driver.find_element(By.ID, "last-name").send_keys("kent")
driver.find_element(By.ID, "postal-code").send_keys("ABCDEF")
driver.find_element(By.ID, "continue").click()


wait.until(EC.url_contains("step-two"))
driver.find_element(By.ID, "finish").click()

wait.until(EC.url_contains("complete"))
confirmation = driver.find_element(By.CSS_SELECTOR, '[data-test="complete-text"]')
assert "Your order has been dispatched, and will arrive just as fast as the pony can get there!" in confirmation.text

driver.find_element(By.ID, "react-burger-menu-btn").click()
wait.until(EC.presence_of_element_located((By.ID, "reset_sidebar_link")))
driver.find_element(By.ID, "reset_sidebar_link").click()
driver.find_element(By.ID, "logout_sidebar_link").click()


# Data-driven login test: refactor your login test to loop over all the different saucedemo usernames (standard_user, locked_out_user, problem_user, performance_glitch_user) and assert expected behavior per user.
USERS = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user"]
driver.get("https://www.saucedemo.com")
wait.until(EC.presence_of_element_located((By.ID, "user-name")))

for user in USERS:
    match user:
        case "standard_user":
            driver.get("https://www.saucedemo.com")
            wait.until(EC.presence_of_element_located((By.ID, "user-name")))

            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()

            wait.until(EC.url_contains("inventory"))

            driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
            driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()

            driver.find_element(By.CSS_SELECTOR, '[data-test="shopping-cart-link"]').click()
            wait.until(EC.url_contains("cart"))

            driver.find_element(By.ID, "checkout").click()
            wait.until(EC.url_contains("checkout"))

            driver.find_element(By.ID, "first-name").send_keys("bob")
            driver.find_element(By.ID, "last-name").send_keys("kent")
            driver.find_element(By.ID, "postal-code").send_keys("ABCDEF")
            driver.find_element(By.ID, "continue").click()


            wait.until(EC.url_contains("step-two"))
            driver.find_element(By.ID, "finish").click()

            wait.until(EC.url_contains("complete"))
            confirmation = driver.find_element(By.CSS_SELECTOR, '[data-test="complete-text"]')
            assert "Your order has been dispatched, and will arrive just as fast as the pony can get there!" in confirmation.text

            driver.find_element(By.ID, "react-burger-menu-btn").click()
            wait.until(EC.presence_of_element_located((By.ID, "reset_sidebar_link")))
            driver.find_element(By.ID, "reset_sidebar_link").click()
            driver.find_element(By.ID, "logout_sidebar_link").click()
        
        case "locked_out_user":
            driver.get("https://www.saucedemo.com")
            wait.until(EC.presence_of_element_located((By.ID, "user-name")))

            driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()

            error = driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
            assert "Sorry, this user has been locked out." in error.text
            
            
        case "problem_user":
            driver.get("https://www.saucedemo.com")
            driver.find_element(By.ID, "user-name").send_keys(user)
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()
            
            wait.until(EC.url_contains("inventory"))

            print("logged in as problem_user")
            driver.find_element(By.CSS_SELECTOR, '[value="lohi"]').click()
            items = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
            
            inOrder = True

            for i in range(0, len(items) - 1):
                lower = float(items[i].text.replace("$", ""))
                higher = float(items[i + 1].text.replace("$", ""))
                if lower >= higher:
                    inOrder = False
            
            try:
                assert inOrder == False
            
            except AssertionError:
                print("problem_user lohi should not work, but did.")
            
            link = driver.find_element(By.ID, "item_4_img_link")
            img = link.find_element(By.TAG_NAME, "img")
            src = img.get_attribute("src")
            
            link2 = driver.find_element(By.ID, "item_0_img_link")
            img2 = link2.find_element(By.TAG_NAME, "img")
            src2 = img2.get_attribute("src")
            
            try:
                assert src == src2
                
            except AssertionError:
                    print(f"Items 0 and 4 have different images, but they should be the same wrong image for problem_user")
                    
            name = driver.find_element(By.ID, "item_4_title_link").text
            link2.click()
            wait.until(EC.url_contains("inventory-item"))
            name2 = driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text
            try:
                assert name != name2
                
            except AssertionError:
                    print("problem_user should bring up wrong item when clicking one, but it was correct.")
            
            driver.find_element(By.ID, "react-burger-menu-btn").click()
            wait.until(EC.presence_of_element_located((By.ID, "reset_sidebar_link")))
            driver.find_element(By.ID, "reset_sidebar_link").click()
            driver.find_element(By.ID, "logout_sidebar_link").click()
                
        case "performance_glitch_user":
            driver.get("https://www.saucedemo.com")
            
            # need to use time because delay happens inside .click() call
            start = time.time()
            
            driver.find_element(By.ID, "user-name").send_keys(user)
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()
            wait10 = WebDriverWait(driver, 10)
            clickWait = time.time() - start
            assert clickWait > 2, f"Expected performance_glitch_user login to be slow, took {clickWait:.2f}s"
            
            wait10.until(EC.url_contains("inventory"))
            print(f"URL changed at {time.time() - start:.2f}s")

            wait10.until(EC.presence_of_element_located((By.ID, "item_0_img_link")))
            print(f"element present at {time.time() - start:.2f}s")

            wait10.until(EC.visibility_of_element_located((By.ID, "item_0_img_link")))
            print(f"element visible at {time.time() - start:.2f}s")

            wait10.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print(f"document ready at {time.time() - start:.2f}s")
            
driver.quit()

