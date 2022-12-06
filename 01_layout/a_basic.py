from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Instantiates the DASH app
app = Dash(__name__)

# This is the data source
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

# Figure object for the chart - bar chart
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# Layout
# html.Div is a standard component - can define a number of children
# dcc.Graph - is the container for the figure
# id - this is how components are tagged, registered and identified
app.layout = html.Div(children=[
    html.H1(children='Mad Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)