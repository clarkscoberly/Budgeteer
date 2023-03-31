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

from questioneer.automatic_budget import *

from support.db import Database, user

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
db = Database() # database control.

title = dcc.Markdown(children="# **Budgeteer**")

login_layout = create_login_layout()
account_creation_layout = create_account_creation_layout()

##################
# USER CALLBACKS #
##################
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
            return dcc.Location(pathname="/questioneer_decision", id="create_account")
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

@app.callback(
    Output("settings_placeholder", "value"),
    Input("delete_user_button", "n_clicks"),
)
def delete_user_profile_callback(n_clicks):
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id)
    if triggered_id == "delete_user_button":
        db.delete_user_profile()
        return ""
    else:
        PreventUpdate




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
        columns = [
            {"name": "Envelope Name", "id": "name"},
            {"name": "Budget", "id": "budget"},
            # {"name": "Time Period", "id": "frequency"},
        ]
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
    Output('envelope_budget_card', 'children'),
    Output("envelope_budget_card", "color"),
    Input('url', 'pathname'),
    State("envelope_budget_card", "children"),
)
def populate_envelope_with_data(url, children_of_card):
    url = url.split('/')[-1]
    if url != "envelope":
        PreventUpdate

    else:
        envelope_items_df = db.user.envelopes_df[db.user.envelopes_df["name"] == db.user.current_envelope["name"]]    
        items_list = envelope_items_df["items"].iloc[0]
        items_df = pd.DataFrame(items_list)
        items_df["date"] = items_df["date"].dt.strftime("%m/%d/%Y")

        data = items_df[["name", "cost", "note", "date"]].to_dict("records")
        try:
            spending = sum(int(record["cost"]) for record in data)
            print(spending)
        except Exception as e:
            print("Exception in populate_envelope_with_data: ", e)
            spending = 0

        try:
            initial_budget = children_of_card[1]['props']['children']
            print(initial_budget)
            current_budget = initial_budget - spending
            if current_budget <= 0:
                card_color = "danger"
            elif current_budget > initial_budget / 2:
                card_color = "info"
            else:
                card_color = "warning"
        except Exception as e:
            print(e)
            current_budget = initial_budget
            card_color = "info"

        card_content = [
        html.H4("Budget Remaining", className="card-title"),
        html.P(current_budget, id="envelope_budget_value", className="card-text"),
        ]
        columns=[
            {"name": "Name", "id": "name"},
            {"name": "Cost", "id": "cost"},
            {"name": "Note", "id": "note"},
            {"name": "Date", "id": "date"}
        ]
        return data, columns, card_content, card_color


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

@app.callback(
    Output("edit_item_placeholder", "value"),
    Input("edit_envelope_item_name", "value"),
    Input("edit_envelope_item_cost", "value"),
    Input("edit_item_text_area", "value"),
    Input("edit_item_button", "n_clicks"),

)
def update_item_callback(new_name, new_cost, new_note, n_click):
    id = ctx.triggered_id
    print(id)
    if id == "edit_item_button":
        envelope_name = db.user.current_envelope["name"]
        # print(envelope_name)
        # i = db.user.envelopes_df[db.user.envelopes_df["name"] == envelope_name]
        # # print(i["items"].head())
        # # print(i[i["id"]])
        # # db.update_item_cost(envelope_name, item_name, new_cost)
        # # db.reload_db()
        # def get_id(my_dict):
        #     return my_dict['id']

        # # apply function to dataframe
        # df['id'] = i['my_dict'].apply(get_id)

        # # display resulting dataframe
        # print(df)
    else:
        PreventUpdate

    return ""

############################
# BUDGET CREATION CALLBACK #
############################
@app.callback(
    Output('age_inputs_container', 'children'),
    Input('family_size', 'value')
)
def generate_age_inputs(family_size):
    if not family_size:
        return []

    age_inputs = []
    for i in range(family_size):
        age_inputs.append(
            dcc.Input(
                id=f'age_input_{i}',
                type='number',
                placeholder=f'Enter age for family member {i+1}',
                className='form-control mb-3'
            )
        )
    return age_inputs

@app.callback(
    Output('url', 'pathname'),
    Input('confirm_button', 'n_clicks'),
    State('family_size', 'value'),
    State('age_inputs_container', 'children'),
    State('savings_level', 'value')
)
def automatic_budget_creation_callback(n_clicks, family_size, age_inputs, savings_level):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    # Extract age inputs
    ages = [int(input_element['props']['value']) for input_element in age_inputs]

    # Call function to create budget
    automatic_budget_creation(family_size, ages, savings_level)



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
    elif pathname == '/questioneer_decision':
        return create_questioneer_decision()
    elif pathname == '/questioneer_layout':
        return create_questioneer_layout()
    else:
        return '404 Page not found'


app.layout = html.Div([
dcc.Location(id='url', refresh=False),
html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=False)