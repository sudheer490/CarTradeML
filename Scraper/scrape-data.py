from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import pandas as pd
driver = webdriver.Chrome()
def get_anchors(path,driver = driver):
    anchor_elements = driver.find_elements(By.XPATH, path)
    # Iterate through the anchor elements and get their href attributes
    href_list = [anchor.get_attribute("href") for anchor in anchor_elements]
    return href_list
outfile = 'sedan.csv'
base_url = 'https://www.vroom.com/cars?body_style=sedan&zip=33613'



driver.get(base_url)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Find the navigation element with page links
page_urls = [base_url + '&page='+ str(page) for page in range(1, 45)]






data = {}
cntr = 0
for page_url in tqdm(page_urls):
    driver.get(page_url)
    pth = "//a[contains(@class, 'listing-link')]"
    hrefs = get_anchors(path = pth)
    for hr in tqdm(hrefs):
        try:
            desired_href = hr
            driver.get(hr)
            time.sleep(1)
            button = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]')
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(2)
            button = driver.find_element(By.XPATH, '//*[@id="tab-2"]')
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            features_ul = soup.find('ul', class_='highlighted-features-list')
            if features_ul:
                features = [feature.get_text(strip=True) for feature in features_ul.find_all('li')]
            button.click()
            time.sleep(1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            miles_text = soup.find('span', class_='miles').get_text(strip=True)
            price_span = soup.find('span', class_='u-pos-r')
            price = price_span.get_text(strip=True)
            details_tables = soup.find_all('div', class_='details-table')
            table_data = {}
            current_property_name = None
            table_data['html']= details_tables
            table_data['miles']= miles_text
            table_data['source'] = hr 
            table_data['features'] = features
            table_data['price'] = price
            data[cntr] = table_data
            driver.back()
            cntr+=1
            try:
                df = pd.DataFrame(data)
                df.to_csv('tmps.csv')
            except:
                pass
        except:
            pass
df = pd.DataFrame(data)
df.to_csv(outfile)
driver.quit()


