import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc


# Load some sample data
df = px.data.iris()

# Create a scatter plot using the sample data
placeholder = px.scatter(df, x='sepal_width', y='sepal_length')


def create_home_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Home")], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='graph1', figure=placeholder)
            ], width=3),
            dbc.Col([
                dcc.Graph(id='graph2', figure=placeholder)
            ], width=5),
            dbc.Col([
                dcc.Graph(id='graph3', figure=placeholder)
            ], width=4),
        ]),
        dbc.Row([
            dbc.Col([
                html.A("Log Out", href="/", className="mt-4 text-muted")
            ], width=2)
        ])
    ], fluid=True)