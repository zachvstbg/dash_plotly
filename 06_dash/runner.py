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
    Output("fade", "is_in"),
    [Input("fade-button", "n_clicks")],
    [State("fade", "is_in")],
)
def toggle_description_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return False
    return not is_in


# Standard components
# ======================================================================================================================
def build_dash_graph(id: str):
    style = {'width': '60vh', 'height': '60vh'}
    return dcc.Graph(id=id, style=style)


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
                                                          'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                                                          'border': '1px solid rgb(0, 116, 217)'
                                                          }])

    return table


# # HELPERS = callback
# # ======================================================================================================================
# @callback(Output('df_data', 'data'), Input(f'run-button', 'value'))
# def generate_numbers(n_clicks: int):
#     n = 10
#     numbers = np.random.uniform(low=-10, high=15, size=(n,n))
#     data = {str(x): numbers[x] for x in range(0, n)}
#     df = pd.DataFrame.from_dict(data, orient='index')
#     return df.to_json()
#
#
# @callback(Output('table-average', 'data'), Input('df_data', 'data'))
# def update_table(df_string: str):
#     df = pd.read_json(df_string)
#     averages = {x : np.mean(df[x]) for x in df.columns}
#     df_averages = pd.DataFrame.from_dict(averages, orient='index')
#     return df_averages.to_dict("records")
#
# @callback(Output(f'tbl_out', 'children'),
#           [Input(f'table-average', 'active_cell'), Input('df_data', 'data')])
# def update_graphs(active_cell, df_serialised):
#     if active_cell:
#         # Take the row
#         row = active_cell['row']
#
#         # Deserialise the data into a dataframe
#         df = pd.read_json(df_serialised)
#         data = df[row]
#
#         output = data.values.tolist()
#
#         # Graph doesnt quite work - don't know why
#         # fig = go.Bar(x=data.index.to_list(), y=data.values.tolist())
#
#         return output
#     else:
#         return "Click on a cell"


# HELPERS = layout
# ======================================================================================================================
# Build a sample layout
def build_layout():
    # Separate components : Description (Fade)
    # ------------------------------------------------------------------------------------------------------------------
    description_button = dbc.Button("Description", id="fade-button", size="sm", className="mb-3", n_clicks=0)
    description_text = html.P(
        "Provides an aggregated view of the main broad corporate bond indices - GBP (UC00), EUR (ER00) and USD (US00).",
        className="description-text")
    description_fade = dbc.Fade(description_text, id="fade", is_in=False, appear=False)

    description_row = html.Div(dbc.Row([dbc.Col(description_button, width='auto'),
                                        dbc.Col(description_fade)]))

    # Separate components : User Selections (Inputs)
    # ------------------------------------------------------------------------------------------------------------------
    user_selections_inputs = [html.H6('USER SELECTIONS: Inputs'),
                              dbc.Row([dbc.Col(html.P('CoB Date'), width=4),
                                       dbc.Col(dcc.DatePickerSingle(id=f'date-selector',
                                                                    initial_visible_month=datetime.date.today(),
                                                                    display_format='DD/MM/YYYY',
                                                                    date=datetime.date.today()), width=8)])]

    # Separate components : User Selections (Inputs)
    # ------------------------------------------------------------------------------------------------------------------
    user_selections_analysis = [html.H6('USER SELECTIONS: Analysis')]

    # Separate components : Viewer
    # ------------------------------------------------------------------------------------------------------------------
    tab_gbp_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id='tbl-gbp-fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id='tbl-gbp-nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id='scatter-gbp-fin')),
                                dbc.Col(build_dash_graph(id='scatter-gbp-nonfin'))])]

    tab_eur_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id='tbl-eur-fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id='tbl-eur-nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id='scatter-eur-fin')),
                                dbc.Col(build_dash_graph(id='scatter-eur-nonfin'))])]

    tab_usd_content = [html.Br(),
                       dbc.Row([dbc.Col(build_dash_table(id='tbl-usd-fin', data=dummy_df.to_dict('records'))),
                                dbc.Col(build_dash_table(id='tbl-usd-nonfin', data=dummy_df.to_dict('records')))]),
                       html.Br(),
                       dbc.Row([dbc.Col(build_dash_graph(id='scatter-usd-fin')),
                                dbc.Col(build_dash_graph(id='scatter-usd-nonfin'))])]

    viewer_tabs = dbc.Tabs([dbc.Tab(tab_gbp_content, id='tab-gbp', label='GBP'),
                            dbc.Tab(tab_eur_content, id='tab-eur', label='EUR'),
                            dbc.Tab(tab_usd_content, id='tab-usd', label='USD')])

    viewer = [html.H6('INDEX VIEWER'),
              dbc.Row(viewer_tabs)]

    # Combining the components
    # ------------------------------------------------------------------------------------------------------------------
    section_top = [html.H3('LIQUID CREDIT VIEWER'),
                   html.Hr(),
                   description_row]

    # Constructing the overall layout
    # ------------------------------------------------------------------------------------------------------------------
    main_layout = [dbc.Row(children=section_top),
                   html.Br(),
                   dbc.Row([dbc.Col([dbc.Row(user_selections_inputs),
                                     html.Br(),
                                     dbc.Row(user_selections_analysis)], width=2),
                            dbc.Col(viewer, width=10)])]

    # # Define components
    # parameters = [html.H3('Random App'),
    #               dbc.Label('Select date', html_for=f'date-selector'),
    #               dbc.Col(dcc.DatePickerSingle(id=f'date-selector',
    #                                            initial_visible_month=datetime.date.today(),
    #                                            display_format='DD/MM/YYYY',
    #                                            date=datetime.date.today())),
    #               dbc.Label('Run averages', html_for=f'run-button'),
    #               dbc.Button("Run", size='sm', id=f'run-button', n_clicks=0)]
    #
    # output = [html.Hr(),
    #           dbc.Label('Table: average', html_for=f'table-average'),
    #           dash_table.DataTable(id=f'table-average', data = dummy_df.to_dict("records")),
    #           dbc.Alert(id='tbl_out'),
    #           html.Hr(),
    #           dcc.Graph(id=f'bar_chart')]

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
