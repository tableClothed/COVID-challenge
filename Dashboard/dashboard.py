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
from data import Data
from scatter import Scatter_Plot
from plot import Line_Plot
from table import Table_Data



class Dashboard():
	def __init__(self):
		self.data = Data()
		self.graph_type = "line_plot"

		self.navbar = html.Div(["This is supposed to be a navbar."])
		self.main_graph = html.Div(["This is supposed to be a dashboard"])

		self.app = dash.Dash(__name__,
			suppress_callback_exceptions=True,
			external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css", "assets/style.css"])


		self.line_plot = Line_Plot(self.app, self.data.df)
		self.scatter_plot = Scatter_Plot(self.app, self.data.df_today)
		self.table_data = Table_Data(self.app, self.data.df)

		self.main_plot = self.line_plot

		self.handle_layout()
		
		self.app.callback([Output('graph-layout', 'children'),
						  Output('navbar', 'children')],
		            	  Input('plot_type', 'value'))(self.change_to_graph)



	####### HANDLE PLOT TYPES ########
	def change_to_graph(self, plot_type):
		if plot_type == "line_plot" or plot_type == "Line Plot":
			self.main_plot = self.line_plot
		elif plot_type == "scatter_plot" or plot_type == "Scatter Plot":
			self.main_plot = self.scatter_plot
		else:
			self.main_plot = self.table_data

		return self.main_plot.graph, self.main_plot.navbar 
		# self.handle_layout()


	####### LAYOUT APPEARANCE #######
	def handle_layout(self):
		self.app.layout = html.Div([

			html.Div([
				html.Div([
					##### navbar #####
					html.Label("Plot Type"),
						dcc.Dropdown(
							id="plot_type",
							options = [
								{"label":"Line Plot", "value":"line_plot"},
								{"label":"Scatter Plot", "value":"scatter_plot"},
								{"label":"Data Table", "value":"data_table"}
							],
							value="Line Plot")
					]),

				html.Div(id="navbar")
				],
				
				style={
					"width":'15vw',
					'display': 'inline-block',
					'padding': 20,
					'background':'#f5f5ed',
					'height':'100vh'}
				),


			##### graph #####
			html.Div(
				style={
					"width":'85vw',
					'display':'inline-block'
				},
				id="graph-layout")


			],
			style={
				"display":"flex",
				"width":"100vw",
				'margin':0,
				'height':'100vh',
				'overflow':'hidden'}
		)


if __name__ == '__main__':
	dashboard = Dashboard()
	dashboard.app.run_server(debug=True)