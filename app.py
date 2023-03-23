"""
Author: Clark Coberly
Title: Budgeteer
Creation Date: 2/18/23
Purpose: To provide a means to encourage people to budget through an easy to use free application
"""

from dash import Dash, dcc, html, Output, Input, State, ctx, dash_table, dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from layouts.login_layout import *
from layouts.account_creation_layout import *

from layouts.home_layout import *
from layouts.analytics_layout import *
from layouts.settings_layout import *
from layouts.envelope_layout import *
from layouts.envelope_creation_layout import *
from layouts.envelope_edit_layout import *
from layouts.add_item_layout import *
from layouts.edit_item_layout import *

from support.db import Database, user

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
db = Database() # database control.

title = dcc.Markdown(children="# **Budgeteer**")

login_layout = create_login_layout()
account_creation_layout = create_account_creation_layout()

#############
# LOGIN/OUT #
#############
@app.callback(
    Output('error-msg', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value')
)
def login_user(login, username, password):

    # Check if the username and password are valid
    if db.login_user(username, password) != None:   
        return dcc.Location(pathname='/home', id='home')
    elif username == None and password == None:
        pass
    else:
        return "Invalid username or password"

# Define the callback for account creation
@app.callback(
    Output('account-creation-msg', 'children'),
    Input('create_account_button', 'n_clicks'),
    State('new-username', 'value'),
    State('new-password', 'value'),
    State('confirm-password', 'value')
)
def create_account(n_clicks, new_username, new_password, confirm_password):
# Check if the passwords match
    if new_password == None and new_username == None:
        PreventUpdate

    elif new_password != confirm_password:
        return "Passwords Do Not Match"

    elif new_username == None:
        return "Username Cannot Be Empty"
    
    elif new_username != None and new_password != None and confirm_password != None and new_password == confirm_password:
        
        if db.create_user(new_username, new_password) != None:
            return dcc.Location(pathname="/home", id="home")
        else:
            return "Username Already Exists"

@app.callback(
    Output("settings_placeholder", "children"),
    Input("logout_button", "n_clicks"),
)
def logout_user(n_clicks):
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == "logout_button":
        db.user.log_out()

    return ""
    



######################
# ENVELOPE CALLBACKS #
######################
# Change the following so that you don't "return" anything and this is changed into two callbacks
# This way you can have it be on both.

@app.callback(
    Output('home_envelope_data_table', "data"),
    Output('home_envelope_data_table', "columns"),
    Input('url', 'pathname'),
)
def populate_envelope_with_data(url):
    url = url.split('/')[-1]
    if url != "home":
        PreventUpdate

    else:
        db.reload_db()
        data = user.envelopes_df[["name", "budget"]].to_dict("records")
        columns = [{"name": "Envelope Name", "id": "name"},
                    {"name": "Budget", "id": "budget"}]
        return data, columns


@app.callback(
    Output('home_selected_envelope_placeholder', 'children'),
    Input('home_envelope_data_table', 'active_cell'),
    State('home_envelope_data_table', 'data'),
)
def enter_selected_envelope_callback(home_cell, home_data):
    if not ctx.triggered:
        raise PreventUpdate
    
    table_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if table_id == "home_envelope_data_table":
        path, data = enter_selected_envelope(home_cell, home_data)
        db.user.current_envelope = data

        return dcc.Location(id="home_selected_envelope_location", pathname=path)

    raise PreventUpdate


@app.callback(
    Output('envelope_item_selection_placeholder', 'children'),
    Input('envelope_items_data_table', 'active_cell'),
    State('envelope_items_data_table', 'data'),
)
def enter_selected_item_callback(item_cell, item_data):
    if not ctx.triggered:
        raise PreventUpdate

    table_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if table_id == "envelope_items_data_table":

        path, data = enter_selected_item(item_cell, item_data)
        db.user.current_item = data
        return dcc.Location(id="envelope_item_selection_location", pathname=path)

    raise PreventUpdate


@app.callback(
    Output("envelope_creation_placeholder", "children"),
    Input("save_envelope_button", "n_clicks"),
    Input("envelope_creation_name", "value"),
    Input("envelope_creation_budget_amount", "value"),
    Input("envelope_creation_options", "value"),
    Input("envelope_creation_text_area", "value"),
)
def create_envelope(n_clicks, name, budget, frequency, note):
    if not ctx.triggered:
        PreventUpdate
    else:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == "save_envelope_button":
            db.create_envelope(name, budget, frequency, note)
            user.envelopes_df = db.get_envelopes_for_user()
            
            return ""

@app.callback(
    Output("envelope_edit_placeholder", "value"),
    Input("edit_envelope_button", "n_clicks"),
    Input("delete_envelope_button", "n_clicks"),
    Input("edit_envelope_name", "value"),
    Input("edit_envelope_budget_amount", "value"),
    Input("edit_envelope_options_dropdown", "value"),
    Input("edit_envelope_text_area", "value"),
)
def edit_envelope(edit, delete, name, budget, option, note):
    # Currently Updates just the budget and does not do it in "real-time" requiring a reload to realize the changes.
    if not ctx.triggered:
        PreventUpdate
    else:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        name = db.user.current_envelope["name"]
        if triggered_id == "edit_envelope_button":

            db.update_envelope_budget(name, budget)

            
            return ""
        elif triggered_id == "delete_envelope_button":
            db.delete_envelope(name)
            db.reload_db()

            return ""



###################
# ITEMS CALLBACKS #
###################

@app.callback(
    Output('envelope_items_data_table', "data"),
    Output('envelope_items_data_table', "columns"),
    Input('url', 'pathname'),
)
def populate_envelope_with_data(url):
    url = url.split('/')[-1]
    if url != "envelope":
        PreventUpdate

    else:
        envelope_items_df = db.user.envelopes_df[db.user.envelopes_df["name"] == db.user.current_envelope["name"]]    
        items_list = envelope_items_df["items"].iloc[0]
        items_df = pd.DataFrame(items_list)
        items_df["date"] = items_df["date"].dt.strftime("%m/%d/%Y")

        data = items_df[["name", "cost", "note", "date"]].to_dict("records")
        columns=[
        {"name": "Name", "id": "name"},
        {"name": "Cost", "id": "cost"},
        {"name": "Note", "id": "note"},
        {"name": "Date", "id": "date"}
        ]
        return data, columns


@app.callback(
    Output("item_add_placeholder", "value"),
    Input("envelope_item_name", "value"),
    Input("envelope_item_cost", "value"),
    Input("item_text_area", "value"),
    Input("save_item_button", "n_clicks"),

)
def create_item_callback(name, cost, note, n_click):
    id = ctx.triggered_id
    if id == "save_item_button":
        envelope_name = db.user.current_envelope["name"]
        db.add_item_to_envelope(envelope_name, name, cost, note)
        db.reload_db()
    else:
        PreventUpdate

    return ""








####################
# DISPLAY CALLBACK #
####################
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    if pathname == '/':
        return login_layout
    elif pathname == '/create_account':
        return account_creation_layout
    elif pathname == '/home':
        return create_home_layout()
    elif pathname == '/analytics':
        return create_analytics_layout()
    elif pathname == '/settings':
        return create_settings_layout()
    elif pathname == '/envelope':
        return create_envelope_layout(db.user.current_envelope["name"], db.user.current_envelope["budget"])
    elif pathname == '/create_envelope':
        return create_envelope_creation_layout()
    elif pathname == '/edit_envelope':
        return create_envelope_edit_layout()
    elif pathname == '/edit_item':
        return create_edit_item_layout()
    elif pathname == '/add_item':
        return create_add_item_layout()
    else:
        return '404 Page not found'


app.layout = html.Div([
dcc.Location(id='url', refresh=False),
html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=True)