import dash_bootstrap_components as dbc
from dash import html

def create_navbar(nav_title):
    return dbc.Navbar(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="assets/favicon.jpg", height="30px")),
                        dbc.Col(dbc.NavbarBrand(nav_title, className="ml-2")),
                    ],
                    align="center",
                ),
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink("Home", href="/home")),
                        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
                        dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
                        dbc.DropdownMenu(
                            [
                                dbc.DropdownMenuItem("Action", href="#"),
                                dbc.DropdownMenuItem("Another action", href="#"),
                                # dbc.DropdownMenuItem(divider=True),
                                dbc.DropdownMenuItem("Separated link", href="#"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="Dropdown",
                        ),
                    ],
                    className="ml-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        color="dark",
        dark=True,
        sticky="top",
    )

