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


class Table_Data():
	def __init__(self, app, data):
		self.data = data

		self.navbar = html.Div([])

		self.graph = dash_table.DataTable(
			id="table",
			columns=[{"name":i, "id":i} for i in self.data.columns],
			data=self.data.to_dict('records'),
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
		