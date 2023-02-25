import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table


# Load some sample data
df = px.data.iris()

# Create a scatter plot using the sample data
placeholder = px.scatter(df, x='sepal_width', y='sepal_length')

envelope_history_data_table = dash_table.DataTable(
    id='table',
    columns=[{'name': i, 'id': i} for i in df.columns],
    data=df.to_dict('records'),
    style_data={'border': '1px solid black'},
    style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
    style_cell={'textAlign': 'center'}
)


def create_envelope_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Envelope - Edit to Change Based on Envelope")], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Button('Home', className='btn btn-primary mt-2', style={"width" : "100%"}, href="/home")),
                    dbc.Col(dbc.Button('Edit Envelope', id='edit_envelope_button', className='btn btn-primary mt-2', style={"width" : "100%"}, href="/edit_envelope")),
                    dbc.Col(dbc.Button('Add Item', id='add_item_button', className='btn btn-primary mt-2', style={"width" : "100%"}, href="/add_item"))
                ]),
                dbc.Row(envelope_history_data_table)
            ], width=6),
            dbc.Col([
                dcc.Graph(id='graph1', figure=placeholder),
                dcc.Graph(id='graph2', figure=placeholder)
            ], width=6),
        ])
    ], fluid=True)



