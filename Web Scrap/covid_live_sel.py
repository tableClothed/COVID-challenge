import numpy as np
import selenium
import requests
import json
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pickle


# headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# GET COOKIES
PATH = "C:\Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=options)

URL = "https://www.worldometers.info/coronavirus/"

driver.get(URL)
driver.implicitly_wait(5)
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
# driver.quit()


# ENABLE COOKIES
# driver = webdriver.Chrome(PATH, chrome_options=options)
# driver.get(URL)
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
    # driver.add_cookie(cookie)
# driver.implicitly_wait(5)

countries_table = driver.find_element_by_id("main_table_countries_today")
titles = countries_table.find_element_by_tag_name("tr").text
titles = titles.lower().replace("/\n1m pop", "/1m_pop\n").replace(" ", "_").replace(",", "").replace("ts_t", "ts\nt").replace("al\nte", "al_te").replace("\n_", "\n").split("\n")[:-1]

countries_data_even = countries_table.find_elements_by_class_name("even")
countries_data_odd = countries_table.find_elements_by_class_name("odd")

# json

print("\n\n\n\n\n")
# for i in range(len(countries_data_even)):
for i in range(10):
    
    text1 = countries_data_even[i].text.replace(",", "").replace("+", "").split(" ")
    text2 = countries_data_odd[i].text

    # if len(text) < 40: break
    print(text1)
    print(text2)

driver.quit()

print(len(countries_data_even))
print(len(countries_data_odd))