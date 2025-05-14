from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def init_driver():
    # initialize and return a chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5) # wait 5s to elements to appear
    return driver
def test_amazon_load():
    #test if we can load amazon
    driver = init_driver()
    try :
        driver.get("https://www.amazon.com")
        assert "Amazon.com" in driver.title
        print("amazon load successfully")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_amazon_load()
