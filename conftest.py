import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    drv = webdriver.Firefox(options=options)
    yield drv          # test runs here
    drv.quit()          # runs after the test, even if it failed/raised
    
@pytest.fixture
def login_as(driver):
    def _login_as(username, password):
        loginPage = LoginPage(driver).load()
        loginPage.login(username, password)
        return loginPage
    return _login_as