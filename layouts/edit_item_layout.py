import dash_bootstrap_components as dbc
from dash import html, dcc

def create_edit_item_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Edit Item", className="text-center mt-5", style={"padding-bottom" : "30px"})], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row(dbc.Input(id="envelope_item_name", placeholder="Payee (Who Recieved Payment?)", type="text"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dbc.Input(id="envelope_item_cost", placeholder="Amount", type="number"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dbc.Textarea(placeholder="Enter a description of the expense if you'd like...", id='item_text_area', style={"width" : "60%", "margin" : "auto", "padding-bottom" : "20px"})),
                dbc.Row(dbc.Button('Save', id='save_item_button', className='btn btn-primary mt-2', style={"width" : "25%", "margin" : "auto"}, href="/envelope"))
            ], width=12),
        ])
    ], fluid=True)