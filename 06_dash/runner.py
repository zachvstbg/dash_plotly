from dash import Dash, Input, Output, callback, dash_table, State
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import datetime
import numpy as np

# Create dummy data
ratings = ['AAA', 'AA', 'A', 'BBB']
buckets = ['3y', '5y', '7y', '10y', '12y', '15y', '20y', '25y', '30y', '35y', '40y', '70y']

dummy_data = {}
for b in buckets:
    dummy_data[b] = {r: int(np.random.uniform(low=20, high=100, size=(1,))[0]) for r in ratings}

dummy_df = pd.DataFrame.from_records(dummy_data, index=ratings)
dummy_df = dummy_df[buckets]
dummy_df.reset_index(inplace=True)
dummy_df.rename(columns={'index': 'Rating'}, inplace=True)


# CALLBACKS
# ======================================================================================================================
@callback(
    Output(f'fade_desc', "is_in"),
    [Input(f'btn_desc', "n_clicks")],
    [State(f'fade_desc', "is_in")],
)
def toggle_description_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in


# Standard components
# ======================================================================================================================
def build_dash_graph(id: str):
    style = {'width': '72vh', 'height': '60vh'}
    colors = {'background': '#262626', 'text': '#cc7a00'}

    figure = {'layout': {'plot_bgcolor': colors['background'],
                         'paper_bgcolor': colors['background'],
                         'font': {'color': colors['text']}}}

    return dcc.Graph(id=id, style=style, figure=figure)


def build_dash_table(id: str, data):
    table = dash_table.DataTable(id=id, data=data,
                                 style_cell={'textAlign': 'center'},
                                 style_header={'backgroundColor': 'rgb(50, 50, 50)',
                                               'color': 'white',
                                               'border': '2px black'},
                                 style_data={'backgroundColor': 'rgb(80, 80, 80)',
                                             'color': 'white',
                                             'border': '1px black'},
                                 style_data_conditional=[{'if': {'state': 'active'},
                                                          'backgroundColor': '#cc7a00',
                                                          'border': '1px solid #cc7a00'
                                                          }])

    return table


# SUBSECTIONS
# ======================================================================================================================
# Input card
def build_card_user_inputs(id: str):
    date_picker = dcc.DatePickerSingle(id=f'date_input',
                                       initial_visible_month=datetime.date.today(),
                                       display_format='DD/MM/YYYY',
                                       date=datetime.date.today(),
                                       style={'font-size': '6px', 'display': 'inline-block'})

    input_tabs = dbc.Tabs([dbc.Tab(id=f'tab_input_buckets', label='Buckets'),
                           dbc.Tab(id=f'tab_input_costs', label='FVA Costs')])

    currency_drop = dbc.DropdownMenu(label="Currency", id=f'select-currency',
                                     children=[dbc.DropdownMenuItem("GBP"),
                                               dbc.DropdownMenuItem("EUR"),
                                               dbc.DropdownMenuItem("USD")])

    body = dbc.CardBody([html.H6("USER SELECTIONS: INPUTS"),
                         html.Hr(),
                         dbc.Row([dbc.Col(dbc.Label('Select CoB', html_for=f'date_input'), width=6),
                                  dbc.Col(date_picker, width=6)], justify="left", align="center"),
                         dbc.Row([dbc.Col(dbc.Label('Base Currency', html_for=f'select-currency')),
                                  dbc.Col(currency_drop, width=6)], justify="left", align="center"),
                         html.Br(),
                         dbc.Row(input_tabs),
                         html.Hr(),
                         dbc.Row([dbc.Button('Run Model', size='md', id=f'btn_run_model')])])
    return dbc.Card([body], id=id, style={"margin-left": "15px"})


# Analysis card
def build_card_user_analysis(id: str):
    body = dbc.CardBody([html.H6("USER SELECTIONS: ANALYSIS"),
                         html.Hr()])
    return dbc.Card([body], id=id, style={"margin-left": "15px"})

# Status card
def build_card_app_status(id: str):
    body = dbc.CardBody([html.H6("APP STATUS"),
                         html.Hr()])
    return dbc.Card([body], id=id, style={"margin-left": "15px"})


# Viewer card
def build_card_viewer(id: str):
    # Build tabs
    tab_gbp_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id=f'tbl_gbp_fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id=f'tbl_gbp_nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id=f'scatter_gbp_fin')),
                                dbc.Col(build_dash_graph(id=f'scatter_gbp_nonfin'))])]

    tab_eur_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id=f'tbl_eur_fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id=f'tbl_eur_nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id=f'scatter_eur_fin')),
                                dbc.Col(build_dash_graph(id=f'scatter_eur_nonfin'))])]

    tab_usd_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id=f'tbl_usd_fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id=f'tbl_usd_nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id=f'scatter_usd_fin')),
                                dbc.Col(build_dash_graph(id=f'scatter_usd_nonfin'))])]

    # Combine into a list
    viewer_tabs = dbc.Tabs([dbc.Tab(tab_gbp_content, id=f'tab_gbp', label='GBP'),
                            dbc.Tab(tab_eur_content, id=f'tab_eur', label='EUR'),
                            dbc.Tab(tab_usd_content, id=f'tab_usd', label='USD'),
                            dbc.Tab(id=f'tab_usd_muni', label='USD Muni'),
                            dbc.Tab(id=f'tab_custom', label='Custom')])

    body = dbc.CardBody([html.H6("INDEX VIEWER"),
                         html.Hr(),
                         viewer_tabs])

    return dbc.Card([body], id=id, style={"margin-left": "15px"})


# HELPERS = layout
# ======================================================================================================================
# Build a sample layout
def build_layout():
    # Separate components : Description (Fade)
    # ------------------------------------------------------------------------------------------------------------------
    desc_button = dbc.Button("Description", id=f'btn_desc', size="sm", n_clicks=0)
    desc_label = dbc.Label(
        "Provides an aggregated view of the main broad corporate bond indices - GBP (UC00), EUR (ER00) and USD (US00).",
        html_for=f'btn_desc')
    desc_fade = dbc.Fade(desc_label, id=f'fade_desc', is_in=False, appear=False)
    description_row = html.Div(dbc.Row([dbc.Col(desc_button, width='auto'),
                                        dbc.Col(desc_fade)], justify="left", align="center"),
                               style={"margin-left": "15px"})

    # Separate components : User Selections (Inputs)
    # ------------------------------------------------------------------------------------------------------------------
    user_selections_inputs = [dbc.Row(dbc.Card()),
                              dbc.Row(dbc.Card())]

    # Combining the components
    # ------------------------------------------------------------------------------------------------------------------
    section_top = [html.H3('LIQUID CREDIT VIEWER'),
                   html.Hr(),
                   description_row]

    # Constructing the overall layout
    # ------------------------------------------------------------------------------------------------------------------
    main_layout = [dbc.Row(section_top),
                   html.Br(),
                   dbc.Row([dbc.Col([dbc.Row([build_card_user_inputs(f'card_inputs')]),
                                     html.Br(),
                                     dbc.Row([build_card_user_analysis(f'card_analysis')]),
                                     html.Br(),
                                     dbc.Row([build_card_app_status(f'card_status')])], width=2),
                            dbc.Col([build_card_viewer(id=f'card_viewer')], width=10)])]

    # Define the data store
    dcc_stores = [dcc.Store(id=f'df_data')]

    # Define the main layout

    # Combine into a layout
    final_layout = dbc.Container(children=dcc_stores + main_layout, fluid=True)

    return final_layout


# CREATE THE APP + assign layout
# ======================================================================================================================
app = Dash(external_stylesheets=[dbc.themes.SLATE])
app.layout = build_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
