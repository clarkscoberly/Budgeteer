"""
Author: Clark Coberly
Title: Budgeteer
Creation Date: 2/18/23
Purpose: To provide a means to encourage people to budget through an easy to use free application
"""

from dash import Dash, dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas

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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


title = dcc.Markdown(children="# **Budgeteer**")



login_layout = create_login_layout()
account_creation_layout = create_account_creation_layout()
home_layout = create_home_layout()
analyze_layout = create_analytics_layout()
settings_layout = create_settings_layout()
envelope_layout = create_envelope_layout()
envelope_creation_layout = create_envelope_creation_layout()
envelope_edit_layout = create_envelope_edit_layout()
add_item_layout = create_add_item_layout()
edit_item_layout = create_edit_item_layout()


@app.callback(
    Output('error-msg', 'children'),
    Input('login-button', 'n_clicks'),
    State('username', 'value'),
    State('password', 'value')
)
def validate_login(login, username, password):
    # Check if the username and password are valid
    if username == '1' and password == '1':
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
        return dcc.Location(pathname="/home", id="home")


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
        return home_layout
    elif pathname == '/analyze':
        return analyze_layout
    elif pathname == '/settings':
        return settings_layout
    elif pathname == '/envelope':
        return envelope_layout
    elif pathname == '/create_envelope':
        return envelope_creation_layout
    elif pathname == '/edit_envelope':
        return envelope_edit_layout
    elif pathname == '/edit_item':
        return edit_item_layout
    elif pathname == '/add_item':
        return add_item_layout
    else:
        return '404 Page not found'
    

app.layout = html.Div([
dcc.Location(id='url', refresh=False),
html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=False)