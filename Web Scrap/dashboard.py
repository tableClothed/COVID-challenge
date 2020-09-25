import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with open("countries.txt", "r") as f:
	country_list = f.read()

regs = []

for country in country_list.split("\n")[:-1]:
	regs.append({"label":country, "value":country})

df = pd.DataFrame({
	"Country":country_list[:5],
	"Amount":range(len(country_list[:5]))
	})

fig = px.bar(df, x="Country", y="Amount", barmode="group")

app.layout = html.Div([

	html.Div([

		html.Label("Data Source"),
		dcc.Dropdown(
			options = [
				{'label':"Confirmed Cases", "value":"Confirmed Cases"},
				{'label':"Confirmed Cases", "value":"Confirmed Cases"},
				{'label':"Confirmed Cases", "value":"Confirmed Cases"}]),

		html.Label("Data Source"),
		dcc.Dropdown(
			options = [
				{'label':"Trajectory", "value":"Trajectory"},
				{'label':"Daily Increase", "value":"Daily Increase"},
				{'label':"Cumulative", "value":"Cumulative"},
				{'label':"Development 10", "value":"Development 10"},
				{'label':"Development 100", "value":"Development 100"}]),


		html.Label("Radio Items"),
		dcc.RadioItems(
			options=[
				{'label':"log","value":"log"},
				{'label':"linear","value":"linear"}
			],
			value="log"),

		##### MULTI #####

		html.Label("Regions"),
		dcc.Dropdown(
			options = regs,
			value=["World"],
			multi=True),

		html.Label("Date"),
		dcc.Slider(
			min=0,
			max=10),
			],

		style={"width":'22%','display': 'inline-block', 'marginTop': 0}),

	html.Div([
		dcc.Graph(id="example_graph", figure=fig)],
		style={"width":'77%', 'display': 'inline-block'})
	],
	style={"display":"flex"})


if __name__ == '__main__':
	app.run_server(debug=True)