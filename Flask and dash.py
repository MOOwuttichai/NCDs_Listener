# # Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
from flask import Flask, request, render_template, session, redirect, url_for,jsonify

# # Incorporate data
# df = pd.read_csv('data_pre.csv')
# df = df.reset_index()
# # Initialize the app
# server = Flask(__name__)

# @server.route("/",methods = ['POST', 'GET'])
# def login():
#    if request.method == 'POST':
#       user = request.form['name']
#       return redirect(url_for('dashboard',name = user))
#    else:
#       user = request.args.get('name')
#       return render_template('login.html')
# app = Dash(server=server, routes_pathname_prefix="/dash/")
# app.layout = html.Div("{{ name }}")
# # App layout
# # app.layout = [
# #     html.Div(children='My First App with Data'),
# #     html.Div(children={{ name }}),
# #     dash_table.DataTable(data=df.to_dict('records'), page_size=10),
# #     dcc.Graph(figure=px.histogram(df, x='โรค', y='index', histfunc='avg')),
# #     dcc.Graph(figure=px.pie(df, values='index', names='ใครเล่า'))
# # ]

# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)
import dash
import dash_html_components as html
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

server = flask.Flask(__name__)

app1 = dash.Dash()
@server.route("/", methods=['GET'])
def home():
    fig = px.scatter(x=range(10), y=range(10))
    return render_template("login.html",fig=fig)


# app1 = dash.Dash(requests_pathname_prefix="/app1/")
# app1.layout = html.Div("Hello, Dash app 1!")

app2 = dash.Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Hello, Dash app 2!")

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server, "/app2": app2.server},
)

if __name__ == "__main__":
    run_simple("localhost", 8050, application)