import dash_bootstrap_components as dbc
from dash import html, dcc

def create_account_creation_layout():
    return dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Create A New Account", className="text-center mt-5"),
            html.Hr(),
            dbc.Input(id='new-username', type='text', placeholder='Username', className='mt-4'),
            dbc.Input(id='new-password', type='password', placeholder='Password', className='mt-4'),
            dbc.Input(id='confirm-password', type='password', placeholder='Confirm Password', className='mt-4'),
            html.Div(id='account-creation-msg', className='mt-2 text-danger')
        ], width=6, style={"margin" : "auto"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Button('Create Account', id='create_account_button', n_clicks=0, className='btn btn-primary mt-4', style={"width" : "100%"}),
        ], width=2, style={"margin" : "auto"})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Back to Login", href="/", className="btn btn-primary mt-4", style={"width" : "100%"})
        ], width=2, style={"margin" : "auto"})
    ])
], fluid=True)