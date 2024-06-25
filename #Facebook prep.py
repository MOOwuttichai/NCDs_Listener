#Facebook prep
# selenium-related
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from lxml import etree 

# other necessary ones
import urllib.request
import pandas as pd
import json
import time
import re
import datetime
from flask import Flask, request, render_template, session, redirect, url_for,jsonify
import numpy as np
import pandas as pd
import os

#prep
from attacut import tokenize, Tokenizer
import pythainlp
from pythainlp import sent_tokenize, word_tokenize, Tokenizer
from pythainlp.util import normalize
from pythainlp.corpus.common import thai_words
from collections import OrderedDict
from sklearn.cluster import KMeans
from pythainlp import spell
from pythainlp.spell import NorvigSpellChecker
from pythainlp.corpus import ttc
from pythainlp import correct
from pythainlp.util import normalize
from sentence_transformers import SentenceTransformer,util
import ast


app = Flask(__name__,static_folder=os.path.join(os.getcwd(),'static'))

@app.route('/', methods=['GET'])
def index():
  return render_template('text_2.html')

@app.route('/test.py', methods=['POST','GET'])
def test():
    data = pd.read_csv('data_commentsFB_docter copy.csv')  
    # ระบุโรค
    name_cancar_and_symptoms_pd = pd.read_csv('all_data_nameandsym.csv')
    name_cancar_list  = name_cancar_and_symptoms_pd['name_cancarTH_se'].tolist()
    name_cancar = [item for item in name_cancar_list if not(pd.isnull(item)) == True]

    # ระบุอาการ
    symptoms_pd = name_cancar_and_symptoms_pd[['Key_symptoms_TH','Values_symptoms_TH']].dropna()
    data_k_list = symptoms_pd['Key_symptoms_TH'].tolist()
    data_V_list = symptoms_pd['Values_symptoms_TH'].tolist()
    symptoms = {}
    for list_item in range(len(data_V_list)):
        split_t = ast.literal_eval(data_V_list[list_item])
        split_t = [n.strip() for n in split_t]
        symptoms[data_k_list[list_item]]=split_t

    #เเปลงหัวตาราง
    data.rename(columns={'name': 'ชื่อ', 'comments': 'คำพูดโรค'}, inplace=True)
    comment=data.groupby('ชื่อ').sum().reset_index()

    # สร้าง set ข้อมูลภาษาไทย
    words = set(thai_words())
    words.remove("โรคมะเร็ง")
    name =['กระเพาะปัสสวะ','กระเพาะปัสสาวะ','เยื่อบุโพรงมดลูก','ปากมดลูก','เม็ดเลือดขาว','กระเพาะอาหาร','กระเพราะอาหาร','ต่อมไทรอยด์','ต่อมไทยรอยด์','ท่อน้ำดี']
    for i in name:
        words.add(i)

    # สร้าง list เก็บตัว nlp เพิ่อนำไปวิเคราะห์โรค อาการ เเละเพศ
    list_token =[]
    Token_N= []
    checker_custom_filter = NorvigSpellChecker(dict_filter=None)
    for i in range(len(comment)):#len(comment)
        text= comment['คำพูดโรค'][i]
        custom_tokenizer = Tokenizer(words)
        Token = custom_tokenizer.word_tokenize(normalize(str(text)))
        Token.append('end')
        list_token.append(Token)
    time.sleep(8)
    #หาโรค
    #--------------------------------------------------------
    new_colcan = []
    for i in range(len(list_token)):#len(comment)
        list_cancer = []
        for k in range(len(list_token[i])):
            if (list_token[i][k] == "มะเร็ง")|(list_token[i][k] == "โรคมะเร็ง"):
                list_cancer.append(list_token[i][k]+list_token[i][k+1])
        unique_list = list(OrderedDict.fromkeys(list_cancer))
        #----------------------------------------------------------
        list_define_cancer = []
        for i in range(len(unique_list)):
            for j in range(len(name_cancar)):
                if unique_list[i]==name_cancar[j]:
                    list_define_cancer.append(unique_list[i])
        #-----------------------------------------------------
        cancer_list_de2 =[]
        if len(list_define_cancer) > 0:
            if len(list_define_cancer) == 2:
                cancer_list_de2.append('เล่ามากกว่า 2 โรค')
            elif len(list_define_cancer)==1:
                cancer_list_de2.append(list_define_cancer[0])
        elif list_define_cancer==[]:
            cancer_list_de2.append('ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น')
        if len(cancer_list_de2)> 0 :
            new_colcan.append(cancer_list_de2[0])
        elif len(cancer_list_de2)== 0 :
            new_colcan.append('ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น')
    # สร้าง list เพศ 
    Genden = {'ชาย':['พ่อ','บิดา','พี่ชาย','น้องชาย','ลูกชาย','สามี','พัว','ผัว','ปู่','ตา','คุณปู่','คุณตา','คุณพ่อ',
                    'ปู่ทวด','ตาทวด','ลุง','อาหนู','คุณอา','คุณลุง','หลายชาย','ลูกเขย','เขย','พี่เขย','น้องเขย',
                    'พ่อตา','พ่อผม','พ่อหนู','พ่อพม','ชาย','หนุ่ม','ลช.','ผ่อ','ชย.','น้าชาย','ผ่อตา','หน.']
            ,'หญิง':['แม่','เเม่','คุณแม่','มารดา','พี่สาว','น้องสาว','ลูกสาว','ภรรยา','เมีย','ย่า','ยาย','คุณย่า',
                    'คุณยาย','คุณเเม่','ย่าทวด','ยายทวด','ป้า','น้า','คุณป้า','คุณน้า','หลายสาว','ลูกสะใถ้',
                    'ลูกสะใภ้','สะใภ้','พี่สะใภ้','น้องสะใภ้','เเม่ผม','เเม่หนู','เเม่พม','แม่ผม','แม่หนู','แม่พม','สาว','หญิง','ก้อน','คลำ']}
    # หาเพศ โดยใช้nlp
    new_colgenden=[]
    list_genden=[]
    for i in range(len(list_token)):
        for j in range(len(Genden['หญิง'])):
            for k in range(len(list_token[i])):
                if (list_token[i][k] == Genden['ชาย'][j]):
                    list_genden.append('เพศชาย')
                elif(list_token[i][k] == Genden['หญิง'][j]):
                    list_genden.append('เพศหญิง')
        genden_list =[]
        genden_list = list(OrderedDict.fromkeys(list_genden)) # ลบคำซ้ำ
        #-------------------------------------------------------------------
        list_define_genden = []
        if len(genden_list) > 0 :
            if len(genden_list) == 2:
                list_define_genden.append('เล่าทั้งสองเพศ')
            elif len(genden_list)==1:
                list_define_genden.append(genden_list[0])
        elif len(genden_list)==0:
            list_define_genden.append('ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น')
        genden_list_de =[]
        genden_list_de = list(OrderedDict.fromkeys(list_define_genden))
        new_colgenden.append(genden_list_de[0])

    # หาอาการโดย nlp
    symptoms_colcan = []
    for i in range(len(list_token)):
        list_symptoms= []
        for j in range(len(list_token[i])):
            for k in symptoms:
                for l in range(len(symptoms[k])):
                    if list_token[i][j] == symptoms[k][l]:
                        list_symptoms.append(symptoms[k][0])
        unique_list_symptoms = list(OrderedDict.fromkeys(list_symptoms))
        if len(unique_list_symptoms) > 0:
            symptoms_colcan.append(unique_list_symptoms)
        else :
            symptoms_colcan.append(['ไม่มีการระบุอาการ'])

    #สร้างฟังชั่นหาเพศกับใครเป็นคนพูด
    def detect_person(comment):
    # คำที่ใช้ตรวจสอบว่ามีใครเป็นคนอยู่ในความคิดเห็น
        other = ['พ่อ','บิดา','พี่ชาย','น้องชาย','ลูกชาย','สามี','พัว','ผัว','ปู่','ตา','คุณปู่','คุณตา','คุณพ่อ',
                'ปู่ทวด','ตาทวด','ลุง','อาหนู','คุณอา','คุณลุง','หลายชาย','ลูกเขย','เขย','พี่เขย','น้องเขย',
                'พ่อตา','พ่อผม','พ่อหนู','พ่อพม','ชาย','หนุ่ม''แม่','เเม่','คุณแม่','มารดา','พี่สาว','น้องสาว',
                'ลูกสาว','ภรรยา','เมีย','ย่า','ยาย','คุณย่า','คุณยาย','คุณเเม่','ย่าทวด','ยายทวด','ป้า',
                'น้า','คุณป้า','คุณน้า','หลายสาว','ลูกสะใถ้','ลูกสะใภ้','สะใภ้','พี่สะใภ้','น้องสะใภ้','เเม่ผม','เเม่หนู','เเม่พม','แม่ผม','แม่หนู','แม่พม','สาว','หญิง']
        myself = ['ผมเป็น','ผมเอง','กระผม','พมเป็น','พมเอง','กระพม','หนูเอง','หนู','ดิฉัน','ตัวเอง','ก้อน','คลำ']
        # ตรวจสอบคำในความคิดเห็น
        for keyword in  other:
            if keyword in comment and "อาการ" not in comment :
                return 'เล่าประสบการณ์คนอื่น'
        for keyword in  myself:
            if keyword in comment:
                return 'เล่าประสบการณ์ตัวเอง'
        # หากไม่พบคำที่บ่งบอกถึงคน
        return 'ไม่ได้เล่าประสบการณ์'
    def detect_gender_other(comment):
        # คำที่บ่งบอกถึงเพศชาย
        male_keywords = ['พ่อ','บิดา','พี่ชาย','น้องชาย','ลูกชาย','สามี','พัว','ผัว','ปู่','ตา','คุณปู่','คุณตา','คุณพ่อ',
                        'ปู่ทวด','ตาทวด','ลุง','อาหนู','คุณอา','คุณลุง','หลายชาย','ลูกเขย','เขย','พี่เขย','น้องเขย',
                        'พ่อตา','พ่อผม','พ่อหนู','พ่อพม','ชาย','หนุ่ม']
        # คำที่บ่งบอกถึงเพศหญิง
        female_keywords = ['แม่','เเม่','คุณแม่','มารดา','พี่สาว','น้องสาว','ลูกสาว','ภรรยา','เมีย','ย่า','ยาย','คุณย่า','คุณยาย','คุณเเม่','ย่าทวด','ยายทวด','ป้า',
                        'น้า','คุณป้า','คุณน้า','หลายสาว','ลูกสะใถ้','ลูกสะใภ้','สะใภ้','พี่สะใภ้','น้องสะใภ้','เเม่ผม','เเม่หนู','เเม่พม','แม่ผม','แม่หนู','แม่พม','สาว','หญิง']
        # ตรวจสอบคำในความคิดเห็น
        for keyword in male_keywords:
            if keyword in comment and "อาการ" not in comment :
                return "เพศชาย"
        for keyword in female_keywords:
            if keyword in comment:
                return "เพศหญิง"
        # หากไม่พบคำที่บ่งบอกถึงเพศ
        return "ไม่ระบุเพศ"
    def detect_gender_self(comment):
        # คำที่บ่งบอกถึงเพศชาย
        male_keywords = ['ผมเป็น','ครับ','ผมเอง','คับ','กระผม','พมเป็น','พมเอง','กระพม']
        # คำที่บ่งบอกถึงเพศหญิง
        female_keywords = ['ค่ะ','คะ','หนูเอง','หนูเป็น','ดิฉัน','ก้อน','คลำ']
        # ตรวจสอบคำในความคิดเห็น
        for keyword in male_keywords:
            if keyword in comment:
                return "เพศชาย"
        for keyword in female_keywords:
            if keyword in comment:
                return "เพศหญิง"
        # หากไม่พบคำที่บ่งบอกถึงเพศ
        return "ไม่ระบุเพศ"
    #เเบ่งเพศเเละใครเล่าโดยใช้ python
    k1=[]
    k2=[]
    for i in comment['คำพูดโรค']:
        k1.append(detect_person(str(i)))
        if detect_person(str(i)) == 'เล่าประสบการณ์คนอื่น':
            k2.append(detect_gender_other(str(i)))
        elif detect_person(str(i)) == 'เล่าประสบการณ์ตัวเอง':
            k2.append(detect_gender_self(str(i)))
        elif detect_person(str(i)) == 'ไม่ได้เล่าประสบการณ์':
            k2.append(detect_gender_self(str(i)))

    #SentenceTransformer
    sentences = list(comment['คำพูดโรค'])
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    embeddings = model.encode(sentences)
    #Normalize the embeddings to unit length
    Normalize_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    clustering_model = KMeans(n_clusters=2)
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_
    clusternd_sentences= {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clusternd_sentences:
            clusternd_sentences[cluster_id] = []
        clusternd_sentences[cluster_id].append(sentences[sentence_id])

    #เเบ่งข้อมูลว่าอันไหนมีประโยนช์
    len_1=[]
    len_2=[]
    for i in range(len(clusternd_sentences)):
        x=len(clusternd_sentences[1][i])
        len_1.append(x)
        y=len(clusternd_sentences[0][i])
        len_2.append(y)
    if max(len_1) < max(len_2) :
        Pop=comment[comment['คำพูดโรค'].isin(clusternd_sentences[1])]
        Pop['โรค_clusternd'] = 'ไม่มีประโยชน์_หรือ_ให้ข้อมูลน้อยเกินไป'
        pop_use=comment[comment['คำพูดโรค'].isin(clusternd_sentences[0])]
        useful = clusternd_sentences[0]
    else :
        Pop=comment[comment['คำพูดโรค'].isin(clusternd_sentences[0])]
        pop_use=comment[comment['คำพูดโรค'].isin(clusternd_sentences[1])]
        Pop['โรค_clusternd'] = 'ไม่มีประโยชน์_หรือ_ให้ข้อมูลน้อยเกินไป'
        useful = clusternd_sentences[1]

    # เเบ่งข้อมูลมีประโยชน์ว่าเป็นโรคอะไร
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    useful_embeddings = model.encode(useful)
    #Normalize the embeddings to unit length
    Normalize_useful_embeddings = useful_embeddings / np.linalg.norm(useful_embeddings, axis=1, keepdims=True)
    clustering_useful_model = KMeans(n_clusters=len(name_cancar))
    clustering_useful_model.fit(Normalize_useful_embeddings)
    cluster_assignment_useful = clustering_useful_model.labels_
    clusternd_useful_sentences= {}
    for sentence_ID, cluster_ID in enumerate(cluster_assignment_useful):
        if cluster_ID not in clusternd_useful_sentences:
            clusternd_useful_sentences[cluster_ID] = []
        clusternd_useful_sentences[cluster_ID].append(useful[sentence_ID])
    # สร้างตาราง
    Data_pre_and_clane = comment
    Data_pre_and_clane['โรค'] = new_colcan

    def define_Cencer_with_clusternd(use_clusternd_sentences,n_clusters):
        data = pd.DataFrame()
        for i in range(n_clusters):
            point = []
            define_C =[]
            test = Data_pre_and_clane[Data_pre_and_clane['คำพูดโรค'].isin(use_clusternd_sentences[i])]
            test_cer = list(test['โรค'])
            for j in range(len(test_cer)):
                if test_cer[j] in name_cancar:
                    point.append(test_cer[j])
            if len(set(point)) == 0 :
                for x in range(len(test_cer)):
                    define_C.append('ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น')
            elif len(set(point)) == 1 :
                for x in range(len(test_cer)):
                    define_C.append(point[0])
            elif len(set(point)) > 1:
                for x in range(len(test_cer)):
                    define_C.append('มีโอกาสเป็นโรคมะเร็งมากกว่า 2 เเบบ')
            test['โรค_clusternd'] = define_C
            data = pd.concat([data,test])
        return data
    define_Cencer_a=define_Cencer_with_clusternd(clusternd_useful_sentences,len(name_cancar))
    usedata=pd.concat([Pop,define_Cencer_a])
    clust_list = usedata['โรค_clusternd'].tolist()
    # สร้างตาราง

    Data_pre_and_clane['โรค_clust'] = clust_list
    Data_pre_and_clane['ใครเล่า'] = k1
    Data_pre_and_clane['เพศเเบ่งโดยใช้_nlp'] = new_colgenden
    Data_pre_and_clane['เพศเเบ่งโดยใช้_python'] = k2
    Data_pre_and_clane['อาการ']=symptoms_colcan
    label_symptoms=Data_pre_and_clane['อาการ'].str.join(sep='*').str.get_dummies(sep='*')
    Data_pre_and_clane=Data_pre_and_clane.join(label_symptoms)
    Data_pre_and_clane.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
    tables = Data_pre_and_clane.to_html(classes='table table-striped', index=False)

    return  render_template('test.html',  tables=[tables], titles=data.columns.values)
    

if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0', port=8001)