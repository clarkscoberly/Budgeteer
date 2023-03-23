import dash_bootstrap_components as dbc
from dash import html, dcc

def create_envelope_edit_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([html.H1("Edit Envelope", className="text-center mt-5", style={"padding-bottom" : "30px"})], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row(dbc.Input(id="edit_envelope_name", placeholder="Enter Envelope Name...", type="text"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dbc.Input(id="edit_envelope_budget_amount", placeholder="Enter Budget Amount...", type="number"), style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"}),
                dbc.Row(dcc.Dropdown(id="edit_envelope_options_dropdown", options={"daily" : "Daily", "weekly" : "Weekly", "monthly" : "Monthly", "yearly" : "Yearly"}, style={"width" : "50%", "margin" : "auto", "padding-bottom" : "20px"})),
                dbc.Row(dbc.Textarea(id='edit_envelope_text_area', placeholder="Enter a description of what your envelope is for if you'd like...", style={"width" : "60%", "margin" : "auto", "padding-bottom" : "20px"})),
                dbc.Row([
                    dbc.Button('Save', id='edit_envelope_button', className='btn btn-primary mt-2', style={"width" : "25%", "margin" : "auto"}, href="/envelope"),
                    dbc.Button('Delete Envelope', id='delete_envelope_button', className='btn btn-primary mt-2', style={"width" : "25%", "margin" : "auto"}, href="/home"),
                ]),

                dbc.Row(html.H1(id="envelope_edit_placeholder"))
            ], width=12),
        ])
    ], fluid=True)