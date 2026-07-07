import pytest
from selenium import webdriver
from pages.login_page import LoginPage

@pytest.fixture
def driver():
    drv = webdriver.Firefox()
    yield drv          # test runs here
    drv.quit()          # runs after the test, even if it failed/raised
    
@pytest.fixture
def login_as(driver):
    def _login_as(username, password):
        loginPage = LoginPage(driver).load()
        loginPage.login(username, password)
        return loginPage
    return _login_as