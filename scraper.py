from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from config import SEARCH_TERM, BASE_URL

def init_driver():
    # initialize and return a chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(60) # wait 5s to elements to appear
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


def search_products(driver):
    # perform a product search
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.clear()
    search_box.send_keys(SEARCH_TERM)
    search_box.submit()
    #time.sleep(2) # let results load

    # captcha bloking us 
    while "captcha" in driver.page_source.lower():
        print("captcha detected solve it manually in the browser")
        input("press enter after solving captcha to continue")

    # verify we got results
    assert "results for " in driver.page_source.lower()
    print("search completed")


def main():
    print("starting script...")
    driver = init_driver()
    try:
        print(f"loading {BASE_URL}...")
        driver.get(BASE_URL)
        print('homepage loaded')

        search_products(driver)
    except Exception as e :
        print(f"critical error: {e}")
    finally:
        print("quitting driver..")
        driver.quit()
        print("script completed")


if __name__ == "__main__":
    main()  
