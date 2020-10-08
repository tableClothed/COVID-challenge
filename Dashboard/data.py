import pandas as pd
import re
import os
import pandas as pd
import requests
import datetime


####### SCRAPED DATA ########
class Data:
	def __init__(self):
		self.df_today, self.df_yesterday, self.df_two_days_ago = self.get_updated_info()
		self.df = self.scrap_time_series()


	######## GET UPDATED INFORMATIONS FROM TODAY, YESTEDAY AND 2 DAYS AGO #########
	def get_updated_info(self):
		url = requests.get("https://www.worldometers.info/coronavirus/").text
		html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), url)

		df = pd.read_html(html_source)
		for d in df:
			d = d[d["Country,Other"] != "Total:"]

		return df

	####### GET LIST OF CONTINENTS ##########
	def get_list_of_continents(self):
		continents = set([d for d in self.df_today["Continent"] if type(d) == str])
		return list(continents)

	####### GET LIST OF COUNTRIES ###########
	def get_list_of_countries(self):
		countries = (set([d for d in self.df_today["Country,Other"]
			if type(d) == str and d not in self.df_today["Continent"]
			and d.lower() is not "total:"]))
		return list(countries) 
	

	######## RETURN ROW VALUE FOR COLUMN, ID ###########
	def get_data_for(self, column, value_in_row, returned_column):
		val = df.loc[df[column] == value_in_row,  returned_column]
		return val


	######### GET INFORMATIONS AS TIME SERIES ###########
	def scrap_time_series(self):
		url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
		
		today = datetime.date.today()
		date_today = today.strftime("%d-%m-%y")


		filename = f"csv/data_net_{date_today}.csv"
		if os.path.isfile(filename):
			df = pd.read_csv(filename)
		else:
			df = pd.read_csv(url)
			df.to_csv(filename)

		return df