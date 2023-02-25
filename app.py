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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


title = dcc.Markdown(children="# **Budgeteer**")



login_layout = create_login_layout()
account_creation_layout = create_account_creation_layout()
home_layout = create_home_layout()
analyze_layout = create_analytics_layout()
settings_layout = create_settings_layout()


# Define the callback for login validation
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

    # There is currently a bug in which you type a character and then delete it thus creating a username without having any letters.
    elif new_username == None:
        return "Username Cannot Be Empty"
    else:
        # Code to create new account
        return dcc.Location(pathname="/", id="home")


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
    else:
        return '404 Page not found'
    

app.layout = html.Div([
dcc.Location(id='url', refresh=False),
html.Div(id='page-content')
])


if __name__ == '__main__':
    app.run_server(debug=True)