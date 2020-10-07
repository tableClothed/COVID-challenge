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
import datetime

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css", "styles/style.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


####### SCRAPED DATA ########
class Data:
	def __init__(self):
		self.df_today, self.df_yesterday, self.df_two_days_ago = self.get_updated_info()
		self.df = self.scrap_time_series()

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




data = Data()
country_list = data.df.Country.unique()

regs = []
for country in country_list:
	regs.append({"label":country, "value":country})


# df = data.df
# plot = px.line(df, x="Date", y="Deaths", color="Country", height=900)
# plot.update_layout(legend=dict(
# 	orientation="h",
# 	yanchor="top",
# 	xanchor="center",
# 	y=-0.3,
# 	x=0.5))


app.layout = html.Div([

	html.Div([

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


		##### COUNTRIES #####
		html.Label("Regions"),
		dcc.Dropdown(
			id="regions",
			options = regs,
			value=["Germany", "Poland"],
			multi=True),


		##### DATE #####
		html.Label("Date"),
		dcc.Slider(
			id="date",
			min=0,
			max=10),
			],

		style={
			"width":'15vw',
			'display': 'inline-block',
			'padding': 20,
			'background':'#f5f5ed',
			'height':'100vh'}
		),

	##### GRAPH #####

	html.Div([
		dcc.Graph(id="graph")],
		style={
			"width":'85vw',
			'display':'inline-block'
			})
	],
	style={
		"display":"flex",
		"width":"100vw",
		'margin':0,
		'height':'100vh',
		'overflow':'hidden'}
)



@app.callback(
	Output("graph", "figure"),
	[Input("regions", "value"),
	Input("radio", "value"),
	Input("date", "value")])
def update_countries_plot(regions, radio, date):
	df = data.df
	# ddf = df[df["TotalCases"] >= date]

	countries_to_show = df.Country.values

	countries_to_df = []
	for country in countries_to_show:
		val = country if country in regions else "other"
		countries_to_df.append(val)

	df["color_scatter"] = countries_to_df

	fig = px.scatter(df,x="Date", y="Deaths", color="color_scatter",
		hover_name="Country")

	# fig.update_layout(margin={'l': 40, 'b': 10, 't': 10, 'r': 40},
	# 	hovermode='closest', showlegend=False)
	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="top",
		xanchor="center",
		y=-0.3,
		x=0.5))

	fig.update_xaxes(type=radio)
	fig.update_yaxes(type=radio)
	return fig





if __name__ == '__main__':
	app.run_server(debug=True)