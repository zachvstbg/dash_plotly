from dash import Dash, Input, Output, callback, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import datetime
import numpy as np
import plotly.graph_objs as go

dummy_df = pd.DataFrame([[None]])

# HELPERS = callback
# ======================================================================================================================
@callback(Output('df_data', 'data'), Input(f'run-button', 'value'))
def generate_numbers(n_clicks: int):
    n = 10
    numbers = np.random.uniform(low=-10, high=15, size=(n,n))
    data = {str(x): numbers[x] for x in range(0, n)}
    df = pd.DataFrame.from_dict(data, orient='index')
    return df.to_json()


@callback(Output('table-average', 'data'), Input('df_data', 'data'))
def update_table(df_string: str):
    df = pd.read_json(df_string)
    averages = {x : np.mean(df[x]) for x in df.columns}
    df_averages = pd.DataFrame.from_dict(averages, orient='index')
    return df_averages.to_dict("records")

@callback(Output(f'tbl_out', 'children'),
          [Input(f'table-average', 'active_cell'), Input('df_data', 'data')])
def update_graphs(active_cell, df_serialised):
    if active_cell:
        # Take the row
        row = active_cell['row']

        # Deserialise the data into a dataframe
        df = pd.read_json(df_serialised)
        data = df[row]

        output = data.values.tolist()

        # Graph doesnt quite work - don't know why
        # fig = go.Bar(x=data.index.to_list(), y=data.values.tolist())

        return output
    else:
        return "Click on a cell"



# HELPERS = layout
# ======================================================================================================================
# Build a sample layout
def build_layout():
    # Define components
    parameters = [html.H3('Random App'),
                  dbc.Label('Select date', html_for=f'date-selector'),
                  dbc.Col(dcc.DatePickerSingle(id=f'date-selector',
                                               initial_visible_month=datetime.date.today(),
                                               display_format='DD/MM/YYYY',
                                               date=datetime.date.today())),
                  dbc.Label('Run averages', html_for=f'run-button'),
                  dbc.Button("Run", size='sm', id=f'run-button', n_clicks=0)]

    output = [html.Hr(),
              dbc.Label('Table: average', html_for=f'table-average'),
              dash_table.DataTable(id=f'table-average', data = dummy_df.to_dict("records")),
              dbc.Alert(id='tbl_out'),
              html.Hr(),
              dcc.Graph(id=f'bar_chart')]

    # Define the data store
    dcc_stores = [dcc.Store(id=f'df_data')]

    # Define the main layout
    main_layout = [dbc.Row([dbc.Col(children=parameters + output)])]

    # Combine into a layout
    final_layout = dbc.Container(children=dcc_stores + main_layout, fluid=True)

    return final_layout


# CREATE THE APP + assign layout
# ======================================================================================================================
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = build_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
