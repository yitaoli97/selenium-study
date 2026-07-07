from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage:
    URL = "https://www.saucedemo.com"

    CART_BADGE = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
    CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
    SORT_DROPDOWN = (By.CSS_SELECTOR, '[data-test="product-sort-container"]')
    PRICES = (By.CLASS_NAME, "inventory_item_price")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        
    def addToCart(self, id):
        locator = (By.ID, f"add-to-cart-{id}")
        self.driver.find_element(*locator).click()
        return self
    
    def getCartCount(self):
        cart = self.driver.find_element(*self.CART_BADGE)
        return cart.text
        
    def sortBy(self, value):
        from selenium.webdriver.support.ui import Select
        # * syntax expands tuple into separate arguments
        Select(self.driver.find_element(*self.SORT_DROPDOWN)).select_by_value(value)
        
    def getPrices(self):
        return self.driver.find_elements(*self.PRICES)
    
    def goToCart(self):
        self.driver.find_element(*self.CART_LINK).click()
    
    