import dash_bootstrap_components as dbc
from dash import html, dcc
from layouts.navbar_layout import *

def create_settings_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col(create_navbar("Settings")),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Themes'),
                    dcc.Dropdown(
                        id='themes-dropdown',
                        options=[
                            {'label': 'Dark', 'value': 'dark'},
                            {'label': 'Light', 'value': 'light'}
                        ],
                        value='dark'
                    )
                ], className='mt-4'),
                html.Div([
                    dcc.RadioItems(
                        id='auto-fill-radio',
                        options=[
                            {'label': 'On', 'value': 'on'},
                            {'label': 'Off', 'value': 'off'}
                        ],
                        value='on',
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                    )
                ], className='mt-4'),
                dbc.Button('Log Out', id="logout_button", className='btn btn-primary mt-4', href="/"),
                dbc.Button('Delete Profile', id="delete_user_button", className='btn btn-primary mt-4', href="/", color="warning")
            ], width=6, style={'margin': 'auto'})
        ]),
        html.H1(id="settings_placeholder")
    ], fluid=True)