from bs4 import BeautifulSoup as soup
import numpy as np
import requests
import json
import re
from datetime import datetime

json_data = {}


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
URL = "https://www.worldometers.info/coronavirus/"

page_html = requests.get(URL, headers=headers)
page_html = soup(page_html.content, 'lxml')

country_table = page_html.find("table", {"id":"main_table_countries_today"})
# print(country_table)

titles = [th.text for th in country_table.thead.tr.findAll("th")]


# wszystkie nagłówki do lowercase, wstawianie spacji przed dużymi literami
# zamiana spacji i przecinków na _
titles = [re.sub(r"(\w)([A-Z])", r"\1 \2", i).lower().replace("\xa0", " ").replace(" ", "_").replace(",", "_").replace("\n", "")
                 for i in titles[1:]]


print(country_table.findAll("tr"))

# for country in country_table.tbody.findAll("tr"):
#     region = country.find("td").text.replace("\n", "")
#     info_array = dict()
#     for i, info in enumerate(country.findAll("td")[1:]):
#         text = info.text.replace("\n", "").replace("+", "")

#         text = text.replace(" ", "").replace(",", "").replace(".", "")
#         if text == "":
#             text = "0"
#         # print(region, text)
#         info_array[titles[i]] = text

#     json_data[text] = info_array
    
# with open(f"infos-{datetime.today().strftime('%Y-%m-%d')}.json", "w") as f:
#     json.dump(json_data, f, indent=4, sort_keys=True)