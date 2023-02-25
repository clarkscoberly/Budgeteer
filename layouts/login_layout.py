import dash_bootstrap_components as dbc
from dash import html, dcc

def create_login_layout():
    return dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Welcome to Budgeteer", className="text-center mt-5"),
            html.Hr(),
            html.P("Please Log In To Continue", className="text-center mt-5"),
            dbc.Input(id='username', type='text', placeholder='Username', className='mt-4'),
            dbc.Input(id='password', type='password', placeholder='Password', className='mt-4'),
            html.Div(id='error-msg', className='mt-2 text-danger')
        ], width=6, style={"margin" : "auto"})
    ]),
    dbc.Row([
        dbc.Col([
            html.Button('Log In', id='login-button', n_clicks=0, className='btn btn-primary mt-4', style={"width" : "100%", "margin" : "auto"})
        ], width=2, style={"margin" : "auto"})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Link(html.Button('Create Account', className='btn btn-primary mt-4', style={"width" : "100%", "margin" : "auto"}), href='/create_account')
        ], width=2, style={"margin" : "auto"})
    ])
], fluid=True)