from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)
data_for_dash_facebook = pd.read_csv('data_pre.csv')
data_for_dash_facebook['count_plot'] = 1
sym_o_th = data_for_dash_facebook.iloc[:, 13:-1]
sym_o1_th = sym_o_th.melt()
sym_o2_th = (pd.crosstab(sym_o1_th['variable'], sym_o1_th['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
app.layout = html.Div([html.Div([
        html.Div([
            html.P("ประสบการณ์:"),
            dcc.Checklist(id='pie-charts-exp-names',
                options=data_for_dash_facebook['ใครเล่า'].unique(),
                value=data_for_dash_facebook['ใครเล่า'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("เพศ:"),
            dcc.Checklist(id='pie-charts-Gender-names',
                options=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique(),
                value=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("โรค:"),
            dcc.Dropdown(id='pie-charts-cancer-names',
                options=data_for_dash_facebook['โรค'].unique(),
                value=data_for_dash_facebook['โรค'].unique(),multi=True),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("ความมีประโยชน์:"),
            dcc.Checklist(id="pie-charts-useful-names",
                options=data_for_dash_facebook['โรค_clust'].unique(),
                value=data_for_dash_facebook['โรค_clust'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("อาการ:"),
            dcc.Dropdown(id='pie-charts-sym-names',
                options=sym_o2_th['variable'].unique(),
                multi=True),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("จำนวน like(ขั้นต่ำ):"),
            dcc.Slider(0, 1000, 50,
               value=0,tooltip={"placement": "bottom", "always_visible": True},
               id='slider-count_like-names'),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("จำนวนการตอบกลับ(ขั้นต่ำ):"),
            dcc.Slider(0, 1000, 50,
               value=0,tooltip={"placement": "bottom", "always_visible": True},
               id='slider-count_rechat-names'),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
            dcc.Slider(0, 1000, 50,
               value=0,tooltip={"placement": "bottom", "always_visible": True},
               id='slider-count_word-names'),
            ],style={'width': '49%', 'display': 'inline-block'}),
    ]),
    # exp
    html.Div([dcc.Graph(id="pie-charts-exp-graph")],style={'width': '49%',  'display': 'inline-block'}),
    # Gender
    html.Div([dcc.Graph(id="pie-charts-Gender-graph")],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    # carcer
    html.Div([dcc.Graph(id="his-charts-carcer-graph")],style={'width': '49%', 'display': 'inline-block'}),
    # useful
    html.Div([dcc.Graph(id="pie-charts-useful-graph")],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    # sym
    html.Div([dcc.Graph(id="his-charts-sym-graph")],style={'width': '49%','display': 'inline-block'}),
    # word count
    html.Div([dcc.Graph(id="line-charts-like-graph")],style={'width': '49%','float': 'right','display': 'inline-block'}),
    # word count
    html.Div([dcc.Graph(id="line-charts-rechat-graph")],style={'width': '49%','display': 'inline-block'}),
    # word count
    html.Div([dcc.Graph(id="line-charts-count_word-graph")],style={'width': '49%','float': 'right','display': 'inline-block'})
])

@app.callback(
    Output("pie-charts-exp-graph", "figure"),
    Output("pie-charts-Gender-graph", "figure"),
    Output("his-charts-carcer-graph", "figure"), 
    Output("pie-charts-useful-graph", "figure"),
    Output("his-charts-sym-graph", "figure"),
    Output("line-charts-like-graph", "figure"),
    Output("line-charts-rechat-graph", "figure"),
    Output("line-charts-count_word-graph", "figure"),  
    Input("pie-charts-exp-names", "value"),
    Input("pie-charts-Gender-names", "value"),
    Input("pie-charts-cancer-names", "value"),
    Input("pie-charts-useful-names", "value"),
    Input("pie-charts-sym-names", "value"),
    Input("slider-count_like-names", "value"),
    Input("slider-count_rechat-names", "value"),
    Input("slider-count_word-names", "value"),
    )
def generate_chart(exp,Gender,carcer,useful,sym,count_like,count_rechat,count_word):
    nms = data_for_dash_facebook
    if sym == [] or sym is None:
        nms = data_for_dash_facebook
    else:
        for defind_sym in range(len(sym)):
            x = nms[nms[sym[defind_sym]]==1]
            nms = x           
    nms = nms[nms['ใครเล่า'].isin(exp)]
    nms = nms[nms['เพศเเบ่งโดยใช้_python'].isin(Gender)]
    nms = nms[nms['โรค'].isin(carcer)]
    nms = nms[nms['โรค_clust'].isin(useful)]
    nms = nms[nms['like']>=count_like]
    nms = nms[nms['rechat']>=count_rechat]
    nms = nms[nms['count']>=count_word] 
    print(nms)
    sym_c = nms.iloc[:, 13:-1]
    sym_ca = sym_c.melt()
    sym_can = (pd.crosstab(sym_ca['variable'], sym_ca['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'}))
    plot_data=sym_can['มีการเล่า'].reset_index()
    if sym == [] or sym is None :
        plot_data_None = plot_data
        plot_sym=plot_data_None[plot_data_None['มีการเล่า'] != 0]
    elif len(sym) == 1:
        plot_data_None = plot_data
        plot_sym=plot_data_None[plot_data_None['มีการเล่า'] != 0]
    else:
        x_value=plot_data[plot_data['variable'].isin(sym)]['มีการเล่า'].to_list()
        x_name=plot_data[plot_data['variable'].isin(sym)]['variable'].to_list()
        sum_name =""
        for sum_name_count in x_name:
            if sum_name == "":
                sum_name = sum_name+sum_name_count
            else:
                sum_name = sum_name+"&"+sum_name_count
        x_plot_1 = pd.DataFrame(data={'variable': sum_name, 'มีการเล่า': x_value})
        plot_data_non=plot_data[plot_data.variable.isin(sym) == False]
        plot_data_nonnone=pd.concat([plot_data_non,x_plot_1])
        plot_sym=plot_data_nonnone.drop_duplicates()
        plot_sym = plot_sym[plot_sym['มีการเล่า']!=0]
    fig_1 = px.pie(nms, values='count_plot', names=nms['ใครเล่า'])
    fig_2 = px.pie(nms, values='count_plot', names=nms['เพศเเบ่งโดยใช้_python'])
    fig_3 = px.histogram(nms, x=nms['โรค'], y='count_plot',barmode='group')
    fig_4 = px.pie(nms, values='count_plot', names=nms['โรค_clust'])
    fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group')
    fig_6 = px.line(nms,x='ชื่อ', y='like')
    fig_7 = px.line(nms,x='ชื่อ', y='rechat')
    fig_8 = px.line(nms,x='ชื่อ', y='count')
    return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8]

if __name__ == "__main__":
    app.run_server(debug=True)
