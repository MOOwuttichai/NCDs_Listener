#Facebook SC
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
from flask import Flask, request, render_template, make_response, session,jsonify,send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import os
from wordcloud import WordCloud # ใช้ทำ Word Cloud
import matplotlib.pyplot as plt # ใช้ Visualize Word Cloud
from pythainlp.tokenize import word_tokenize # เป็นตัวตัดคำของภาษาไทย
from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย

#dash
from dash import dash, dcc, html, Input, Output,dash_table
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

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
import nltk
nltk.download(['punkt', 'wordnet', 'omw-1.4', 'stopwords'])
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from textblob import TextBlob
import secrets


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

data = pd.read_csv('data_tokenizer.csv', encoding='utf-8-sig')
count_user = len(set(data['ชื่อ']))
count_comment = len(set(data['คำพูดโรค']))
comment=data.groupby('ชื่อ').sum().reset_index()
# สร้าง list เก็บตัว nlp เพิ่อนำไปวิเคราะห์โรค อาการ เเละเพศ
list_token = []
for i in range(len(comment['token'])):
  list_token.append(ast.literal_eval(comment['token'][i]))
#หาโรค
#--------------------------------------------------------
new_colcan = []
for i in range(len(list_token)):#len(comment)
    list_cancer = []
    for k in range(len(list_token[i])):
        if (list_token[i][k] == "มะเร็ง")|(list_token[i][k] == "โรคมะเร็ง")|(list_token[i][k] == "โรค"):
            list_cancer.append(list_token[i][k]+list_token[i][k+1])
            print(list_cancer)
    unique_list = list(OrderedDict.fromkeys(list_cancer))
    print(unique_list)
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
print(new_colcan)