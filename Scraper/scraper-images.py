from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image
from tqdm import tqdm

def get_image(img_result,file_name,index):
    file_path = './new_images/' + file_name + '.jpg'
    result = requests.get(img_result, allow_redirects=True, timeout=10)
    open(file_path, 'wb').write(result.content)
    #print(result)
    img = Image.open(file_path)
    img = img.convert('RGB')
    img.save(file_path, 'JPEG')
    locations['image_location'].append(file_path)
    #print('Image saved from https.')



df = pd.read_excel('master_data.xlsx')
df = df[['year','make','model']].drop_duplicates()
df['make'] = df.make.map(lambda x: 'mercedes-benz' if x=='mercedes' else x)
df['model'] = df.model.map(lambda x: str(x).replace('benz ','' ))
df['make'] = df.make.map(lambda x: 'alfa-romeo' if x=='alfa' else x)
df['model'] = df.model.map(lambda x: str(x).replace('romeo ','' ))

df['search'] = df['make']+'_' + df.model.str.replace(' ','-').astype(str) + '_' + df.year.fillna(2023).astype(int).astype(str) 
print(df.shape)

locations = {'image_location':[]}
driver = webdriver.Chrome()
index=-1
for search_term in tqdm(df.search.values[191:].ravel()):
    print(search_term,sep='')
    index+=1
    try:
        url_to_go = 'https://www.thecarconnection.com/overview/' + search_term  
        driver.get(url_to_go)
        time.sleep(2)
        #print("Current URL:", current_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        div_element = soup.find('div', class_='image')

        meta_tag = soup.find('meta', property='og:image')

    # Extract the value of the "content" attribute
        image_link = meta_tag['content']


        
        for img_result in [image_link]:
            print(img_result)
            file_name = search_term
            get_image(img_result,file_name,index)
    except:
        pass


df = pd.concat([df,pd.DataFrame(locations)],axis=1)

driver.quit()