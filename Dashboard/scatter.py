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


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


####### SCRAPED DATA ########
class Data:
	def __init__(self):
		self.df_today, self.df_yesterday, self.df_two_days_ago = self.get_updated_info()
		self.column_names = list(self.df_today.columns)[1:]

	
	def clean_df(self, df):
		cols_to_replace = ["NewCases", "NewDeaths", "NewRecovered"]

		for col in cols_to_replace:
			df[col] = df[col].astype(str)
			df[col] = df[col].apply(lambda x : x.replace("+", ""))
			df[col] = df[col].apply(lambda x : x.replace(",", "")).astype(float)
		return df


	def get_updated_info(self):
		today = datetime.date.today()
		date_today = today.strftime("%d-%m-%y")

		if os.listdir("csv")[-1] == f"data_{date_today}.csv":
			# print("-------READ CSV--------")
			dfs = []
			for df_url in os.listdir("csv"):
				df = pd.read_csv(f"csv/{df_url}")
				dfs.append(df)
			return list(reversed(dfs))
		
		# print("-------USE URL--------")
		url = requests.get("https://www.worldometers.info/coronavirus/").text
		html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), url)

		new_dfs = []
		df = pd.read_html(html_source)
		dates = [
			date_today,
			(today - datetime.timedelta(days=1)).strftime("%d-%m-%y"),
			(today - datetime.timedelta(days=2)).strftime("%d-%m-%y")
		]

		for d, date in zip(df, dates):
			d = d[d["Country,Other"] != "Total:"]
			d = self.clean_df(d)
			new_dfs.append(d)
			d.to_csv(f"csv/data_{date}.csv", index=False)

		return new_dfs


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

options = [{'label':col, "value":col}
			for col in list(data.column_names)
			if type(data.df_today.iloc[22][col]) != str]


app.layout = html.Div([

	html.Div([

		##### DATA X #####
		html.Label("x data:"),
		dcc.Dropdown(
			id="x_data",
			value=options[2]["value"],
			options = options),


		##### DATA Y #####
		html.Label("y data:"),
		dcc.Dropdown(
			id="y_data",
			value=options[1]["label"],
			options = options),


		##### GRAPH TYPE #####
		html.Label("Graph scaling:"),
		dcc.RadioItems(
			id="radio",
			options=[
				{'label':"log","value":"log"},
				{'label':"linear","value":"linear"}
			],
			value="log"),


		##### CUNTRIES #####
		html.Label("Regions:"),
		dcc.Dropdown(
			id="regions",
			value=["World"],
			multi=True),


		##### DATE #####
		html.Label("Min cases threshold:"),
		dcc.Input(
			id="thresh",
			type="number",
			value=100),
		
		],

		style={"width":'22%','display': 'inline-block', 'margin': 20}),

	##### GRAPH #####
	html.Div([
		dcc.Graph(id="graph")],


		style={"width":'77%', 'display': 'inline-block', 'margin':20})
	],
	style={"display":"flex", "width":"100%"})


########### CALLBACKS ############

@app.callback(
	Output("regions","options"),
	 Input("thresh", "value"))
def update_countries_dropdown(thresh):
	df = data.df_today

	ddf = df[df["TotalCases"] >= thresh]
	countries = ddf["Country,Other"].values

	return [{'label': country, 'value': country} for country in countries if len(country) > 0]


@app.callback(
	Output("graph", "figure"),
	[Input("x_data", "value"),
	Input("y_data", "value"),
	Input("regions", "value"),
	Input("radio", "value"),
	Input("thresh", "value")])
def update_scatter(x, y, regions, radio_type, thresh_val):
	df = data.df_today

	ddf = df[df["TotalCases"] >= thresh_val]
	countries_to_show = ddf["Country,Other"].values

	countries_to_df = []
	for country in countries_to_show:
		val = "chosen" if country in regions else "other"
		countries_to_df.append(val)

	ddf["color_scatter"] = countries_to_df

	fig = px.scatter(ddf, x=x, y=y,	color="color_scatter",
		hover_name="Country,Other")

	fig.update_layout(margin={'l': 40, 'b': 10, 't': 10, 'r': 40},
		hovermode='closest', showlegend=False)

	fig.update_xaxes(title=x, type=radio_type)
	fig.update_yaxes(title=y, type=radio_type)


	return fig
	


if __name__ == '__main__':
	app.run_server(debug=True)