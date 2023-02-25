import dash_bootstrap_components as dbc
from dash import html, dcc

def create_settings_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Settings")], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row(html.Nav([
                    html.A('Home', href='/home', className='nav-link'),
                    html.A('Analytics', href='/analyze', className='nav-link'),
                    html.A('Settings', href='/settings', className='nav-link')
                    ], className='navbar navbar-expand-lg navbar-light bg-light'),),
            ])
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
                dbc.Button('Log Out', id="logout_button", className='btn btn-primary mt-4', href="/")
            ], width=6, style={'margin': 'auto'})
        ])
    ], fluid=True)