from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv('data_pre.csv')
df['count_plot'] = 1
last_10_columns = df.iloc[:, 10:-1]
last_10_columns
dfm = last_10_columns.melt()
plot_df = (
 pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
)
plot_data=plot_df['มีการเล่า'].reset_index()
plot_sym=plot_data

app.layout = html.Div([
    html.H4('Analysis of the restaurant sales'),
    dcc.Graph(id="graph"),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=df['defind_cancer_with_nlp'].unique(),
        clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['count_plot'],
        value='total_bill', clearable=False
    ),
])


@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"), 
    Input("values", "value"))
def generate_chart(names, values):
    df = px.data.tips() # replace with your own data source
    n_mane = df[df['defind_cancer_with_nlp']==names]
    fig = px.pie(df, values=df[values], names=df[df['defind_cancer_with_nlp']==names], hole=.3)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
