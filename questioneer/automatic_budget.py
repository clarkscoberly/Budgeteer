import dash_bootstrap_components as dbc
from app import db
from dash import html, dcc, dash

# u is under and o is over
age_expenditure = {
    "u25": 30373,
    "u34": 48087,
    "u44": 58784,
    "u54": 60524,
    "u64": 55892,
    "u74": 46757,
    "o75": 34382
}

def automatic_budget_creation(family_size, ages, savings_level): 
    try:
        total_rent = 0
        total_groceries = 0
        total_eating_out = 0
        total_entertainment = 0
        total_gifts = 0
        total_grooming = 0

        for age in ages:
            if age <= 25:
                key = "u25"
            elif age <= 34:
                key = "u34"
            elif age <= 44:
                key = "u44"
            elif age <= 54:
                key = "u54"
            elif age <= 64:
                key = "u64"
            elif age <= 74:
                key = "u74"
            else:
                key = "075"

            if savings_level == "low":
                cost = age_expenditure[key] / 12
                rent = cost * .35
                groceries = cost * .27
                eating_out = cost * .12
                entertainment = cost * .9
                gifts = cost * .12
                grooming = cost * .5

            elif savings_level == "medium":
                cost = age_expenditure[key] / 12
                
                rent = (cost * .35) * .75
                groceries = (cost * .27) * .75
                eating_out = (cost * .12) * .75
                entertainment = (cost * .09) * .75
                gifts = (cost * .12) * .75
                grooming = (cost * .05) * .75
            else: # Savings == "high"
                rent = 500
                groceries = 125
                eating_out = 60
                entertainment = 20
                gifts = 30
                grooming = 10

            total_rent += rent
            total_groceries += groceries
            total_eating_out += eating_out
            total_entertainment += entertainment
            total_gifts += gifts
            total_grooming += grooming
    except Exception as e:
        print(e)

    total_rent = round(total_rent)
    total_groceries = round(total_groceries)
    total_eating_out = round(total_eating_out)
    total_entertainment = round(total_entertainment)
    total_gifts = round(total_gifts)
    total_grooming = round(total_grooming)
    
    db.create_envelope("Rent", total_rent, "Monthly", "One Budget For All And All For The Budget")
    db.create_envelope("Groceries", total_groceries, "Monthly", "One Budget For All And All For The Budget")
    db.create_envelope("Eating Out", total_eating_out, "Monthly", "One Budget For All And All For The Budget")
    db.create_envelope("Entertainment", total_entertainment, "Monthly", "One Budget For All And All For The Budget")
    db.create_envelope("Gifts", total_gifts, "Monthly", "One Budget For All And All For The Budget")
    db.create_envelope("Grooming", total_grooming, "Monthly", "One Budget For All And All For The Budget")

def create_questioneer_decision():
    return dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Button("Create Automatic Budget", href="/questioneer_layout")),
            dbc.Col(dbc.Button("I'd Like To Make My Own", href="/home")),
        ])
    ])

def create_questioneer_layout():
    return dbc.Container([
        html.H1('Family Budget Creator', className='text-center mt-3 mb-4'),
        dbc.Row([
            dbc.Col([
                html.Label('Family Size', className='form-label'),
                dcc.Input(id='family_size', type='number', placeholder='Enter family size', className='form-control mb-3')
            ], width=6, className='mx-auto'),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Family Member Ages', className='form-label'),
                html.Div(id='age_inputs_container', children=[]),
                # dbc.Button('Add Family Member', id='add_member_button', color='primary', className='mt-3'),
            ], width=6, className='mx-auto'),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Savings Level', className='form-label'),
                dcc.Dropdown(
                    id='savings_level',
                    options=[
                        {'label': 'Low', 'value': 'low'},
                        {'label': 'Medium', 'value': 'medium'},
                        {'label': 'High', 'value': 'high'},
                    ],
                    placeholder='Select savings level',
                    className='mb-3'
                ),
                dbc.Button('Confirm Choices', id='confirm_button', color='primary', className='mt-3', href="/home"),
            ], width=6, className='mx-auto'),
        ]),
    ], className='py-4')