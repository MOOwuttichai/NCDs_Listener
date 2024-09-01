from dash import Dash, html, Input, Output, callback,dcc,dash_table,no_update,dash
import pandas as pd
import plotly.express as px
import os
import dash_bootstrap_components as dbc
import dash_daq as daq
css_tab_STYLE = {'width': '45%','display': 'inline-block','font-family':'THSarabunNew','font-size': '20px','margin-left': '3%','margin-top': '2%'}
css_tab_STYLE_v2 = {'font-family':'THSarabunNew','font-size': '20px','align-items': 'center', 'justify-content': 'center'}
css_pie_STYLE = {'font-family':'THSarabunNew','font-size': '20px','align-items': 'center', 'justify-content': 'center'}
css_bar_and_line_STYLE={'align-items': 'center', 'justify-content': 'center','font-family':'THSarabunNew','font-size': '20px'}
css_slider_style = {'width': '90%', 'display': 'inline-block','font-family':'THSarabunNew','font-size': '20px','margin-left': '3%'}
css_grahp_name_style={'text-align': 'center','font-family':'THSarabunNew','font-size': '20px'}
css_summare_text = {'text-align': 'left','font-size': '20px','font-family':'THSarabunNew','width': 'auto','margin-left': '9%','margin-top': '9%'}
css_summare_text_v2 = {'text-align': 'left','whiteSpace': 'pre-line','font-size': '20px','font-family':'THSarabunNew','width': 'auto','margin-left': '9%','margin-top': '9%'}
css_summare_text_v = {'box-shadow':' 0 4px 8px 0 rgba(0, 0, 0, 0.2)','border-radius': '18px','backgroundColor':'#d0f8ce','margin-left': '5%'}
css_label_fillter = {'font-size': '20px','text-shadow': '0 0 6px #66B032','font-weight': 'bold'}
time_run_va = {'time_run':[0]}
time_run= pd.DataFrame(time_run_va)
time_run.to_csv('time_run.csv',index=False)
app = dash.Dash(__name__)
app.layout =  html.Div([
        html.Div([
        html.Div([
            html.H1('สรุปความคิดเห็นของข้อมูลที่ดึงมาโดย Google Gemini',style={'text-align': 'center','font-family':'THSarabunNew','box-shadow':' 0 4px 8px 0 rgba(0, 0, 0, 0.2)','backgroundColor':'#59caa4','border-radius': '18px'}),
            html.P(id ="text_sum_bybot",style={'whiteSpace': 'pre-line','font-family':'THSarabunNew','font-size': '25px','height': '500px','overflowY': 'auto'}),
        ],style={'margin-left': 10,'margin-right': 10,'margin-top': 10})
        ],style={'backgroundColor':'#d0f8ce','box-shadow':' 0 4px 8px 0 rgba(0, 0, 0, 0.2)','border-radius': '18px'}),
html.Div([
        html.Div([
        html.P('เรียงลำดับข้อมูลในตารางตาม "จำนวนคำ" : ',style={'display': 'inline-block','font-family':'THSarabunNew','font-size': '25px'}),
        dcc.Dropdown(id='soft_table',options=['มากไปน้อย','น้อยไปมาก'],value ='น้อยไปมาก',style={'width': '300px','display': 'inline-block','margin-left': 10,'font-size': '20px','font-family':'THSarabunNew'}),
        ],style={'margin-left': '25%'}),
        html.Div([
        dcc.Interval( id="interval",n_intervals=0,),
        dcc.Interval( id="interval_v_o",n_intervals=0,),
        html.Div(id='datatable',style={'height': '500px','overflowY': 'auto','margin-top': 12}),
        ]),
html.H1("Dashboard",style={'text-align': 'center','font-family':'THSarabunNew'}),
dbc.Container([
    html.Div([
        html.Div([
                html.P("ความมีประโยชน์:",style=css_label_fillter),
                dcc.Checklist(id="pie-charts-useful-names"),
                ],style=css_tab_STYLE),
        html.Div([
                html.P("จำนวนคำ 'ขั้นต่ำ' ที่มีประโยชน์:",style=css_label_fillter),
                dcc.Input(id='my-numeric-input-1',type= "number",placeholder="จำนวนคำ 'ขั้นต่ำ' ที่มีประโยชน์",value = 3)
                ],style=css_tab_STYLE),
        html.Div([
            html.P("ประสบการณ์:",style=css_label_fillter),
            dcc.Checklist(id='pie-charts-exp-names')
            ],style=css_tab_STYLE),
        html.Div([
            html.P("เพศ:",style=css_label_fillter),
            dcc.Checklist(id='pie-charts-Gender-names')
            ],style=css_tab_STYLE),
        html.Div([
        html.P("โรค:",style=css_label_fillter),
            dcc.Dropdown(id='pie-charts-cancer-names',multi=True)
            ],style=css_tab_STYLE_v2),
        html.Div([
            html.P("อาการ:",style=css_label_fillter),
            dcc.Dropdown(id='pie-charts-sym-names',multi=True)
            ],style=css_tab_STYLE_v2),
        html.Div([
            html.P("จำนวนคำในประโยค(ขั้นต่ำ):",style=css_label_fillter),
            dcc.Slider(0,200,200/5,value=0,
                tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_word-names'),
            ],style=css_slider_style),
        html.Div([
            html.P("จำนวนการตอบกลับ(ขั้นต่ำ):",style=css_label_fillter),
            dcc.Slider(0, 100, 100/5,
                value=0,tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_rechat-names'),
            ],style=css_slider_style),
        html.Div([
            html.P("จำนวน like(ขั้นต่ำ):",style=css_label_fillter),
            dcc.Slider(0, 500, 500/5,
                value=0,tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_like-names'),
            ],style=css_slider_style),
    ],style={
        'width': 500,
        'margin-left': 20,
        'margin-top': 35,
        'margin-bottom': 35,
        'height':1000,
        'backgroundColor':'#d0f8ce',
        'overflowY': 'auto',
        'border-radius': '18px',
        'margin-right': '12px',
        'box-shadow': '0 4px 8px 0 rgba(0, 0, 0, 0.2)',
        }),
    html.Div([
    dbc.ModalBody([
        html.Div([
            html.H3("แผนภูมิ ความมีประโยชน์กับจำนวนความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="pie-charts-useful-graph",style=css_pie_STYLE),
            html.Div([
            html.P(id ="text_sum_useful",style=css_summare_text),
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ การเล่าประสบการณ์กับจำนวนความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="pie-charts-exp-graph",style=css_pie_STYLE),
            html.Div([
            html.P(id = 'text_sum_exp',style=css_summare_text)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ เพศผู้ป่วยกับจำนวนความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="pie-charts-Gender-graph",style=css_pie_STYLE),
            html.Div([
            html.P(id = 'text_sum_Gender',style=css_summare_text)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ โรคกับจำนวนความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="pie-charts-carcer-graph",style=css_tab_STYLE_v2),
            html.Div([
            html.P(id = 'text_sum_cancer',style=css_summare_text_v2)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ อาการกับจำนวนความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="his-charts-sym-graph",style=css_tab_STYLE_v2),
            html.Div([
            html.P(id ="text_sum_sym",style=css_summare_text_v2)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ จำนวนคำกับชื่อผู้ที่มาเเสดงความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="line-charts-count_word-graph",style=css_bar_and_line_STYLE),
            html.Div([
            html.P(id ="text_sum_word",style=css_summare_text_v2)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ จำนวนยอดไลน์กับชื่อผู้ที่มาเเสดงความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="line-charts-like-graph",style=css_bar_and_line_STYLE),
            html.Div([
            html.P(id ="text_sum_like",style=css_summare_text_v2)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        html.Div([
            html.H3("แผนภูมิ จำนวนการตอบกลับกับชื่อผู้ที่มาเเสดงความคิดเห็น",style=css_grahp_name_style),
            dcc.Graph(id="line-charts-rechat-graph",style=css_bar_and_line_STYLE),
            html.Div([
            html.P(id ="text_sum_reply",style=css_summare_text_v2)
            ],style=css_summare_text_v),
        ],style={'width': 'auto'}),
        #กรอบ print
        ],id="grid-print-area")#,style={'display':'grid','grid-template-columns': "50% 50%"}
    ],
        style={
            'width': 1000,
            'height':1000,
            'margin-top': 35,
            'margin-right': 10,
            'margin-bottom': 35,
            'box-shadow':' 0 4px 8px 0 rgba(0, 0, 0, 0.2)',
            'border-radius': '18px',
            'overflowY': 'auto',
            'display':'flex'
        }),html.Div(id="dummy"),
]   ,fluid=True,
    style={'display': 'flex'},),
html.Div([
dbc.Button("Print", id="grid-browser-print-btn"),
# ,style={'height': '60px','width': '200px','textAlign': 'center'
#                                                         ,'background-color': '#04AA6D','color':' white','border-radius': '12px',
#                                                         'align-items': 'center','font-size': '24px','display': 'flex',
#                                                         'justify-content': 'center','margin-left': '43%','margin-top': 30,'border-color':'white',
#                                                         'box-shadow': '2px 2px 20px 10px #7fecad'}
]),                                                            
]),
])
@callback(
    Output(component_id='interval', component_property='interval'),
    Input("interval", "n_intervals"),
)
def inten_n (n):
    time_run = pd.read_csv('time_run.csv')
    if time_run.iloc[0,0] == 0:
        time_run.iloc[0,0] = 1
        time_run.to_csv('time_run.csv',index=False)
        return 5*1000
    else:
        return 210*1000
@callback(
    Output('pie-charts-exp-names', "options",allow_duplicate=True),
    Output('pie-charts-exp-names', "value",allow_duplicate=True),
    Output('pie-charts-cancer-names', "options",allow_duplicate=True),
    Output('pie-charts-cancer-names', "value",allow_duplicate=True),
    Output('pie-charts-Gender-names', "options",allow_duplicate=True),
    Output('pie-charts-Gender-names', "value",allow_duplicate=True),
    Output('pie-charts-useful-names', "options",allow_duplicate=True),
    Output('pie-charts-useful-names', "value",allow_duplicate=True),
    Output('pie-charts-sym-names', "options",allow_duplicate=True),
    Input("interval", "n_intervals"),
    prevent_initial_call=True,
)
def input_tag(n):
    import dash_bootstrap_components as dbc
    data_for_dash_facebook = pd.read_csv('เชี่ยงใหม่\data_comment_pre_pa.csv', encoding='utf-8-sig')
    sym_o_th = data_for_dash_facebook.iloc[:, 12:]
    sym_o1_th = sym_o_th.melt()
    sym_o2_th = (pd.crosstab(sym_o1_th['variable'], sym_o1_th['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
    sym_o2_th = sym_o2_th[sym_o2_th['มีการเล่า']!=0]
    o_1=data_for_dash_facebook['defind_exp_with_python'].unique()
    v_1=data_for_dash_facebook['defind_exp_with_python'].unique()
    o_2=data_for_dash_facebook['defind_cancer_with_nlp'].unique()
    v_2=data_for_dash_facebook['defind_cancer_with_nlp'].unique()
    o_3 = data_for_dash_facebook['defind_Genden_with_python'].unique()
    v_3 = data_for_dash_facebook['defind_Genden_with_python'].unique()
    o_4 = ['อาจมีประโยชน์','ไม่มีประโยชน์']
    v_4 = ['อาจมีประโยชน์']
    o_5 = sym_o2_th['variable'].unique()
    return (o_1,v_1,o_2,v_2,o_3,v_3,o_4,v_4,o_5) #,

@callback(
    Output("pie-charts-exp-graph", "figure",allow_duplicate=True),
    Output('pie-charts-Gender-graph', "figure",allow_duplicate=True),
    Output("pie-charts-carcer-graph", "figure",allow_duplicate=True),
    Output("pie-charts-useful-graph", "figure",allow_duplicate=True),
    Output("his-charts-sym-graph", "figure",allow_duplicate=True),
    Output("line-charts-like-graph", "figure",allow_duplicate=True),
    Output("line-charts-rechat-graph", "figure",allow_duplicate=True),
    Output("line-charts-count_word-graph", "figure",allow_duplicate=True), 
    Output("text_sum_exp", 'children'),
    Output("text_sum_Gender", 'children'),
    Output("text_sum_cancer", 'children'),
    Output("text_sum_useful", 'children'), 
    Output("text_sum_sym", 'children'),
    Output("text_sum_like", 'children'),
    Output("text_sum_reply", 'children'),
    Output("text_sum_word", 'children'),
    Output('datatable', 'children',allow_duplicate=True),
    Output("text_sum_bybot", 'children'),
    Input("interval", "n_intervals"),
    Input("pie-charts-exp-names", "value"),
    Input('pie-charts-Gender-names', "value"),
    Input('pie-charts-cancer-names', "value"),
    Input('pie-charts-useful-names', "value"),
    Input("pie-charts-sym-names", "value"),
    Input("slider-count_word-names", "value"),
    Input("slider-count_like-names", "value"),
    Input("slider-count_rechat-names", "value"),
    Input('my-numeric-input-1', 'value'),
    Input('soft_table', 'value'),
    prevent_initial_call=True)

def generate_chart(n,exp,Gender,carcer,useful,sym,count_word,count_like,count_rechat,real_useFul,soft_table): #
    import dash_bootstrap_components as dbc
    data_for_dash_facebook = pd.read_csv('เชี่ยงใหม่\data_comment_pre_pa.csv', encoding='utf-8-sig')
    data_for_dash_facebook['count_plot'] = 1
    nms = data_for_dash_facebook
    if sym == [] or sym is None:
            nms = data_for_dash_facebook
    else:
        for defind_sym in range(len(sym)):
            x = nms[nms[sym[defind_sym]]==1]
            nms = x 
    real_useFul_1=[]
    for token in nms['จำนวนคำ']:
        if token >= real_useFul:
            real_useFul_1.append('อาจมีประโยชน์')
        else:
            real_useFul_1.append('ไม่มีประโยชน์')
    nms['use_ful'] = real_useFul_1
    nms = nms[nms['defind_exp_with_python'].isin(exp)]
    nms = nms[nms['defind_Genden_with_python'].isin(Gender)]
    nms = nms[nms['defind_cancer_with_nlp'].isin(carcer)]
    nms = nms[nms['use_ful'].isin(useful)]
    nms = nms[nms['ยอดไลค์']>=count_like]
    nms = nms[nms['จำนวนการตอบกลับ']>=count_rechat]
    nms = nms[nms['จำนวนคำ']>=count_word]
    sym_c = nms.iloc[:, 12:-1]
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
        # # return 'เล่าประสบการณ์คนอื่น'
        #     for keyword in  myself:
        #         if keyword in comment:
        #             return 'เล่าประสบการณ์ตัวเอง'
        #     # หากไม่พบคำที่บ่งบอกถึงคน
        #     return 'ไม่สามารถระบุได้'

    fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'],labels={'defind_exp_with_python':'ถูกเล่าจาก ','count_plot':'จำนวนความคิดเห็น '},color='defind_exp_with_python',color_discrete_map={'ไม่สามารถระบุได้':'lightcyan','เล่าประสบการณ์ตัวเอง':"royalblue",'เล่าประสบการณ์คนอื่น':'darkblue'}) #,color_discrete_sequence=px.colors.sequential.Teal
    fig_2 = px.pie(nms, values='count_plot', names=nms['defind_Genden_with_python'],labels={'defind_Genden_with_python':'เพศ ','count_plot':'จำนวนความคิดเห็น '},color_discrete_sequence=px.colors.sequential.Emrld)#,color='defind_Genden_with_python',color_discrete_map={'เพศชาย':'#4424D6','เพศหญิง':"#C21460",'ไม่ระบุเพศ':'#DAD4F7'}
    fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'],labels={'defind_cancer_with_nlp':'โรคที่พบ ','count':'จำนวนความคิดเห็น '},barmode='group',text_auto=True,color_discrete_sequence=['#7FBD32'])
    fig_4 = px.pie(nms, values='count_plot', names=nms['use_ful'],labels={'use_ful':'ความมีประโยชน์ ','count_plot':'จำนวนความคิดเห็น '},color='use_ful',color_discrete_map={'อาจมีประโยชน์':'#A33AF2','ไม่มีประโยชน์':"#EFDDFD"})
    fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True,color_discrete_sequence=['#496D1D'])
    fig_6 = px.line(nms,x='name', y='ยอดไลค์')
    fig_7 = px.line(nms,x='name', y='จำนวนการตอบกลับ')
    fig_8 = px.line(nms,x='name', y='จำนวนคำ')
    fig_1.update_layout(legend=dict( orientation="h"))
    fig_2.update_layout(legend=dict( orientation="h"))
    fig_3.update_layout(xaxis_title="โรคที่พบ",yaxis_title="จำนวนความคิดเห็น",plot_bgcolor="#D9EEBF")
    fig_4.update_layout(legend=dict( orientation="h"))
    fig_5.update_layout(xaxis_title="อาการที่พบ",yaxis_title="จำนวนความคิดเห็น",plot_bgcolor="#D9EEBF")
    fig_6.update_layout(xaxis_title="ชื่อผู้เเสดงความคิดเห็น",yaxis_title="ยอดไลค์",plot_bgcolor="#D9EEBF")
    fig_7.update_layout(xaxis_title="ชื่อผู้เเสดงความคิดเห็น",yaxis_title="จำนวนการตอบกลับ",plot_bgcolor="#D9EEBF")
    fig_8.update_layout(xaxis_title="ชื่อผู้เเสดงความคิดเห็น",yaxis_title="จำนวนคำ",plot_bgcolor="#D9EEBF")
    fig_6.update_traces(line_color='#213409', line_width=2)
    fig_7.update_traces(line_color='#213409', line_width=2)
    fig_8.update_traces(line_color='#213409', line_width=2)
    fig_1.update_layout(clickmode='event+select')
    fig_2.update_layout(clickmode='event+select')
    fig_3.update_layout(clickmode='event+select')
    fig_4.update_layout(clickmode='event+select')
    fig_5.update_layout(clickmode='event+select')
    # สรุปกราฟประสบการณ์
    sum_all_exp = nms['defind_exp_with_python']
    sum_non_exp = nms[nms['defind_exp_with_python'].isin(['ไม่สามารถระบุได้',"Didn't tell the experience"]) ]
    sum_other_exp = nms[nms['defind_exp_with_python'].isin(['เล่าประสบการณ์คนอื่น',"Tell other people's experiences"])]
    sum_self_exp = nms[nms['defind_exp_with_python'].isin(['เล่าประสบการณ์ตัวเอง','Tell about your own experiences'])] 
    value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
    value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
    value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
    text_1 = f'''ผลจากแผนภูมิ ประสบการณ์กับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุได้มีจำนวน {len(sum_non_exp)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
    { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
    if len(sum_other_exp) > len(sum_self_exp) else 
    f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
    #สรุปกราฟเพศ 
    sum_all_gen = nms['defind_Genden_with_python']
    sum_female_gen = nms[nms['defind_Genden_with_python'].isin(['เพศหญิง','Female'])]
    sum_male_gen = nms[nms['defind_Genden_with_python'].isin(['เพศชาย','Male'])]
    sum_non_gen = nms[nms['defind_Genden_with_python'].isin(['ไม่ระบุเพศ','Gender not specified'])]
    value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
    value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
    value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
    text_2 = f'''ผลจากแผนภูมิ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
    { f"เพศชายจำนวน {len(sum_male_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} ในขณะที่อีก {len(sum_female_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
        if len(sum_male_gen) > len(sum_female_gen) else 
        f"เพศหญิงจำนวน {len(sum_female_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} ในขณะที่อีก {len(sum_male_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
    # สรุปกราฟโรค
    nms_can = nms[['defind_cancer_with_nlp','count_plot']]
    nms_gro_cancer = nms_can.groupby('defind_cancer_with_nlp').sum().reset_index().sort_values(by='count_plot',ascending=False)
    text_3 ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
    for fill in range(len(nms_gro_cancer)):
        p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
        text_3 = text_3 + f'- {nms_gro_cancer["defind_cancer_with_nlp"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}\n'
    # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
    sum_all_useful = nms['use_ful']
    sum_have_useful = nms[nms['use_ful'].isin(['อาจมีประโยชน์','maybe_useful'])]
    sum_not_useful = nms[nms['use_ful'].isin(['ไม่มีประโยชน์','Not useful or not giving too much information'])]
    value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
    value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
    text_4= f'''ผลจากแผนภูมิ ความมีประโยชน์กับความคิดเห็น พบว่า ส่วนมากเป็นความคิดเห็นที่
    {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)} ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ในขณะที่อีก {len(sum_not_useful)} ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
        if len(sum_have_useful) > len(sum_not_useful) else 
        f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)} ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ในขณะที่อีก {len(sum_have_useful)} ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
    #อาการ
    text_5 ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
    for filler in range(len(plot_sym)):
        plot_sym_next = plot_sym.reset_index()
        text_5 = text_5 + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
    # like reply จำนวนคำ
    avg_11=nms['ยอดไลค์'].mean()
    avg_22=nms['จำนวนการตอบกลับ'].mean()
    avg_33=nms['จำนวนคำ'].mean()
    text_6 = f'''จากแผนภูมิจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุด คือ {nms['ยอดไลค์'].max()}
                ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุด คือ {nms['ยอดไลค์'].min()}
                ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุด คือ {round(avg_11,2)}'''
    text_7= f'''จากแผนภูมิจะพบว่า จำนวนการตอบกลับในหัวข้อนี้มีค่ามากที่สุด คือ {nms['จำนวนการตอบกลับ'].max()}
                จำนวนการตอบกลับในหัวข้อนี้มีค่าน้อยที่สุด คือ {nms['จำนวนการตอบกลับ'].min()}
                จำนวนการตอบกลับในหัวข้อนี้มีค่าเฉลี่ยที่สุด คือ {round(avg_22,2)}'''
    text_8= f'''จากแผนภูมิจะพบว่า จำนวนคำในหัวข้อนี้มีค่ามากที่สุด คือ {nms['จำนวนคำ'].max()}
                จำนวนคำในหัวข้อนี้มีค่าน้อยที่สุด คือ {nms['จำนวนคำ'].min()}
                จำนวนคำในหัวข้อนี้มีค่าเฉลี่ยที่สุด คือ {round(avg_33,2)}'''
    if soft_table == 'มากไปน้อย':
        nms = nms.sort_values(by='จำนวนคำ',ascending=False)
        if nms['ยอดไลค์'].sum() > 1:
            data130 = nms.iloc[:,:4]
        else :
            data130 = nms.iloc[:,:2]
    else:
        nms = nms.sort_values(by='จำนวนคำ',ascending=True)
        if nms['ยอดไลค์'].sum() > 1:
            data130 = nms.iloc[:,:4]
        else :
            data130 = nms.iloc[:,:2]
    data_for_export = dash_table.DataTable(data130.to_dict('records'), [{"name": i, "id": i} for i in data130.columns],style_cell={'textAlign': 'left'},style_header={'backgroundColor': '#04AA6D','color': 'white'},export_format="csv")
    with open('bot_summarize_comment.txt', 'r',encoding='utf-8-sig') as file:
        look_orgin = file.read()
        look = look_orgin.replace('*', '')
    return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8,text_1,text_2,text_3,text_4,text_5,text_6,text_7,text_8,data_for_export,look]#

app.clientside_callback(
            """
            function () {            

                var printContents = document.getElementById('grid-print-area').innerHTML;
                var originalContents = document.body.innerHTML;

                document.body.innerHTML = printContents;

                window.print();

                document.body.innerHTML = originalContents;      
                location.reload()                              

                return window.dash_clientside.no_update
            }
            """,
            Output("dummy", "children"),
            Input("grid-browser-print-btn", "n_clicks"),
            prevent_initial_call=True,
        )

if __name__ == '__main__':
    app.run(debug=True)