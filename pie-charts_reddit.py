from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

app = Dash(__name__)

data_for_dash_raddit = pd.read_csv('Book1.csv')
data_for_dash_raddit['count_plot'] = 1
sym_o = data_for_dash_raddit.iloc[:, 10:-1]
sym_o1 = sym_o.melt()
sym_o2 = (pd.crosstab(sym_o1['variable'], sym_o1['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
app.layout = html.Div([html.Div([
        html.Div([
            html.P("exp:"),
            dcc.Checklist(id='pie-charts-exp-names',
                options=data_for_dash_raddit['defind_exp_with_python'].unique(),
                value=data_for_dash_raddit['defind_exp_with_python'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("Gender:"),
            dcc.Checklist(id='pie-charts-Gender-names',
                options=data_for_dash_raddit['defind_Genden_with_nlp'].unique(),
                value=data_for_dash_raddit['defind_Genden_with_nlp'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("cancer:"),
            dcc.Dropdown(id='pie-charts-cancer-names',
                options=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),
                value=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),multi=True),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("useful:"),
            dcc.Checklist(id="pie-charts-useful-names",
                options=data_for_dash_raddit['cancer_clusternd'].unique(),
                value=data_for_dash_raddit['cancer_clusternd'].unique()),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("sym:"),
            dcc.Dropdown(id='pie-charts-sym-names',
                options=sym_o2['variable'].unique(),
                multi=True),
            ],style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.P("word count:"),
            dcc.Slider(0, 1000, 50,
               value=100,tooltip={"placement": "bottom", "always_visible": True},
               id='slider-count_word-names'),
            ],style={'width': '49%', 'display': 'inline-block'}),
    ]),
    # exp
    html.Div([dcc.Graph(id="pie-charts-exp-graph")],style={'width': '49%',  'display': 'inline-block'}),
    # Gender
    html.Div([dcc.Graph(id="pie-charts-Gender-graph")],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    # carcer
    html.Div([dcc.Graph(id="pie-charts-carcer-graph")],style={'width': '49%', 'display': 'inline-block'}),
    # useful
    html.Div([dcc.Graph(id="pie-charts-useful-graph")],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    # sym
    html.Div([dcc.Graph(id="pie-charts-sym-graph")],style={'width': '49%','display': 'inline-block'}),
    # word count
    html.Div([dcc.Graph(id="pie-charts-count_word-graph")],style={'width': '49%','float': 'right','display': 'inline-block'})
])

@app.callback(
    Output("pie-charts-exp-graph", "figure"),
    Output("pie-charts-Gender-graph", "figure"),
    Output("pie-charts-carcer-graph", "figure"), 
    Output("pie-charts-useful-graph", "figure"),
    Output("pie-charts-sym-graph", "figure"),
    Output("pie-charts-count_word-graph", "figure"),  
    Input("pie-charts-exp-names", "value"),
    Input("pie-charts-Gender-names", "value"),
    Input("pie-charts-cancer-names", "value"),
    Input("pie-charts-useful-names", "value"),
    Input("pie-charts-sym-names", "value"),
    Input("slider-count_word-names", "value"),
    )
def generate_chart(exp,Gender,carcer,useful,sym,count_word):
    nms = data_for_dash_raddit
    if sym == [] or sym is None:
        nms = data_for_dash_raddit
    else:
        for defind_sym in range(len(sym)):
            x = nms[nms[sym[defind_sym]]==1]
            nms = x            
    nms = nms[nms['defind_exp_with_python'].isin(exp)]
    nms = nms[nms['defind_Genden_with_nlp'].isin(Gender)]
    nms = nms[nms['defind_cancer_with_nlp'].isin(carcer)]
    nms = nms[nms['cancer_clusternd'].isin(useful)]
    sym_c = nms.iloc[:, 10:-1]
    sym_ca = sym_c.melt()
    sym_can = (pd.crosstab(sym_ca['variable'], sym_ca['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'}))
    plot_data=sym_can['มีการเล่า'].reset_index()
    print(sym)
    if sym == [] or sym is None :
        plot_data_None = plot_data
        plot_sym=plot_data_None
    elif len(sym) == 1:
        plot_data_None = plot_data
        plot_sym=plot_data_None
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
    print(plot_sym)
    print(nms)
    nms = nms[nms['count']>=count_word]
    fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'])
    fig_2 = px.pie(nms, values='count_plot', names=nms['defind_Genden_with_nlp'])
    fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'], y='count_plot',barmode='group')
    fig_4 = px.pie(nms, values='count_plot', names=nms['cancer_clusternd'])
    fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group')
    list_count_list = []
    for list_count in range(len(nms['count'])):
        list_count_list.append(list_count)
    nms['number'] = list_count_list
    fig_6 = px.line(nms,x='name', y='count')
    return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6]

if __name__ == "__main__":
    app.run_server(debug=True)
