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
                dbc.Row(html.Nav([
                    html.A('Home', href='/home', className='nav-link'),
                    html.A('Analytics', href='/analyze', className='nav-link'),
                    html.A('Settings', href='/settings', className='nav-link')
                    ], className='navbar navbar-expand-lg navbar-light bg-light'),),
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                        html.H5('Home Page', className='card-title')
                        ])], className='mb-4')
                ]),
                dbc.Row([
                    html.Button('Create Envelope', id='create-envelope-button', className='btn btn-primary mt-2')
                ])
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




# # Define the app layout
# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Nav([
#         html.A('Home', href='/home', className='nav-link'),
#         html.A('Analytics', href='/analyze', className='nav-link'),
#         html.A('Settings', href='/settings', className='nav-link')
#     ], className='navbar navbar-expand-lg navbar-light bg-light'),
#     html.Div(id='page-content')
# ])