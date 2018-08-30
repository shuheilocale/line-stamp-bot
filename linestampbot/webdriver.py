from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import FirefoxProfile
import time

"""ドライバ生成"""
def create_driver(browser="chrome"):

    if browser == "chrome":
     driver = webdriver.Chrome("./driver/chromedriver.exe")
    else:
        custom_profile = FirefoxProfile()
        custom_profile.set_preference("dom.disable_beforeunload", True)

        
        driver = webdriver.Firefox(firefox_profile=custom_profile, executable_path="./driver/geckodriver.exe")
    driver.implicitly_wait(10)
    return driver


def find_element_by_css_selector_With_wait(driver, str, retry_count=10):
    for i in range(retry_count):
        try:
            elem = driver.find_element_by_css_selector(str)
            return elem
        except:
            time.sleep(2)
            pass
    return None

def find_elements_by_css_selector_With_wait(driver, str, retry_count=10):
    for i in range(retry_count):
        try:
            elem = driver.find_elements_by_css_selector(str)
            return elem
        except:
            time.sleep(2)
            pass
    return None