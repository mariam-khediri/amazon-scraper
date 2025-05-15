from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from config import SEARCH_TERM, BASE_URL
import pandas as pd
from datetime import datetime
import os



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

SELECTORS = {
    'product_container': 'div.s-result-item[data-component-type="s-search-result"]',
    'title': 'span.a-size-medium.a-color-base.a-text-normal',
    'price_whole': 'span.a-price-whole',
    'price_fraction': 'span.a-price-fraction',
    'rating': 'span.a-icon-alt',
    'review_count': 'span.a-size-base.s-underline-text'
} 

def scrape_product(product_element):
    """Extracts detailed product data from a single product element"""
    data = {
        'title': get_text_or_none(product_element, SELECTORS['title']),
        'price': format_price(product_element),
        'rating': clean_rating(get_text_or_none(product_element, SELECTORS['rating'])),
        'reviews': get_text_or_none(product_element, SELECTORS['review_count']),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return {k: v for k, v in data.items() if v is not None}

# Helper functions
def get_text_or_none(element, selector):
    try:
        return element.find_element(By.CSS_SELECTOR, selector).text.strip()
    except:
        return None

def format_price(element):
    try:
        whole = element.find_element(By.CSS_SELECTOR, SELECTORS['price_whole']).text
        fraction = element.find_element(By.CSS_SELECTOR, SELECTORS['price_fraction']).text
        return f"${whole}.{fraction}"
    except:
        return None

def clean_rating(rating_text):
    return rating_text.split()[0] if rating_text else None

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



def save_to_csv(data, filename=None, folder='outputs', include_timestamp=True):
    """
    Saves scraped data to CSV with automatic file naming and directory creation
    
    Args:
        data (list): List of dictionaries containing product data
        filename (str): Optional custom filename (without extension)
        folder (str): Output directory name
        include_timestamp (bool): Whether to add timestamp to filename
    
    Returns:
        str: Path to the saved file
    """
    if not data:
        print(" No data to save")
        return None

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs(folder, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        filename = f"amazon_{SEARCH_TERM.lower().replace(' ', '_')}"
        if include_timestamp:
            filename += f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Add CSV extension if missing
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    filepath = os.path.join(folder, filename)
    
    try:
        # Save with proper encoding and error handling
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"Successfully saved {len(df)} records to {filepath}")
        return filepath
    except Exception as e:
        print(f" Failed to save CSV: {str(e)}")
        # Attempt backup save method
        try:
            temp_path = os.path.join(folder, f"temp_{filename}")
            df.to_csv(temp_path, index=False)
            print(f" Saved backup to {temp_path}")
            return temp_path
        except:
            print(" Critical backup save failed")
            return None

if __name__ == "__main__":
    main()  
