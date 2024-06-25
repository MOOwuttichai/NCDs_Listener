# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('data_pre.csv')
df = df.reset_index()
# Initialize the app
app = Dash()

# App layout
app.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='โรค', y='index', histfunc='avg')),
    dcc.Graph(figure=px.pie(df, values='index', names='ใครเล่า'))
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)