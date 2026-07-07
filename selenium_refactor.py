from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.navbar import Navbar
import time

# init driver and wait
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 5)
navbar = Navbar(driver)


USERS = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user"]
PASSWORD = "secret_sauce"

try:
    for user in USERS:
        match user:
            case "standard_user":
                # init login and wait for page to load
                loginPage = LoginPage(driver).load()
                
                # login and wait for inventory to load
                loginPage.login(user, PASSWORD)
                wait.until(EC.url_contains("inventory"))

                # init inventory
                inventoryPage = InventoryPage(driver)
                
                inventoryPage.addToCart("sauce-labs-backpack")
                inventoryPage.addToCart("sauce-labs-bike-light")
                
                count = inventoryPage.getCartCount()
                assert count == "2"
                
                inventoryPage.goToCart()
                wait.until(EC.url_contains("cart"))
                
                checkoutPage = CheckoutPage(driver)
                checkoutPage.checkout()
                checkoutPage.fillForm("bob", "kent", "ABCDEF")
                checkoutPage.finish()
                confirmation = checkoutPage.complete()
                assert "Your order has been dispatched, and will arrive just as fast as the pony can get there!" in confirmation.text

                navbar.logout()
                
            
            case "locked_out_user":
                loginPage = LoginPage(driver).load()
                loginPage.login(user, PASSWORD)
                assert "Sorry, this user has been locked out." in loginPage.getErrorText()
                
                
            case "problem_user":
                loginPage = LoginPage(driver).load()
                loginPage.login(user, PASSWORD)
                wait.until(EC.url_contains("inventory"))

                print("logged in as problem_user")
                inventoryPage = InventoryPage(driver)
                inventoryPage.sortBy("lohi")
                prices = inventoryPage.getPrices()
                
                inOrder = True

                for i in range(0, len(prices) - 1):
                    lower = float(prices[i].text.replace("$", ""))
                    higher = float(prices[i + 1].text.replace("$", ""))
                    if lower >= higher:
                        inOrder = False
                
                assert not inOrder, "problem_user lohi should not work, but did."
                
                link = driver.find_element(By.ID, "item_4_img_link")
                img = link.find_element(By.TAG_NAME, "img")
                src = img.get_attribute("src")
                
                link2 = driver.find_element(By.ID, "item_0_img_link")
                img2 = link2.find_element(By.TAG_NAME, "img")
                src2 = img2.get_attribute("src")

                assert src == src2, "Items 0 and 4 should share the same wrong image for problem_user"
                        
                name = driver.find_element(By.ID, "item_4_title_link").text
                link2.click()
                wait.until(EC.url_contains("inventory-item"))
                name2 = driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]').text
                assert name != name2, "problem_user should navigate to the wrong item, but it didn't"
                
                navbar.logout()
                    
            case "performance_glitch_user":
                # need to use time because delay happens inside .click() call
                start = time.time()
                
                loginPage = LoginPage(driver).load()
                loginPage.login(user, PASSWORD)
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
                
                navbar.logout()
finally:
    driver.quit()
                


