from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com"
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        
    def load(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        return self
    
    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        
    def getErrorText(self):
        self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
        error = self.driver.find_element(By.CSS_SELECTOR, '[data-test="error"]')
        return error.text