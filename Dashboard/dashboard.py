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
app.config.supress_callback_exceptions = True


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
country_list = data.get_list_of_countries()

regs = []
for country in country_list:
	regs.append({"label":country, "value":country})

df = pd.DataFrame({
	"Country":list(data.df_today["Country,Other"]),
	"Amount":list(data.df_today.TotalCases)
	})

fig1 = px.line(df, x="Country", y="Amount")
fig2 = px.scatter(df, x="Country", y="Amount")
fig3 = dash_table.DataTable(
			id="table",
			columns=[{"name":i, "id":i} for i in df.columns],
			data=df.to_dict('records'))


# @app.callback(
# 	Output('dropdown1', 'children'),
# 	Input('', 'value'))
# def update_dropdown1(dropdown_value):
# 	return 


app.layout = html.Div([

	html.Div([

		##### DATA SRC #####
		html.Label("Data Source"),
		dcc.Dropdown(
			id="dropdown1",
			options = [
				{'label':"Confirmed Cases", "value":"Confirmed Cases"},
				{'label':"Confirmed Cases", "value":"Confirmed Cases"},
				{'label':"Confirmed Cases", "value":"Confirmed Cases"}]),


		##### INCREASE #####
		html.Label("Data Source"),
		dcc.Dropdown(
			id="dropdown2",
			options = [
				{'label':"Trajectory", "value":"Trajectory"},
				{'label':"Daily Increase", "value":"Daily Increase"},
				{'label':"Cumulative", "value":"Cumulative"},
				{'label':"Development 10", "value":"Development 10"},
				{'label':"Development 100", "value":"Development 100"}]),


		##### GRAPH TYPE #####
		html.Label("Radio Items"),
		dcc.RadioItems(
			id="radio",
			options=[
				{'label':"log","value":"log"},
				{'label':"linear","value":"linear"}
			],
			value="log"),


		##### CUNTRIES #####
		html.Label("Regions"),
		dcc.Dropdown(
			id="regions",
			options = regs,
			value=["World"],
			multi=True),


		##### DATE #####
		html.Label("Date"),
		dcc.Slider(
			id="date",
			min=0,
			max=10),
			],

		style={"width":'22%','display': 'inline-block', 'margin': 20}),

	##### GRAPH #####
	fig3,

	html.Div([
		dcc.Graph(id="example_graph", figure=fig2)],
		style={"width":'77%', 'display': 'inline-block', 'margin':20})
	],
	style={"display":"flex", "width":"100%"})


if __name__ == '__main__':
	app.run_server(debug=True)