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


####### SCRAPED DATA ########
class Data:
	def __init__(self):
		self.df_today, self.df_yesterday, self.df_two_days_ago = self.get_updated_info()
		self.column_names = list(self.df_today.columns)[1:]

	
	def clean_df(self, df):
		cols_to_replace = ["NewCases", "NewDeaths", "NewRecovered"]

		for index, row in df.iterrows():
			for col in cols_to_replace:
				try:
					# df[col] = df[col].str.replace("+", "", regex=False)
					# df[col] = df[col].str.replace(",", "", regex=False).astype(float)
					df.loc[index, col] = df.loc[index, col].str.replace("+", "", regex=False)
					df.loc[index, col] = df.loc[index, col].str.replace(",", "", regex=False).astype(float)

				except:
					next

		return df


	def get_updated_info(self):
		url = requests.get("https://www.worldometers.info/coronavirus/").text
		html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), url)

		df = pd.read_html(html_source)
		for d in df:
			d = d[d["Country,Other"] != "Total:"]
			d = self.clean_df(d)

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


options = [{'label':d, "value":d}
			for d in list(data.column_names)]


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
			options = regs,
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
	Output("graph", "figure"),
	[Input("x_data", "value"),
	Input("y_data", "value"),
	Input("radio", "value"),
	Input("thresh", "value")])
def update_scatter(x, y, radio_type, thresh_val):
	df = data.df_today

	string_cols = [col for col in df.columns if type(df.iloc[22][col]) == str]
	print([df.iloc[22][col] for col in df.columns if type(df.iloc[22][col]) == str])

	df = df.drop(string_cols, axis=1)
	ddf = df[df[x] >= thresh_val & df[y] >= thresh_val]

	fig = px.scatter(ddf, x=x, y=y)

	fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

	fig.update_xaxes(title=x, type=radio_type)
	fig.update_yaxes(title=y, type=radio_type)

	return fig
	


if __name__ == '__main__':
	app.run_server(debug=True)