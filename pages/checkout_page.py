from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage():
    
    CHECKOUT_BUTTON = (By.ID, "checkout")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    COMPLETE = (By.CSS_SELECTOR, '[data-test="complete-text"]')
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        
    def checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
        self.wait.until(EC.presence_of_element_located(self.CONTINUE))
        
    def fillForm(self, firstName, lastName, postalCode):
        self.driver.find_element(*self.FIRST_NAME).send_keys(firstName)
        self.driver.find_element(*self.LAST_NAME).send_keys(lastName)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postalCode)
        self.driver.find_element(*self.CONTINUE).click()
        self.wait.until(EC.presence_of_element_located(self.FINISH))

    def finish(self):
        self.driver.find_element(*self.FINISH).click()
        self.wait.until(EC.presence_of_element_located(self.COMPLETE))
        
    def complete(self):
        confirmation = self.driver.find_element(*self.COMPLETE)
        return confirmation