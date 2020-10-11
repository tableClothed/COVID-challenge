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


class Line_Plot():
	def __init__(self, app, data):
		self.data = data
		country_list = self.data.Country.unique()
		regs = []
		for country in country_list:
			regs.append({"label":country, "value":country})

		self.graph = html.Div([dcc.Graph(id="graph-line")],
			style={
				"width":'85vw',
				'display':'inline-block'
			})

		app.callback(
			Output("graph-line", "figure"),
			[Input("regions-line", "value"),
			Input("chosen_y", "value"),
			Input("radio-line", "value"),
			Input("date-line", "value")])(self.update_countries_plot)


		self.navbar = html.Div([

			##### DATA RELATIONS #####
			html.Label("Data Y"),
			dcc.Dropdown(
				id="chosen_y",
				options = [ {"label":i, "value":i} for i in list(self.data.columns)]),


			##### GRAPH TYPE #####
			html.Label("Radio Items"),
			dcc.RadioItems(
				id="radio-line",
				options=[
					{'label':"log","value":"log"},
					{'label':"linear","value":"linear"}
				],
				labelStyle ={'display': 'inline-block'},
				value="log"),


			##### COUNTRIES #####
			html.Label("Regions"),
			dcc.Dropdown(
				id="regions-line",
				options = regs,
				value=["Germany", "Poland"],
				multi=True),


			##### DATE #####
			html.Label("Date"),
			dcc.Slider(
				id="date-line",
				min=0,
				max=10),
				]

			# style={
			# 	"width":'15vw',
			# 	'display': 'inline-block',
			# 	'padding': 20,
			# 	'background':'#f5f5ed',
			# 	'height':'100vh'}
			)



	def update_countries_plot(self, regions, chosen_y, radio, date):
		df = self.data
		# ddf = df[df["TotalCases"] >= date]

		countries_to_show = df.Country.values

		countries_to_df = []
		for country in countries_to_show:
			val = country if country in regions else "other"
			countries_to_df.append(val)

		df["color_scatter"] = countries_to_df

		fig = px.line(df, x="Date", y="Deaths", color="color_scatter")

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


# df = data.df
# plot = px.line(df, x="Date", y="Deaths", color="Country", height=900)
# plot.update_layout(legend=dict(
# 	orientation="h",
# 	yanchor="top",
# 	xanchor="center",
# 	y=-0.3,
# 	x=0.5))


# app.layout = html.Div([

# 	##### GRAPH #####

# 	html.Div([
# 		dcc.Graph(id="graph")],
# 		style={
# 			"width":'85vw',
# 			'display':'inline-block'
# 			})
# 	],
# 	style={
# 		"display":"flex",
# 		"width":"100vw",
# 		'margin':0,
# 		'height':'100vh',
# 		'overflow':'hidden'}
# )



# @app.callback(
# 	Output("graph", "figure"),
# 	[Input("regions", "value"),
# 	Input("radio", "value"),
# 	Input("date", "value")])
# def update_countries_plot(regions, radio, date):
# 	df = data.df
# 	# ddf = df[df["TotalCases"] >= date]

# 	countries_to_show = df.Country.values

# 	countries_to_df = []
# 	for country in countries_to_show:
# 		val = country if country in regions else "other"
# 		countries_to_df.append(val)

# 	df["color_scatter"] = countries_to_df

# 	fig = px.scatter(df,x="Date", y="Deaths", color="color_scatter",
# 		hover_name="Country")

# 	# fig.update_layout(margin={'l': 40, 'b': 10, 't': 10, 'r': 40},
# 	# 	hovermode='closest', showlegend=False)
# 	fig.update_layout(legend=dict(
# 		orientation="h",
# 		yanchor="top",
# 		xanchor="center",
# 		y=-0.3,
# 		x=0.5))

# 	fig.update_xaxes(type=radio)
# 	fig.update_yaxes(type=radio)
# 	return fig
