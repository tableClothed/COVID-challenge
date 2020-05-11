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

# headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

PATH = "C:\Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH, chrome_options=options)

URL = "https://www.worldometers.info/coronavirus/"

driver.get(URL)
driver.implicitly_wait(5)

countries_table = driver.find_element_by_id("main_table_countries_today")
titles = countries_table.find_element_by_tag_name("tr").text
titles = [i.lower().replace(" ", "_").replace(",", "").replace("/", "") for i in titles.split("\n")]


# for i in range(len(titles):
#     if (titles[i])[-1] == "\\":
#         titles[i].join()

# # titles = [i.join()]

# countries_data = countries_table.find_elements_by_tag_name("tr")

# json

# print("\n\n\n\n\n")
# for c_data in countries_data:
#     text = c_data.text
#     if len(text) < 20: break




print("\n\n\n\n\n")

driver.quit()
print("\n\n\n\n\n")

print(titles)
