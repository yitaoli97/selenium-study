from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Navbar():
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    RESET = (By.ID, "reset_sidebar_link")
    LOGOUT = (By.ID, "logout_sidebar_link")
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
    
    def logout(self):
        self.driver.find_element(*self.MENU_BUTTON).click()
        self.wait.until(EC.presence_of_element_located(self.RESET))
        self.wait.until(EC.presence_of_element_located(self.LOGOUT))
        self.driver.find_element(*self.RESET).click()
        self.driver.find_element(*self.LOGOUT).click()