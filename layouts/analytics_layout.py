import dash_bootstrap_components as dbc
from dash import html, dcc

def create_analytics_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Analyze")], width=12),
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
                dcc.Tabs(
                    id='analyze-tabs',
                    value='weekly-tab',
                    children=[
                        dcc.Tab(label='Weekly', value='weekly-tab'),
                        dcc.Tab(label='Monthly', value='monthly-tab'),
                        dcc.Tab(label='Yearly', value='yearly-tab')
                    ]
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='analyze-graph1', figure={})
            ], width=6),
            dbc.Col([
                dcc.Graph(id='analyze-graph2', figure={})
            ], width=6)
        ], className='mt-4', justify='center')
    ], fluid=True)

