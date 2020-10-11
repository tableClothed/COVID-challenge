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


class Scatter_Plot():
	def __init__(self, app, data):
		app.callback(
			Output("regions-scatter","options"),
			Input("thresh", "value"))(self.update_countries_dropdown)

		app.callback(
			Output("graph-scatter", "figure"),
			[Input("x_data", "value"),
			Input("y_data", "value"),
			Input("regions-scatter", "value"),
			Input("radio", "value"),
			Input("thresh", "value")])(self.update_scatter)

		self.data = data

		options = [{'label':col, "value":col}
			for col in list(self.data.columns)
			if type(self.data.iloc[22][col]) != str]

		self.graph = html.Div([ dcc.Graph(id="graph-scatter")],
			style={"width":'77%',
			'display': 'inline-block',
			'margin':20})


		self.navbar = html.Div([

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
				labelStyle ={'display': 'inline-block'},
				value="log"),


			##### COUNTRIES #####
			html.Label("Regions:"),
			dcc.Dropdown(
				id="regions-scatter",
				value=["World"],
				multi=True),


			##### DATE #####
			html.Label("Min cases threshold:"),
			dcc.Input(
				id="thresh",
				type="number",
				value=100),
			
			]

			# style={"width":'22%','display': 'inline-block', 'margin': 20}
			)


	def update_countries_dropdown(self, thresh):
		df = self.data

		ddf = df[df["TotalCases"] >= thresh]
		countries = ddf["Country,Other"].values

		return [{'label': country, 'value': country} for country in countries if type(country) == str]


	def update_scatter(self, x, y, regions, radio_type, thresh_val):
		df = self.data

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



########### CALLBACKS ############

# @app.callback(
# 	Output("regions","options"),
# 	 Input("thresh", "value"))
# def update_countries_dropdown(thresh):
# 	df = data.df_today

# 	ddf = df[df["TotalCases"] >= thresh]
# 	countries = ddf["Country,Other"].values

# 	return [{'label': country, 'value': country} for country in countries if len(country) > 0]


# @app.callback(
# 	Output("graph", "figure"),
# 	[Input("x_data", "value"),
# 	Input("y_data", "value"),
# 	Input("regions", "value"),
# 	Input("radio", "value"),
# 	Input("thresh", "value")])
# def update_scatter(x, y, regions, radio_type, thresh_val):
# 	df = data.df_today

# 	ddf = df[df["TotalCases"] >= thresh_val]
# 	countries_to_show = ddf["Country,Other"].values

# 	countries_to_df = []
# 	for country in countries_to_show:
# 		val = "chosen" if country in regions else "other"
# 		countries_to_df.append(val)

# 	ddf["color_scatter"] = countries_to_df

# 	fig = px.scatter(ddf, x=x, y=y,	color="color_scatter",
# 		hover_name="Country,Other")

# 	fig.update_layout(margin={'l': 40, 'b': 10, 't': 10, 'r': 40},
# 		hovermode='closest', showlegend=False)

# 	fig.update_xaxes(title=x, type=radio_type)
# 	fig.update_yaxes(title=y, type=radio_type)


# 	return fig
	