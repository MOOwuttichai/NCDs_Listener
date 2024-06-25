import plotly
import plotly.graph_objs as go
from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template #this has changed
import plotly.express as px
import dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


server = Flask(__name__)

@server.route('/')
def index():
    return render_template('login.html') #this has changed


app1 = dash.Dash(requests_pathname_prefix="/app1/")
df = pd.read_csv('data_pre.csv')
df = df.reset_index()
# เพศ/ประสบการณ์/
df['count_plot'] = 1
#โรค
df_can = df[['count_plot','โรค']].groupby(['โรค']).sum().reset_index()
df_can = df_can[df_can['โรค']!= 'ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น']
# อาการ
last_10_columns = df.iloc[:, 12:-1]
last_10_columns
dfm = last_10_columns.melt()
plot_df = (
    pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
)
plot_data=plot_df['มีการเล่า'].reset_index()
plot_sym=plot_data[plot_data['variable'] != 'ไม่มีการระบุอาการ']
app1.layout = [
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.bar(df_can, x='โรค', y='count_plot')),
    dcc.Graph(figure=px.pie(df, values='count_plot', names='ใครเล่า')),
    dcc.Graph(figure=px.pie(df, values='count_plot', names='เพศเเบ่งโดยใช้_python')),
    dcc.Graph(figure=px.histogram(plot_sym, x='variable', y='มีการเล่า', histfunc='avg')),
]


application = DispatcherMiddleware(
    server,
    {"/app1": app1.server},
)
if __name__ == '__main__':
    run_simple("localhost", 8050, application)

