import dash_bootstrap_components as dbc
from dash import html, dcc

def create_envelope_creation_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Envelope Creation", className="text-center mt-5", style={"padding-bottom" : "30px"})], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row(dbc.Input(id="envelope_creation_name", placeholder="Enter Envelope Name...", type="text"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dbc.Input(id="envelope_creation_budget_amount", placeholder="Enter Budget Amount...", type="number"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dcc.Dropdown(id="envelope_creation_options", options={"daily" : "Daily", "weekly" : "Weekly", "monthly" : "Monthly", "yearly" : "Yearly"}, style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"})),
                dbc.Row(dbc.Textarea(placeholder="Enter a description of what your envelope is for if you'd like...", id='envelope_creation_text_area', style={"width" : "60%", "margin" : "auto", "padding-bottom" : "20px"})),
                dbc.Row(dbc.Button('Save', id='save_envelope_button', className='btn btn-primary mt-2', style={"width" : "25%", "margin" : "auto"}, href="/home")),
                html.H1(id="envelope_creation_placeholder")
            ], width=12),
        ])
    ], fluid=True)