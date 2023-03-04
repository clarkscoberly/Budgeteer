import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dash_table, dash
from layouts.navbar_layout import *

# Load some sample data
df = px.data.iris()

# Create a scatter plot using the sample data
placeholder = px.scatter(df, x='sepal_width', y='sepal_length')

home_envelope_data_table = dash_table.DataTable(
    id='home_envelope_data_table',
    columns=[{'name': i, 'id': i} for i in df.columns],
    data=df.to_dict('records'),
    style_data={'border': '1px solid black'},
    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
    style_cell={'textAlign': 'center'},
)

def create_home_layout():
    return dbc.Container([
        dbc.Row([
            # dbc.Col([html.H1("Home")], width=12),
            dbc.Col(create_navbar("Home")),
        ]),
        dbc.Row([
            dbc.Col([
                # dbc.Row(create_navbar()),
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                        html.H5('THIS WILL BE HOW MUCH MONEY IS LEFT IN THE BUDGET / TOTAL ALLOWANCE CURRENTLY', className='card-title')
                        ])], className='mb-4')
                ]),
                dbc.Row([
                    dbc.Button('Create Envelope', id='create-envelope-button', className='btn btn-primary mt-2', href="/create_envelope")
                ])
            ], width=3),
            dbc.Col(home_envelope_data_table, width=9),
        ]),
    ], fluid=True)


def enter_selected_envelope(active_cell, data):
    if not active_cell:
        return dash.no_update
    
    row_id = active_cell['row']
    row_data = data[row_id]

    return '/envelope', f'?id={row_data["species_id"]}'