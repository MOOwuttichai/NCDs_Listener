from dash import Dash, html, Input, Output, callback,dcc,dash_table,no_update
import pandas as pd
import plotly.express as px
import os
import dash_bootstrap_components as dbc
import dash_daq as daq
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_anthropic import ChatAnthropic #v 0.1.15
#v0.2
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyMuPDFLoader, PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.indexes import VectorstoreIndexCreator

from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chains.llm import LLMChain
app = Dash(__name__)
data_for_dash_facebook = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
app.layout = html.Div([
        dcc.Interval( id="interval",interval= 10*1000,n_intervals=0,),
            html.Div([
                html.Div(id='datatable',style={'height': '300px','overflowY': 'auto'}),
                    ]),
        html.Div(
            [
        dbc.Button("Print", id="grid-browser-print-btn",style={'height': '300px','overflowY': 'auto'}),
        dbc.ModalBody(
            # customize your printed report here
            [
        # ประสบการณ์ของใคร
        html.Div([
                html.P("แผนภูมิประสบการณ์กับจำนวนความคิดเห็น"),
                dcc.Graph(id="pie-charts-exp-graph"),
                html.P(id = 'text_sum_exp')],style={'width': '40%',  'display': 'inline-block'}),
        html.Div([
            html.P("ประสบการณ์:"),
            dcc.Checklist(id='pie-charts-exp-names')
            ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
        # Gender
        html.Div([
            html.P("แผนภูมิเพศผู้ป่วยกับจำนวนความคิดเห็น"),
            dcc.Graph(id="pie-charts-Gender-graph"),
            html.P(id = 'text_sum_Gender')],style={'width': '40%',  'display': 'inline-block'}),
        html.Div([
            html.P("เพศ:"),
            dcc.Checklist(id='pie-charts-Gender-names')
            ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
            html.Br(style={"line-height": "5"}),
        # โรค
        html.Div([
            html.P("โรค:"),
            dcc.Dropdown(id='pie-charts-cancer-names',multi=True)
            ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
        html.Div([
            html.P("แผนภูมิโรคกับจำนวนความคิดเห็น"),
            dcc.Graph(id="pie-charts-carcer-graph"),
            html.P(id = 'text_sum_cancer',style={'whiteSpace': 'pre-line'})],style={'width': '50%', 'display': 'inline-block'}),
        # useful
        html.Div([
            html.P("แผนภูมิความมีประโยชน์กับจำนวนความคิดเห็น"),
            dcc.Graph(id="pie-charts-useful-graph"),
            html.P(id ="text_sum_useful")],style={'width': '40%',  'display': 'inline-block'}),
        html.Div([
                html.P("ความมีประโยชน์:"),
                dcc.Checklist(id="pie-charts-useful-names"),
                html.Br(style={"line-height": "5"}),
                html.P("จำนวนคำ 'ขั้นต่ำ' ที่มีประโยชน์:"),
                dcc.Input(id='my-numeric-input-1',type= "number",placeholder="จำนวนคำ 'ขั้นต่ำ' ที่มีประโยชน์",value = 5)
                ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                html.Br(style={"line-height": "5"}),
        # sym
        html.Div([
            html.P("อาการ:"),
            dcc.Dropdown(id='pie-charts-sym-names',multi=True)
            ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
        html.Div([
            html.P("แผนภูมิอาการกับจำนวนความคิดเห็น"),
            dcc.Graph(id="his-charts-sym-graph"),
            html.P(id ="text_sum_sym",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
            html.Br(style={"line-height": "5"}),
            html.Br(style={"line-height": "5"}),
        # word count
        html.Div([
            html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
            dcc.Slider(0,200,200/5,value=0,
                tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_word-names'),
            ],style={'width': '20%', 'display': 'inline-block',"float":"left"}),
        html.Div([
            html.P("แผนภูมิจำนวนคำกับชื่อผู้ที่มาเเสดงความคิดเห็น"),
            dcc.Graph(id="line-charts-count_word-graph"),
            html.P(id ="text_sum_word",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
            html.Br(style={"line-height": "5"}),
            html.Br(style={"line-height": "5"}),
        # like
         html.Div([
            html.P("จำนวน like(ขั้นต่ำ):"),
            dcc.Slider(0, 500, 500/5,
                value=0,tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_like-names'),
            ],style={'width': '20%', 'display': 'inline-block',"float":"left"}),
            html.Br(style={"line-height": "5"}),
            html.Br(style={"line-height": "5"}),
        html.Div([
            html.P("แผนภูมิจำนวนยอดไลน์กับชื่อผู้ที่มาเเสดงความคิดเห็น"),
            dcc.Graph(id="line-charts-like-graph"),
            html.P(id ="text_sum_like",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
            html.Br(style={"line-height": "5"}),
            html.Br(style={"line-height": "5"}),
        # reply count
        html.Div([
            html.P("จำนวนการตอบกลับ(ขั้นต่ำ):"),
            dcc.Slider(0, 100, 100/5,
                value=0,tooltip={"placement": "bottom", "always_visible": True},
                id='slider-count_rechat-names'),
            ],style={'width': '20%', 'display': 'inline-block',"float":"left"}),
        html.Div([
            html.P("แผนภูมิจำนวนการตอบกลับกับชื่อผู้ที่มาเเสดงความคิดเห็น"),
            dcc.Graph(id="line-charts-rechat-graph"),
            html.P(id ="text_sum_reply",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
            html.P('สรุปความคิดเห็นโดย gimini'),
            html.P(id ="text_sum_bybot",style={'whiteSpace': 'pre-line'})
            ],
                id="grid-print-area",
                ),
                html.Div(id="dummy"),
                ])
                
            ])
    
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
    prevent_initial_call=True)

def generate_chart(n,exp,Gender,carcer,useful,sym,count_word,count_like,count_rechat,real_useFul):
    import dash_bootstrap_components as dbc
    data_for_dash_facebook = pd.read_csv('data_for_dash_01.csv', encoding='utf-8-sig')
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
    fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'],color_discrete_sequence=px.colors.sequential.Emrld)
    fig_2 = px.pie(nms, values='count_plot', names=nms['defind_Genden_with_python'],color='defind_Genden_with_python',color_discrete_map={'เพศชาย':'darkblue','เพศหญิง':"magenta",'ไม่ระบุเพศ':'gray','Male':'darkblue','Female':"magenta",'Gender not specified':'gray'})
    fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'], y='count_plot',barmode='group',text_auto=True)
    fig_4 = px.pie(nms, values='count_plot', names=nms['use_ful'],color_discrete_sequence=px.colors.sequential.Aggrnyl)
    fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True)
    fig_6 = px.line(nms,x='name', y='ยอดไลค์')
    fig_7 = px.line(nms,x='name', y='จำนวนการตอบกลับ')
    fig_8 = px.line(nms,x='name', y='จำนวนคำ')
    # สรุปกราฟประสบการณ์
    sum_all_exp = nms['defind_exp_with_python']
    sum_non_exp = nms[nms['defind_exp_with_python'].isin(['ไม่ได้เล่าประสบการณ์',"Didn't tell the experience"]) ]
    sum_other_exp = nms[nms['defind_exp_with_python'].isin(['เล่าประสบการณ์คนอื่น',"Tell other people's experiences"])]
    sum_self_exp = nms[nms['defind_exp_with_python'].isin(['เล่าประสบการณ์ตัวเอง','Tell about your own experiences'])] 
    value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
    value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
    value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
    text_1 = f'''ผลจากแผนภูมิ ประสบการณ์กับความคิดเห็น พบว่าความคิดเห็นที่ไม่ได้เล่าประสบการณ์เกี่ยวกับโรคมีจำนวน {len(sum_non_exp)}ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
    { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก{len(sum_self_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
    if len(sum_other_exp) > len(sum_self_exp) else 
    f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
    #สรุปกราฟเพศ 
    sum_all_gen = nms['defind_Genden_with_python']
    sum_female_gen = nms[nms['defind_Genden_with_python'].isin(['เพศหญิง','Female'])]
    sum_male_gen = nms[nms['defind_Genden_with_python'].isin(['เพศชาย','Male'])]
    sum_non_gen = nms[nms['defind_Genden_with_python'].isin(['ไม่ระบุเพศ','Gender not specified'])]
    value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
    value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
    value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
    text_2 = f'''ผลจากแผนภูมิ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
    { f"เพศชายจำนวน {len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_male_p_gen,2)} ในขณะที่อีก{len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
        if len(sum_male_gen) > len(sum_female_gen) else 
        f"เพศหญิงจำนวน {len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_female_p_gen,2)} ในขณะที่อีก{len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
    # สรุปกราฟโรค
    nms_can = nms[['defind_cancer_with_nlp','count_plot']]
    nms_gro_cancer = nms_can.groupby('defind_cancer_with_nlp').sum().reset_index().sort_values(by='count_plot',ascending=False)
    text_3 ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
    for fill in range(len(nms_gro_cancer)):
        p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
        text_3 = text_3 + f'\n- {nms_gro_cancer["defind_cancer_with_nlp"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}'
    # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
    sum_all_useful = nms['use_ful']
    sum_have_useful = nms[nms['use_ful'].isin(['อาจมีประโยชน์','maybe_useful'])]
    sum_not_useful = nms[nms['use_ful'].isin(['ไม่มีประโยชน์','Not useful or not giving too much information'])]
    value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
    value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
    text_4= f'''ผลจากแผนภูมิ ความมีประโยชน์กับความคิดเห็น พบว่าส่วนมากเป็นความคิดเห็นที่
    {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_have_useful_p,2)} ในขณะที่อีก{len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
        if len(sum_have_useful) > len(sum_not_useful) else 
        f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_not_useful_p,2)} ในขณะที่อีก{len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
    #อาการ
    text_5 ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
    for filler in range(len(plot_sym)):
        plot_sym_next = plot_sym.reset_index()
        text_5 = text_5 + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
    # like reply จำนวนคำ
    avg_11=nms['ยอดไลค์'].mean()
    avg_22=nms['จำนวนการตอบกลับ'].mean()
    avg_33=nms['จำนวนคำ'].mean()
    text_6 = f'''จากแผนภูมิจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['ยอดไลค์'].max()}\n
                ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ {nms['ยอดไลค์'].min()}\n
                ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ {round(avg_11,2)}\n'''
    text_7= f'''จากแผนภูมิจะพบว่า จำนวนการตอบกลับในหัวข้อนี้มีค่ามากที่สุดคือ {nms['จำนวนการตอบกลับ'].max()}\n
                จำนวนการตอบกลับในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['จำนวนการตอบกลับ'].min()}\n
                จำนวนการตอบกลับในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_22,2)}\n'''
    text_8= f'''จากแผนภูมิจะพบว่า จำนวนคำในหัวข้อนี้มีค่ามากที่สุดคือ {nms['จำนวนคำ'].max()}\n
                จำนวนคำในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['จำนวนคำ'].min()}\n
                จำนวนคำในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_33,2)}\n'''
    if nms['ยอดไลค์'].sum() > 1:
        data130 = nms.iloc[:,:4]
    else :
        data130 = nms.iloc[:,:2]
    data_for_export = dash_table.DataTable(data130.to_dict('records'), [{"name": i, "id": i} for i in data130.columns],style_cell={'textAlign': 'left'},sort_action="native",
        sort_mode="multi",export_format="csv")
    with open('bot_summarize_comment.txt', 'r',encoding='utf-8-sig') as file:
        look = file.read()
    return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8,text_1,text_2,text_3,text_4,text_5,text_6,text_7,text_8,data_for_export,look]

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
    Input('my-numeric-input-1', 'value'),
    prevent_initial_call=True,
)
def input_tag(n,real_useFul):
    import dash_bootstrap_components as dbc
    data_for_dash_facebook = pd.read_csv('data_for_dash_01.csv', encoding='utf-8-sig')
    sym_o_th = data_for_dash_facebook.iloc[:, 12:]
    sym_o1_th = sym_o_th.melt()
    sym_o2_th = (pd.crosstab(sym_o1_th['variable'], sym_o1_th['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
    o_1=data_for_dash_facebook['defind_exp_with_python'].unique()
    v_1=data_for_dash_facebook['defind_exp_with_python'].unique()
    o_2=data_for_dash_facebook['defind_cancer_with_nlp'].unique()
    v_2=data_for_dash_facebook['defind_cancer_with_nlp'].unique()
    o_3 = data_for_dash_facebook['defind_Genden_with_python'].unique()
    v_3 = data_for_dash_facebook['defind_Genden_with_python'].unique()
    o_4 = ['อาจมีประโยชน์','ไม่มีประโยชน์']
    v_4 = ['อาจมีประโยชน์','ไม่มีประโยชน์']
    o_5 = sym_o2_th['variable'].unique()
    return(o_1,v_1,o_2,v_2,o_3,v_3,o_4,v_4,o_5)

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

# @callback(
#     Output("pie-charts-exp-graph", "figure"),
#     Output("pie-charts-carcer-graph", "figure"),
#     Output('datatable', 'children'),  
#     Input("pie-charts-exp-graph", 'clickData'),
#     )
# def generate_chart(exp):
#             import dash_bootstrap_components as dbc
#             try:
#                 data_for_dash_facebook = pd.read_csv('data_pre_setting.csv', encoding='utf-8-sig')
#                 data_for_dash_facebook.drop('sum_ch', axis=1, inplace=True)
#             except:
#                 data_for_dash_facebook = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
#             label = str(exp['points'][0]['label'])
#             data_for_dash_facebook['count_plot'] = 1
#             nms = data_for_dash_facebook
#             nms = nms[nms['defind_exp_with_python']== label]
#             fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'],color_discrete_sequence=px.colors.sequential.Emrld)
#             fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'], y='count_plot',barmode='group',text_auto=True)
#             fig_1.update_layout(clickmode='event+select')
#             fig_3.update_layout(clickmode='event+select')
#             data130 = nms.iloc[:,:5]
#             data_for_export = dash_table.DataTable(data130.to_dict('records'), [{"name": i, "id": i} for i in data130.columns],export_format="csv")
#             return [fig_1,fig_3,data_for_export]
   



# sorue_sym_4 = pd.read_csv('soure_url.csv')
# soure = sorue_sym_4['url'][0]
# if soure == 'www.facebook.com':
#     import dash_bootstrap_components as dbc
#     data_for_dash_facebook = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
#     data_for_dash_facebook['count_plot'] = 1
#     sym_o_th = data_for_dash_facebook.iloc[:, 13:-1]
#     sym_o1_th = sym_o_th.melt()
#     sym_o2_th = (pd.crosstab(sym_o1_th['variable'], sym_o1_th['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()

#     app.layout = html.Div([
#         dcc.Interval( id="interval",interval=1*1000,n_intervals=0,),
#         html.Div([
#             html.Div(id='datatable',style={'height': '300px','overflowY': 'auto'}),
#                 ]),
#     html.Div(
#         [
#         dbc.ModalHeader(dbc.Button("Print", id="grid-browser-print-btn")),
#         dbc.ModalBody(
#             # customize your printed report here
#             [
#             # exp
#             html.Div([
#                 html.P("แผนภูมิประสบการณ์กับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="pie-charts-exp-graph"),
#                 html.P(id = 'text_sum_exp')],style={'width': '40%',  'display': 'inline-block'}),
#             html.Div([
#                 html.P("ประสบการณ์:"),
#                 dcc.Checklist(id='pie-charts-exp-names',
#                     options=data_for_dash_facebook['ใครเล่า'].unique(),
#                     value=data_for_dash_facebook['ใครเล่า'].unique()),
#                 ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#             # Gender
#             html.Div([
#                 html.P("แผนภูมิเพศผู้ป่วยกับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="pie-charts-Gender-graph"),
#                 html.P(id = 'text_sum_Gender')],style={'width': '40%',  'display': 'inline-block'}),
#             html.Div([
#                 html.P("เพศ:"),
#                 dcc.Checklist(id='pie-charts-Gender-names',
#                     options=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique(),
#                     value=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique()),
#                     ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#                 html.Br(style={"line-height": "5"}),
#             # carcer
#             html.Div([
#                 html.P("โรค:"),
#                 dcc.Dropdown(id='pie-charts-cancer-names',
#                     options=data_for_dash_facebook['โรค'].unique(),
#                     value=data_for_dash_facebook['โรค'].unique(),multi=True),
#                 ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#             html.Div([
#                 html.P("แผนภูมิโรคกับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="his-charts-carcer-graph"),
#                 html.P(id = 'text_sum_cancer',style={'whiteSpace': 'pre-line'})],style={'width': '50%', 'display': 'inline-block'}),
#             # useful
#             html.Div([
#                 html.P("แผนภูมิความมีประโยชน์กับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="pie-charts-useful-graph"),
#                 html.P(id ="text_sum_useful")],style={'width': '40%',  'display': 'inline-block'}),
#             html.Div([
#                 html.P("ความมีประโยชน์:"),
#                 dcc.Checklist(id="pie-charts-useful-names",
#                     options=data_for_dash_facebook['ความมีประโยชน์'].unique(),
#                     value=data_for_dash_facebook['ความมีประโยชน์'].unique()),
#                 ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#                 html.Br(style={"line-height": "5"}),
#             # sym
#             html.Div([
#                 html.P("อาการ:"),
#                 dcc.Dropdown(id='pie-charts-sym-names',
#                     options=sym_o2_th['variable'].unique(),
#                     multi=True)],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#             html.Div([
#                 html.P("แผนภูมิอาการกับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="his-charts-sym-graph"),
#                 html.P(id ="text_sum_sym",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
#             # like
#             html.Div([
#                 html.P("แผนภูมิจำนวนยอดไลน์กับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="line-charts-like-graph"),
#                 html.P(id ="text_sum_like",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
#             html.Div([
#                 html.P("จำนวน like(ขั้นต่ำ):"),
#                 dcc.Slider(0, max(data_for_dash_facebook['ยอดไลค์'].tolist()), max(data_for_dash_facebook['ยอดไลค์'].tolist())/5,
#                     value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
#                     id='slider-count_like-names'),
#                 ],style={'width': '20%', 'display': 'inline-block',"height": "300px","float":"left"}),
#             # reply count
#             html.Div([
#                 html.P("แผนภูมิจำนวนการตอบกลับกับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="line-charts-rechat-graph"),
#                 html.P(id ="text_sum_reply",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
#             html.Div([
#                 html.P("จำนวนการตอบกลับ(ขั้นต่ำ):"),
#                 dcc.Slider(0, max(data_for_dash_facebook['จำนวนการตอบกลับ'].tolist()), max(data_for_dash_facebook['จำนวนการตอบกลับ'].tolist())/5,
#                     value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
#                     id='slider-count_rechat-names'),
#                 ],style={'width': '20%', 'display': 'inline-block',"height": "300px","float":"left"}),
#             # word count
#             html.Div([
#                 html.P("แผนภูมิจำนวนตัวอักษรกับจำนวนความคิดเห็น"),
#                 dcc.Graph(id="line-charts-count_word-graph"),
#                 html.P(id ="text_sum_word",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
#             html.Div([
#                 html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
#                 dcc.Slider(0, max(data_for_dash_facebook['จำนวนตัวอักษร'].tolist()), max(data_for_dash_facebook['จำนวนตัวอักษร'].tolist())/5,
#                     value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
#                     id='slider-count_word-names'),
#                 ],style={'width': '20%', 'display': 'inline-block',"height": "100px","float":"left"}),
#             ],
#             id="grid-print-area",
#             ),
#             html.Div(id="dummy"),
#             ])
#             ])
#     @callback(
#         Output("pie-charts-exp-graph", "figure"),
#         Output("pie-charts-Gender-graph", "figure"),
#         Output("his-charts-carcer-graph", "figure"), 
#         Output("pie-charts-useful-graph", "figure"),
#         Output("his-charts-sym-graph", "figure"),
#         Output("line-charts-like-graph", "figure"),
#         Output("line-charts-rechat-graph", "figure"),
#         Output("line-charts-count_word-graph", "figure"),
#         Output("text_sum_exp", 'children'),
#         Output("text_sum_Gender", 'children'),
#         Output("text_sum_cancer", 'children'),
#         Output("text_sum_useful", 'children'), 
#         Output("text_sum_sym", 'children'),
#         Output("text_sum_like", 'children'),
#         Output("text_sum_reply", 'children'),
#         Output("text_sum_word", 'children'),
#         Output('datatable', 'children'),
#         Input("pie-charts-exp-names", "value"),
#         Input("pie-charts-Gender-names", "value"),
#         Input("pie-charts-cancer-names", "value"),
#         Input("pie-charts-useful-names", "value"),
#         Input("pie-charts-sym-names", "value"),
#         Input("slider-count_like-names", "value"),
#         Input("slider-count_rechat-names", "value"),
#         Input("slider-count_word-names", "value"),
#         Input("interval", "n_intervals"),
#         prevent_initial_call=True,
#         )
#     def generate_chart(exp,Gender,carcer,useful,sym,count_like,count_rechat,count_word,n):
#         nms = data_for_dash_facebook
#         if sym == [] or sym is None:
#             nms = data_for_dash_facebook
#         else:
#             for defind_sym in range(len(sym)):
#                 x = nms[nms[sym[defind_sym]]==1]
#                 nms = x 
#         nms = nms[nms['ใครเล่า'].isin(exp)]
#         nms = nms[nms['เพศเเบ่งโดยใช้_python'].isin(Gender)]
#         nms = nms[nms['โรค'].isin(carcer)]
#         nms = nms[nms['ความมีประโยชน์'].isin(useful)]
#         nms = nms[nms['ยอดไลค์']>=count_like]
#         nms = nms[nms['จำนวนการตอบกลับ']>=count_rechat]
#         nms = nms[nms['จำนวนตัวอักษร']>=count_word]
#         sym_c = nms.iloc[:, 13:-1]
#         sym_ca = sym_c.melt()
#         sym_can = (pd.crosstab(sym_ca['variable'], sym_ca['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'}))
#         plot_data=sym_can['มีการเล่า'].reset_index()
#         if sym == [] or sym is None :
#             plot_data_None = plot_data
#             plot_sym=plot_data_None[plot_data_None['มีการเล่า'] != 0]
#         elif len(sym) == 1:
#             plot_data_None = plot_data
#             plot_sym=plot_data_None[plot_data_None['มีการเล่า'] != 0]
#         else:
#             x_value=plot_data[plot_data['variable'].isin(sym)]['มีการเล่า'].to_list()
#             x_name=plot_data[plot_data['variable'].isin(sym)]['variable'].to_list()
#             sum_name =""
#             for sum_name_count in x_name:
#                 if sum_name == "":
#                     sum_name = sum_name+sum_name_count
#                 else:
#                     sum_name = sum_name+"&"+sum_name_count
#             x_plot_1 = pd.DataFrame(data={'variable': sum_name, 'มีการเล่า': x_value})
#             plot_data_non=plot_data[plot_data.variable.isin(sym) == False]
#             plot_data_nonnone=pd.concat([plot_data_non,x_plot_1])
#             plot_sym=plot_data_nonnone.drop_duplicates()
#             plot_sym = plot_sym[plot_sym['มีการเล่า']!=0]
#         fig_1 = px.pie(nms, values='count_plot', names=nms['ใครเล่า'],color_discrete_sequence=px.colors.sequential.Emrld)
#         fig_2 = px.pie(nms, values='count_plot', names=nms['เพศเเบ่งโดยใช้_python'],color='เพศเเบ่งโดยใช้_python',color_discrete_map={'เพศชาย':'darkblue','เพศหญิง':"magenta",'ไม่ระบุเพศ':'gray'})
#         fig_3 = px.histogram(nms, x=nms['โรค'], y='count_plot',barmode='group',text_auto=True)
#         fig_4 = px.pie(nms, values='count_plot', names=nms['ความมีประโยชน์'],color_discrete_sequence=px.colors.sequential.Aggrnyl)
#         fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True)
#         fig_6 = px.line(nms,x='ชื่อ', y='ยอดไลค์')
#         fig_7 = px.line(nms,x='ชื่อ', y='จำนวนการตอบกลับ')
#         fig_8 = px.line(nms,x='ชื่อ', y='จำนวนตัวอักษร')
#         #สรุปกราฟประสบการณ์
#         sum_all_exp = nms['ใครเล่า']
#         sum_non_exp = nms[nms['ใครเล่า']=='ไม่ได้เล่าประสบการณ์']
#         sum_other_exp = nms[nms['ใครเล่า']=='เล่าประสบการณ์คนอื่น']
#         sum_self_exp = nms[nms['ใครเล่า']=='เล่าประสบการณ์ตัวเอง']
#         value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
#         value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
#         value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
#         text_1 = f'''ผลจากกราฟ ประสบการณ์กับความคิดเห็น พบว่าความคิดเห็นที่ไม่ได้เล่าประสบการณ์เกี่ยวกับโรคมีจำนวน {len(sum_non_exp)}ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
#         { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก{len(sum_self_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
#          if len(sum_other_exp) > len(sum_self_exp) else 
#          f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
#         #สรุปกราฟเพศ 
#         sum_all_gen = nms['เพศเเบ่งโดยใช้_python']
#         sum_female_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='เพศหญิง']
#         sum_male_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='เพศชาย']
#         sum_non_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='ไม่ระบุเพศ']
#         value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
#         value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
#         value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
#         text_2 = f'''ผลจากกราฟ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
#         { f"เพศชายจำนวน {len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_male_p_gen,2)} ในขณะที่อีก{len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
#          if len(sum_male_gen) > len(sum_female_gen) else 
#          f"เพศหญิงจำนวน {len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_female_p_gen,2)} ในขณะที่อีก{len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
#         # สรุปกราฟโรค
#         nms_can = nms[['โรค','count_plot']]
#         nms_gro_cancer = nms_can.groupby('โรค').sum().reset_index().sort_values(by='count_plot',ascending=False)
#         text_3 ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
#         for fill in range(len(nms_gro_cancer)):
#             p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
#             text_3 = text_3 + f'\n- {nms_gro_cancer["โรค"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}'
#         # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
#         sum_all_useful = nms['ความมีประโยชน์']
#         sum_have_useful = nms[nms['ความมีประโยชน์']=='อาจมีประโยชน์']
#         sum_not_useful = nms[nms['ความมีประโยชน์']=='ไม่มีประโยชน์']
#         value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
#         value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
#         text_4= f'''ผลจากกราฟ ความมีประโยชน์กับความคิดเห็น พบว่าส่วนมากเป็นความคิดเห็นที่
#         {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_have_useful_p,2)} ในขณะที่อีก{len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
#          if len(sum_have_useful) > len(sum_not_useful) else 
#          f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_not_useful_p,2)} ในขณะที่อีก{len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
#         #อาการ
#         text_5 ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
#         for filler in range(len(plot_sym)):
#             plot_sym_next = plot_sym.reset_index()
#             text_5 = text_5 + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
#         # like reply จำนวนตัวอักษร
#         avg_11=nms['ยอดไลค์'].mean()
#         avg_22=nms['จำนวนการตอบกลับ'].mean()
#         avg_33=nms['จำนวนตัวอักษร'].mean()
#         text_6 = f'''จากกราฟจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['ยอดไลค์'].max()}\n
#                     ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ {nms['ยอดไลค์'].min()}\n
#                     ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ {round(avg_11,2)}\n'''
#         text_7= f'''จากกราฟจะพบว่า จำนวนการตอบกลับในหัวข้อนี้มีค่ามากที่สุดคือ {nms['จำนวนการตอบกลับ'].max()}\n
#                     จำนวนการตอบกลับในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['จำนวนการตอบกลับ'].min()}\n
#                     จำนวนการตอบกลับในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_22,2)}\n'''
#         text_8= f'''จากกราฟจะพบว่า จำนวนตัวอักษรในหัวข้อนี้มีค่ามากที่สุดคือ {nms['จำนวนตัวอักษร'].max()}\n
#                     จำนวนตัวอักษรในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['จำนวนตัวอักษร'].min()}\n
#                     จำนวนตัวอักษรในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_33,2)}\n'''
#         data130 = nms.iloc[:,:5]
#         data_for_export = dash_table.DataTable(columns=[{"name": i, "id": i} for i in data130.columns],data=data130.to_dict('records'),export_format="csv")
#         return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8,text_1,text_2,text_3,text_4,text_5,text_6,text_7,text_8,data_for_export]
#     app.clientside_callback(
#                     """
#                     function () {            

#                         var printContents = document.getElementById('grid-print-area').innerHTML;
#                         var originalContents = document.body.innerHTML;

#                         document.body.innerHTML = printContents;

#                         window.print();

#                         document.body.innerHTML = originalContents;      
#                         location.reload()                              

#                         return window.dash_clientside.no_update
#                     }
#                     """,
#                     Output("dummy", "children"),
#                     Input("grid-browser-print-btn", "n_clicks"),
#                     prevent_initial_call=True,
#                 )
# elif soure == 'www.reddit.com':
#     import dash_bootstrap_components as dbc
#     data_for_dash_raddit = pd.read_csv('data_pre.csv')
#     data_for_dash_raddit['count_plot'] = 1
#     sym_o = data_for_dash_raddit.iloc[:, 10:-1]
#     sym_o1 = sym_o.melt()
#     sym_o2 = (pd.crosstab(sym_o1['variable'], sym_o1['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
#     now = data_for_dash_raddit.iloc[:,:4]
#     app.layout = html.Div([
#         html.Div([
#         html.Div(id='datatable',style={'height': '300px','overflowY': 'auto'}),
#         ]),
#     html.Div(
#         [
#     dbc.ModalHeader(dbc.Button("Print", id="grid-browser-print-btn")),
#     dbc.ModalBody(
#     # customize your printed report here
#     [
#     # exp
#     html.Div([
#         html.P("แผนภูมิประสบการณ์กับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-exp-graph"),
#         html.P(id = 'text_sum_exp')],style={'width': '40%',  'display': 'inline-block'}),
#     html.Div([
#             html.P("ประสบการณ์"),
#             # exp
#             dcc.Checklist(id='pie-charts-exp-names',
#                 options=data_for_dash_raddit['defind_exp_with_python'].unique(),
#                 value=data_for_dash_raddit['defind_exp_with_python'].unique()),
#             ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#     # Gender
#     html.Div([
#         html.P("แผนภูมิเพศผู้ป่วยกับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-Gender-graph"),
#         html.P(id = 'text_sum_Gender')],style={'width': '40%',  'display': 'inline-block'}),
#     html.Div([
#             html.P("เพศ"),
#             dcc.Checklist(id='pie-charts-Gender-names',
#                 options=data_for_dash_raddit['defind_Genden_with_python'].unique(),
#                 value=data_for_dash_raddit['defind_Genden_with_python'].unique()),
#             ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#             html.Br(style={"line-height": "5"}),
#     # carcer
#     html.Div([
#             html.P("โรค:"),
#             dcc.Dropdown(id='pie-charts-cancer-names',
#                 options=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),
#                 value=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),multi=True),
#             ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#     html.Div([
#         html.P("แผนภูมิโรคกับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-carcer-graph"),
#         html.P(id = 'text_sum_cancer',style={'whiteSpace': 'pre-line'})],style={'width': '50%', 'display': 'inline-block'}),
#     # useful
#     html.Div([
#         html.P("แผนภูมิความมีประโยชน์กับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-useful-graph"),
#         html.P(id ="text_sum_useful")],style={'width': '40%',  'display': 'inline-block'}),
#     html.Div([
#             html.P("ความมีประโยชน์:"),
#             dcc.Checklist(id="pie-charts-useful-names",
#                 options=data_for_dash_raddit['use_ful'].unique(),
#                 value=data_for_dash_raddit['use_ful'].unique()),
#             ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#             html.Br(style={"line-height": "5"}),
#     # sym
#     html.Div([
#             html.P("อาการ:"),
#             dcc.Dropdown(id='pie-charts-sym-names',
#                 options=sym_o2['variable'].unique(),
#                 multi=True),
#             ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
#     html.Div([
#         html.P("แผนภูมิอาการกับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-sym-graph"),
#         html.P(id ="text_sum_sym",style={'whiteSpace': 'pre-line'})],style={'width': '29%','display': 'inline-block'}),
#     # word count
#     html.Div([
#         html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
#         dcc.Slider(0, 1000, 1000/5,
#         value=100,tooltip={"placement": "bottom", "always_visible": True},
#         id='slider-count_word-names'),
#         ],style={'width': '49%', 'display': 'inline-block',"float":"left"}),
#     html.Div([
#         html.P("แผนภูมิจำนวนตัวอักษรกับจำนวนความคิดเห็น"),
#         dcc.Graph(id="pie-charts-count_word-graph"),
#         html.P(id ="text_sum_word",style={'whiteSpace': 'pre-line'})],style={'width': '70%','display': 'inline-block'}),
#         ],
#         id="grid-print-area",
#         ),
#         html.Div(id="dummy"),
#         ])
#         ])
#     @app.callback(
#         Output("pie-charts-exp-graph", "figure"),
#         Output("pie-charts-Gender-graph", "figure"),
#         Output("pie-charts-carcer-graph", "figure"), 
#         Output("pie-charts-useful-graph", "figure"),
#         Output("pie-charts-sym-graph", "figure"),
#         Output("pie-charts-count_word-graph", "figure"),
#         Output("text_sum_exp", 'children'),
#         Output("text_sum_Gender", 'children'),
#         Output("text_sum_cancer", 'children'), 
#         Output("text_sum_useful", 'children'),
#         Output("text_sum_sym", 'children'), 
#         Output("text_sum_word", 'children'),
#         Output('datatable', 'children'),
#         Input("pie-charts-exp-names", "value"),
#         Input("pie-charts-Gender-names", "value"),
#         Input("pie-charts-cancer-names", "value"),
#         Input("pie-charts-useful-names", "value"),
#         Input("pie-charts-sym-names", "value"),
#         Input("slider-count_word-names", "value"),
#         prevent_initial_call=True,
#         )
#     def generate_chart(exp,Gender,carcer,useful,sym,count_word):
#         sorue_sym_4 = pd.read_csv('soure_url.csv')
#         soure = sorue_sym_4['url'][0]
#         nms = data_for_dash_raddit
#         if sym == [] or sym is None:
#             nms = data_for_dash_raddit
#         else:
#             for defind_sym in range(len(sym)):
#                 x = nms[nms[sym[defind_sym]]==1]
#                 nms = x       
#         nms = nms[nms['defind_exp_with_python'].isin(exp)]
#         nms = nms[nms['defind_Genden_with_python'].isin(Gender)]
#         nms = nms[nms['defind_cancer_with_nlp'].isin(carcer)]
#         nms = nms[nms['use_ful'].isin(useful)]
#         sym_c = nms.iloc[:, 10:-1]
#         sym_ca = sym_c.melt()
#         sym_can = (pd.crosstab(sym_ca['variable'], sym_ca['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'}))
#         plot_data=sym_can['มีการเล่า'].reset_index()
#         if sym == [] or sym is None :
#             plot_data_None = plot_data
#             plot_sym=plot_data_None
#         elif len(sym) == 1:
#             plot_data_None = plot_data
#             plot_sym=plot_data_None
#         else:
#             x_value=plot_data[plot_data['variable'].isin(sym)]['มีการเล่า'].to_list()
#             x_name=plot_data[plot_data['variable'].isin(sym)]['variable'].to_list()
#             sum_name =""
#             for sum_name_count in x_name:
#                 if sum_name == "":
#                     sum_name = sum_name+sum_name_count
#                 else:
#                     sum_name = sum_name+"&"+sum_name_count
#             x_plot_1 = pd.DataFrame(data={'variable': sum_name, 'มีการเล่า': x_value})
#             plot_data_non=plot_data[plot_data.variable.isin(sym) == False]
#             plot_data_nonnone=pd.concat([plot_data_non,x_plot_1])
#             plot_sym=plot_data_nonnone.drop_duplicates()
#         nms = nms[nms['จำนวนตัวอักษร']>=count_word]
#         fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'],color_discrete_sequence=px.colors.sequential.Emrld)
#         fig_2 = px.pie(nms, values='count_plot', names=nms['defind_Genden_with_python'],color='defind_Genden_with_python',color_discrete_map={'Male':'darkblue','Female':"magenta",'Gender not specified':'gray'})
#         fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'], y='count_plot',barmode='group',text_auto=True)
#         fig_4 = px.pie(nms, values='count_plot', names=nms['use_ful'],color_discrete_sequence=px.colors.sequential.Aggrnyl)
#         fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True)
#         fig_6 = px.line(nms,x='name', y='จำนวนตัวอักษร')
#         avg_33=nms['จำนวนตัวอักษร'].mean()
#         #สรุปกราฟประสบการณ์
#         sum_all_exp = nms['defind_exp_with_python']
#         sum_non_exp = nms[nms['defind_exp_with_python']=="Didn't tell the experience"]
#         sum_other_exp = nms[nms['defind_exp_with_python']=="Tell other people's experiences"]
#         sum_self_exp = nms[nms['defind_exp_with_python']=='Tell about your own experiences']
#         value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
#         value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
#         value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
#         text_1_en = f'''ผลจากกราฟ ประสบการณ์กับความคิดเห็น พบว่าความคิดเห็นที่ไม่ได้เล่าประสบการณ์เกี่ยวกับโรคมีจำนวน {len(sum_non_exp)}ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
#         { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก{len(sum_self_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
#          if len(sum_other_exp) > len(sum_self_exp) else 
#          f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
#         #สรุปกราฟเพศ 
#         sum_all_gen = nms['defind_Genden_with_python']
#         sum_female_gen = nms[nms['defind_Genden_with_python']=='Female']
#         sum_male_gen = nms[nms['defind_Genden_with_python']=='Male']
#         sum_non_gen = nms[nms['defind_Genden_with_python']=='Gender not specified']
#         value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
#         value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
#         value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
#         text_2_en = f'''ผลจากกราฟ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
#         { f"เพศชายจำนวน {len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_male_p_gen,2)} ในขณะที่อีก{len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
#          if len(sum_male_gen) > len(sum_female_gen) else 
#          f"เพศหญิงจำนวน {len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_female_p_gen,2)} ในขณะที่อีก{len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
#         # สรุปกราฟโรค
#         nms_can = nms[['defind_cancer_with_nlp','count_plot']]
#         nms_gro_cancer = nms_can.groupby('defind_cancer_with_nlp').sum().reset_index().sort_values(by='count_plot',ascending=False)
#         text_3_en ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
#         for fill in range(len(nms_gro_cancer)):
#             p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
#             text_3_en = text_3_en + f'\n- {nms_gro_cancer["defind_cancer_with_nlp"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}'
#         # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
#         sum_all_useful = nms['use_ful']
#         sum_have_useful = nms[nms['use_ful']=='maybe_useful']
#         sum_not_useful = nms[nms['use_ful']=='Not useful or not giving too much information']
#         value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
#         value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
#         text_4_en= f'''ผลจากกราฟ ความมีประโยชน์กับความคิดเห็น พบว่าส่วนมากเป็นความคิดเห็นที่
#         {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_have_useful_p,2)} ในขณะที่อีก{len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
#          if len(sum_have_useful) > len(sum_not_useful) else 
#          f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_not_useful_p,2)} ในขณะที่อีก{len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
#         #อาการ
#         text_5_en ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
#         for filler in range(len(plot_sym)):
#             plot_sym_next = plot_sym.reset_index()
#             text_5_en = text_5_en + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
#         # count word
#         text_6_en= f'''จากกราฟจะพบว่า จำนวนตัวอักษรในหัวข้อนี้มีค่ามากที่สุดคือ {nms['จำนวนตัวอักษร'].max()}\n
#             จำนวนตัวอักษรในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['จำนวนตัวอักษร'].min()}\n
#             จำนวนตัวอักษรในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_33,2)}\n'''
#         data140 = nms.iloc[:,:3]
#         data_for_export = dash_table.DataTable(columns=[{"name": i, "id": i} for i in data140.columns],data=data140.to_dict('records'),export_format="csv")
#         return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,text_1_en,text_2_en,text_3_en,text_4_en,text_5_en,text_6_en,data_for_export]
#     app.clientside_callback(
#             """
#             function () {            

#                 var printContents = document.getElementById('grid-print-area').innerHTML;
#                 var originalContents = document.body.innerHTML;

#                 document.body.innerHTML = printContents;

#                 window.print();

#                 document.body.innerHTML = originalContents;      
#                 location.reload()                              

#                 return window.dash_clientside.no_update
#             }
#             """,
#             Output("dummy", "children"),
#             Input("grid-browser-print-btn", "n_clicks"),
#             prevent_initial_call=True,
#         )

if __name__ == '__main__':
    app.run(debug=True)
