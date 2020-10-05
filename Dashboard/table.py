import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import re
import os
import pandas as pd
import requests
from dash.dependencies  import Input, Output, State
import plotly.graph_objs as go

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app.config.supress_callback_exceptions = True


####### SCRAPED DATA ########
class Data:
	def __init__(self):
		self.df_today, self.df_yesterday, self.df_two_days_ago = self.get_updated_info()
		

	def get_updated_info(self):
		url = requests.get("https://www.worldometers.info/coronavirus/").text
		html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), url)

		df = pd.read_html(html_source)
		for d in df:
			d = d[d["Country,Other"] != "Total:"]

		return df


	def get_list_of_continents(self):
		continents = set([d for d in self.df_today["Continent"] if type(d) == str])
		return list(continents)


	def get_list_of_countries(self):
		countries = (set([d for d in self.df_today["Country,Other"]
			if type(d) == str and d not in self.df_today["Continent"]
			and d.lower() is not "total:"]))
		return list(countries) 
	

	def get_data_for(self, column, value_in_row, returned_column):
		val = df.loc[df[column] == value_in_row,  returned_column]
		return val



data = Data()
df = data.df_today

app.layout = html.Div([

	html.Div([

	##### TABLE #####
	dash_table.DataTable(
			id="table",
			columns=[{"name":i, "id":i} for i in df.columns],
			data=df.to_dict('records'),
			editable=True,
			filter_action="native",
			sort_action="native",
			sort_mode="multi",
			row_deletable=True,
			selected_rows=[],
			page_action="native",
			page_current=0,
			page_size=20
		)
	],

	style={"display":"flex", "width":"100%"})
	])


if __name__ == '__main__':
	app.run_server(debug=True)