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
from flask import Flask, request, render_template, session, redirect, url_for,jsonify,send_from_directory
import numpy as np
import os
from wordcloud import WordCloud # ใช้ทำ Word Cloud
import matplotlib.pyplot as plt # ใช้ Visualize Word Cloud
from pythainlp.tokenize import word_tokenize # เป็นตัวตัดคำของภาษาไทย
from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย


#dash
import dash
import plotly
import plotly.graph_objs as go
from dash import Dash, html, dash_table, dcc
import plotly.express as px
import dash
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

server = Flask(__name__,static_folder=os.path.join(os.getcwd(),'static'))
app1 = dash.Dash(requests_pathname_prefix="/app1/")
@server.route('/', methods=['GET'])
def index():
  return render_template('input2.html')

@server.route('/process.py', methods=['POST'])
def process():
    import pandas as pd
    url = request.form['url']
    url_chack = str(url).split('/')[2]
    data_soure_a = {'url':[url_chack]}
    data_soure_b = pd.DataFrame(data_soure_a)
    data_soure_b.to_csv('soure_url.csv',index=False)
    # facebook
    if url_chack == 'www.facebook.com':
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )

        with open('facebook_credentials.txt') as file:
            EMAIL = file.readline().split('"')[1]
            PASSWORD = file.readline().split('"')[1]
            
        browser = webdriver.Chrome(options=option)
        browser.get("http://facebook.com")
        browser.maximize_window()
        wait = WebDriverWait(browser, 30)
        email_field = wait.until(EC.visibility_of_element_located((By.NAME, 'email')))
        email_field.send_keys(EMAIL)
        pass_field = wait.until(EC.visibility_of_element_located((By.NAME, 'pass')))
        pass_field.send_keys(PASSWORD)
        pass_field.send_keys(Keys.RETURN)

        time.sleep(20)
        x='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[52]/div[1]/div/div[2]/span/span'
        a=int(x[162:164])
        k=x

        aoa='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[1]/div/div/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/span/div[2]/div/div'
        kok={'a_a':'div/div/div','b_a':'div[2]/div/div','b_b':'div/div[2]/div','b_c':'div/div/div[2]','c_a':'div[3]/div/div','c_b':'div/div[3]/div','c_c':'div/div/div[3]'}
        LOL=[]
        time.sleep(20)
        browser.get(url)
        wait = WebDriverWait(browser, 120) # once logged in, free to open up any target page
        time.sleep(7)
        
        count_r = 0
        switch = True
        # เปิดความคิดเห็นเพิ่มเติม
        try: 
            while switch:
                count_r += 1
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                l = browser.find_element(By.XPATH,k)
                l.click()
                a+=50
                k = x[:162]+str(a)+x[164:]
                time.sleep(7)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(11)
        except:
            pass

         # เช็กว่าลงสุดไหม
        SCROLL_PAUSE_TIME = 4

        # Get scroll height
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            for i in range(5):
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
           
            # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # เปิดเพิ่มเติม
        r=int(aoa[-81:-80])
        for i in range(2):
            for i in range(9999):
                r += 1
                for j in kok:
                    kra = aoa[:-81]+ str(r) + aoa[-80:-14] + kok[j]
                    LOL.append(kra)
            for g in range(1000):
                try:
                    l = browser.find_element(By.XPATH,LOL[g])
                    l.click()
                    time.sleep(1)
                except:
                    pass

        # เช็กว่าลงสุดไหมv.2
        last_height = browser.execute_script("return document.body.scrollHeight")
        while True:
            for i in range(3):
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(5)
                # Calculate new scroll height and compare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        #setup bs4 and data
        #ดึงข้อมูล
        comments=[]
        names=[]
        re_chat_all=[]
        like_kk = []
        count=[]
        html =  BeautifulSoup(browser.page_source, "html.parser")
        soup = BeautifulSoup(browser.page_source, 'lxml')
        dom = etree.HTML(str(soup))
        # ## comment
        re_chak = dom.xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[3]/div/div/div/div[2]/div/div/text()')
        test_chak = ''
        for item_chak in re_chak:
            test_chak = test_chak + item_chak
        result = html.find_all('div',{"class":"xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"})
        # ## name
        name = html.find_all(["span"],{"class":"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
        # ## re_chat
        for i in range(len(result)):
            x1=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/text()')
            y1=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/div/div[4]/text()')
            z1=x1+y1
            try:
                re_chat_all.append((re.findall(r'\b\d+\b',z1[0]))[0])
            except:
                re_chat_all.append(0)
        # like
        for i in range(len(result)):
            x2=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/span/div/div[1]/span/text()')
            try:
                like_kk.append(x2[0])
            except:
                like_kk.append(0)

        # แปลง like จาก str ไปเป็น int
        like_count=[]
        for j in like_kk:
            try:
                split_v_like=j.split(' ')
                if split_v_like[1] == 'พัน':
                    ror=float(split_v_like[0])*1000
                    T_V_like=int(ror)
                elif split_v_like[1] == 'หมื่น':
                    ror=float(split_v_like[0])*100000
                    T_V_like=int(ror)
                elif split_v_like[1] == 'แสน':
                    ror=float(split_v_like[0])*1000000
                    T_V_like=int(ror)
                elif split_v_like[1] == 'ล้าน':
                    ror=float(split_v_like[0])*100000000
                    T_V_like=int(ror)
                like_count.append(T_V_like)
            except:
                like_count.append(int(j))
                
        #เริ่มเก็บข้อมูล
        FBcomments = []
        for item in result:
            comments.append(item.text)
        for item in comments:
            if item == test_chak:
                pass
            else:
                FBcomments.append(item)
        for item in name :
            names.append(item.text)
        data = pd.DataFrame()

        #นับความยาว ความคิดเห็น
        for item in FBcomments:
            count.append(len(item))

        data_comment=pd.DataFrame(data={'comments':FBcomments})
        data_name=pd.DataFrame(data={'name':names})
        data_rechat=pd.DataFrame(data={'rechat':re_chat_all})
        data_like=pd.DataFrame(data={'like':like_kk})
        data_count=pd.DataFrame(data={'count':count})
        # ทำตาราง
        data = data_comment
        data = data.join(data_name).fillna('NaN_name')
        data = data.join(data_rechat).fillna(0)
        data = data.join(data_like).fillna(0)
        data = data.join(data_count).fillna(0)
        data_f = data.iloc[:,[1,0,3,2,4]]
        number_of_rows = len(data)
        number_of_columns = len(data.columns)
        data.to_csv('data_commentsFB_docter.csv', index=False, encoding='utf-8-sig')
        browser.close() 
        
    # reddit
    elif url_chack == 'www.reddit.com':
        names=[]
        comments=[]
        data = pd.DataFrame()
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # button = driver.find_element("CLASS",'text-tone-2 text-12 no-underline hover:underline px-xs py-xs flex ml-[3px] xs:ml-0 !bg-transparent !border-0')
        # button.click()
        try: 
            for i in range(99) :
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                wait = WebDriverWait(driver, 60)
                time.sleep(3)
                l = driver.find_element("xpath",'//*[@id="comment-tree"]/faceplate-partial/div[1]/button')
                l.click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                wait = WebDriverWait(driver, 60)
                time.sleep(3)
        except:
            pass
        time.sleep(5)
        html =  BeautifulSoup(driver.page_source, "html.parser")
        result = html.find_all('div',{"class":"py-0 xs:mx-xs mx-2xs inline-block max-w-full"})
        name = html.find_all(['a',"span"],{"class":["truncate font-bold text-neutral-content-strong text-12 hover:underline","truncate font-bold text-neutral-content-strong text-12 hover:no-underline text-neutral-content-weak"]})
        for item in result:
            comments.append(item.text)
        for item in name :
            names.append(item.text)
        if len(comments)>len(names):
            differ = len(comments)-len(names)
            for i in range(differ):
                names.append(f'fillname_{i}')
        elif len(comments)<len(names):
            differ = len(names)-len(FBcomments)
            for i in range(differ):
                FBcomments.append('comments_miss')
        count_1=[]
        for item in comments:
            count_1.append(len(item))

        data['name'] = names
        data['comments'] = comments
        data['count'] = count_1
        data=data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
        data_red = data[data['comments'] != 'comments_miss']
        number_of_rows = len(data)
        number_of_columns = len(data.columns)
        data.to_csv('data_commentsred_docter.csv', index=False, encoding='utf-8-sig')
        driver.close() 

    if url_chack == 'www.facebook.com': 
        _ = ['like','จำนวนการตอบกลับ','ความยาว']
        data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
        def sort_data(column_name):
            if column_name == 'like':
                data.sort_values('like', inplace=True, ascending=False)
            elif column_name == 'การตอบกลับ':
                data.sort_values('rechat', inplace=True, ascending=False)
            elif column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        _ = ['like','จำนวนการตอบกลับ','ความยาว']
        sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['name_cancarTH'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list()
        #------word cloud---------#
        from pythainlp.tokenize import word_tokenize as to_th_k # เป็นตัวตัดคำของภาษาไทย
        from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย
        text_th= ''
        for row in data['comments']: # ให้ python อ่านข้อมูลรีวิวจากทุก row ใน columns 'content'
            text_th = text_th + row.lower() + ' ' # เก็บข้อมูลรีวิวของเราทั้งหมดเป็น String ในตัวแปร text

        wt_th = to_th_k(text_th, engine='newmm') # ตัดคำที่ได้จากตัวแปร text

        path_th = 'THSarabunNew-20240628T045147Z-001\THSarabunNew\THSarabunNew.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
        wordcloud_th = WordCloud(font_path = path_th, # font ที่เราต้องการใช้ในการแสดงผล เราเลือกใช้ THSarabunNew
                            stopwords = thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                            relative_scaling = 0.3,
                            min_font_size = 1,
                            background_color = "white",
                            width = 1024,
                            height = 768,
                            max_words = 500, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                            colormap = 'plasma',
                            scale = 3,
                            font_step = 4,
                            collocations = False,
                            regexp = r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                            margin=2).generate(' '.join(wt_th)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

        wordcloud_th.to_file("wordcloud.png") 

    elif url_chack == 'www.reddit.com':
        from nltk.tokenize import word_tokenize as to_en
        from nltk.stem import WordNetLemmatizer
        data = pd.read_csv("data_commentsred_docter.csv")
        _ = ['ความยาว']
        def sort_data(column_name):
            if column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        sort_options = ['ความยาวของความคิดเห็น']
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['cancer_names_en'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
        import pandas as pd
        #------word cloud---------#
        # Combine all text into a single string
        text = ' '.join(data['comments'].str.lower())
        # Tokenize the text
        tokens = to_en(text)
        # Remove stop words and lemmatize
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        filtered_words = [lemmatizer.lemmatize(w) for w in tokens if w.isalpha() and w not in stop_words]
        # Create a word cloud
        wordcloud = WordCloud(
            stopwords=stop_words,
            background_color="white",
            width=1024,
            height=768,
            max_words=500,
            colormap='plasma',
            scale=3,
            font_step=4,
            collocations=False,
            margin=2
        ).generate(' '.join(filtered_words))

        # Save the word cloud to a file
        wordcloud.to_file("wordcloud.png")
    max_v = []
    min_v = []
    avg_v = []
    for i in range(len(data.columns)):
        if i >= 2:
            max_v.append(max(data[data.columns[i]].tolist()))
            min_v.append(min(data[data.columns[i]].tolist()))
            avg_v.append(np.mean(data[data.columns[i]].tolist()))
    descriptive = pd.DataFrame()
    descriptive[' '] = _
    descriptive['max'] = max_v
    descriptive['min'] = min_v
    descriptive['avg'] = avg_v
    descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # เรียงลำดับข้อมูลตามค่าเริ่มต้น (like)
    sorted_data = sort_data('like')
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    # เตรียมตัวเลือกสำหรับ dropdownlist

    return  render_template('output2.html',  tables=[tables], titles=data.columns.values, 
                            sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])

@server.route('/sort', methods=['POST','GET'])
def sort():
    soure_b = pd.read_csv('soure_url.csv')
    soure = soure_b['url'][0]
    if soure == 'www.facebook.com':
        data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
        def sort_data(column_name):
            if column_name == 'like':
                data.sort_values('like', inplace=True, ascending=False)
            elif column_name == 'การตอบกลับ':
                data.sort_values('rechat', inplace=True, ascending=False)
            elif column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
        # number_of_rows = len(data)
        # number_of_columns = len(data.columns) 
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['name_cancarTH'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
    elif soure == 'www.reddit.com':
        data =  pd.read_csv("data_commentsred_docter.csv")
        def sort_data(column_name):
            if column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        sort_options = ['ความยาวของความคิดเห็น']
        # number_of_rows = len(data)
        # number_of_columns = len(data.columns)  
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['cancer_names_en'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
    descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
    descriptive = descriptive.iloc[:, 1:]
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # รับค่าคอลัมน์ที่เลือกจาก dropdownlist
    column_name = request.form['sort_column']
    # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
    sorted_data = sort_data(column_name)
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('output2.html', tables=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1],soure=soure)

@server.route('/wordcloud.png')
def wordcloud():
    return send_from_directory('.', 'wordcloud.png')
#number_of_rows=number_of_rows, number_of_columns=number_of_columns,

@server.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
  if request.method == 'POST':
        # ข้อมูลที่ได้รับจากการกรอง
        skill = request.form['skill']
        symptom  = request.form['symptom'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        # ข้อมูลอาการเพิ่มเติม
        c_submit= request.form['custId']
        soure_b = pd.read_csv('soure_url.csv')
        soure = soure_b['url'][0]
        if soure == 'www.facebook.com':
            data_defu = pd.read_csv('name_cancer_and_symptoms (2).csv')
            data_defu_sym = data_defu[['Key_symptoms_TH','Values_symptoms_TH']].dropna()
            data_value_TH = pd.DataFrame()
            data_symptoms_TH = pd.DataFrame()
            data_value_TH['name_cancarTH_se']=name_cancer
            data_symptoms_TH['Key_symptoms_TH'] =name_symptom
            data_symptoms_TH_1 = data_symptoms_TH.merge(data_defu_sym, how='left',on='Key_symptoms_TH')
            value_symptoms_TH= data_symptoms_TH_1[data_symptoms_TH_1['Values_symptoms_TH'].isna()]
            list_of_sym_va_th = value_symptoms_TH['Key_symptoms_TH'].tolist()
            for i in list_of_sym_va_th:
                data_symptoms_TH_1.fillna(f"['{i}']",limit=1,inplace=True)
            # สร้างตาราง
            all_data = pd.DataFrame()
            list_100 = list(range(0,100))
            all_data['index'] = list_100
            all_data = all_data.merge(data_value_TH.reset_index(), how='outer')
            all_data = all_data.merge(data_symptoms_TH_1.reset_index(), how='outer')
        elif soure == 'www.reddit.com':
            data_defu = pd.read_csv('name_cancer_and_symptoms (2).csv')
            data_defu_sym = data_defu[['Key_symptoms_EN','Valuessymptoms_EN']].dropna()
            data_value_TH = pd.DataFrame()
            data_symptoms_TH = pd.DataFrame()
            data_value_TH['cancer_names_en_se']=name_cancer
            data_symptoms_TH['Key_symptoms_EN'] =name_symptom
            data_symptoms_TH_1 = data_symptoms_TH.merge(data_defu_sym, how='left',on='Key_symptoms_EN')
            value_symptoms_TH= data_symptoms_TH_1[data_symptoms_TH_1['Valuessymptoms_EN'].isna()]
            list_of_sym_va_th = value_symptoms_TH['Key_symptoms_EN'].tolist()
            for i in list_of_sym_va_th:
                data_symptoms_TH_1.fillna(f"['{i}']",limit=1,inplace=True)
            # สร้างตาราง
            all_data = pd.DataFrame()
            list_100 = list(range(0,100))
            all_data['index'] = list_100
            all_data = all_data.merge(data_value_TH.reset_index(), how='outer')
            all_data = all_data.merge(data_symptoms_TH_1.reset_index(), how='outer')
        all_data['chack_submit'] = c_submit
        all_data.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
        msg = 'New record created successfully'  
        return jsonify(msg)     

@server.route('/page3.py',methods=["POST","GET"])
def index_2():
    try:
      data_defind = pd.read_csv('all_data_nameandsym.csv')
      # num_data_defind = data_defind[data_defind['chack_submit'][0]]
      data_defind = data_defind.drop('chack_submit', axis=1)
      data_defind.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
    except:
      sorue_sym_2 = pd.read_csv('soure_url.csv')
      sorue = sorue_sym_2['url'][0]
      if sorue == 'www.facebook.com':
        data_sy_na = pd.read_csv('name_cancer_and_symptoms (2).csv')
        data_defind = data_sy_na[['name_cancarTH','Key_symptoms_TH','Values_symptoms_TH']]
        data_defind = data_defind.rename(columns={'name_cancarTH': 'name_cancarTH_se'})
        data_defind.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
      elif sorue == 'www.reddit.com':
        data_sy_na = pd.read_csv('name_cancer_and_symptoms (2).csv')
        data_defind = data_sy_na[['cancer_names_en','Key_symptoms_EN','Valuessymptoms_EN']]
        data_defind=data_defind.rename(columns={'cancer_names_en': 'cancer_names_en_se'})
        data_defind.to_csv('all_data_nameandsym.csv')
    sorue_sym_3 = pd.read_csv('soure_url.csv')
    sorue = sorue_sym_3['url'][0]
    if sorue == 'www.facebook.com':
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
            Pop['ความมีประโยชน์'] = 'ไม่มีประโยชน์_หรือ_ให้ข้อมูลน้อยเกินไป'
            pop_use=comment[comment['คำพูดโรค'].isin(clusternd_sentences[0])]
            useful = clusternd_sentences[0]
        else :
            Pop=comment[comment['คำพูดโรค'].isin(clusternd_sentences[0])]
            pop_use=comment[comment['คำพูดโรค'].isin(clusternd_sentences[1])]
            Pop['โรค_clusternd'] = 'ไม่มีประโยชน์_หรือ_ให้ข้อมูลน้อยเกินไป'
            Pop['ความมีประโยชน์'] = 'ไม่มีประโยชน์_หรือ_ให้ข้อมูลน้อยเกินไป'
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
        define_Cencer_a['ความมีประโยชน์'] = 'อาจมีประโยชน์หรืออาจให้ข้อมูลเพียงพอ'
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
    elif sorue == 'www.reddit.com':
        data = pd.read_csv('data_commentsred_docter.csv')  
        # ระบุโรค
        name_cancar_and_symptoms_pd = pd.read_csv('all_data_nameandsym.csv')
        name_cancar_list  = name_cancar_and_symptoms_pd['cancer_names_en_se'].tolist()
        cancer_names_en = [item for item in name_cancar_list if not(pd.isnull(item)) == True]
        # ระบุอาการ
        symptoms_pd = name_cancar_and_symptoms_pd[['Key_symptoms_EN','Valuessymptoms_EN']].dropna()
        data_k_list = symptoms_pd['Key_symptoms_EN'].tolist()
        data_V_list = symptoms_pd['Valuessymptoms_EN'].tolist()
        cancer_symptoms_en = {}
        for list_item in range(len(data_V_list)):
            split_t = ast.literal_eval(data_V_list[list_item])
            split_t = [n.strip() for n in split_t]
            cancer_symptoms_en[data_k_list[list_item]]=split_t
        data=data.groupby('name').sum().reset_index()
        def token(data):
            tokens = nltk.word_tokenize(data)
            tokens.insert(0, 'start')
            tokens.append('end')
            return tokens
        def remove_(tokens):
            final = [word.lower()
                    for word in tokens if word not in stopwords.words("english")]
            return final
        # Lemmatizing
        def lemma(final):
            # initialize an empty string
            str1 = ' '.join(final)
            s = TextBlob(str1)
            lemmatized_sentence = " ".join([w.lemmatize() for w in s.words])
            return final
        data_com = data['comments'].to_list()
        list_token_red = []
        for item_comment_red in range(len(data_com)):
            data_r_token = token(data_com[item_comment_red].translate(str.maketrans('', '', string.punctuation)))
            data_r_token = remove_(data_r_token)
            data_r_token = lemma(data_r_token)
            list_token_red.append(data_r_token)
        column_cancer_nlp_rad=[]
        for list_token_i in range(len(list_token_red)):#len(comment)
            list_cancer_en = []
            for list_token_k in range(len(list_token_red[list_token_i])):
                for cancer_names_j in range(len(cancer_names_en)):
                    if (list_token_red[list_token_i][list_token_k] == 'cancer'):
                        list_cancer_en.append(list_token_red[list_token_i][list_token_k-1]+list_token_red[list_token_i][list_token_k])
            unique_list_en = list(OrderedDict.fromkeys(list_cancer_en))
        #----------------------------------------------------------------------------
            list_define_cancer_en = []
            new_list_en=[]
            for i in range(len(unique_list_en)):
                for j in range(len(cancer_names_en)):
                    if unique_list_en[i]==cancer_names_en[j]:
                        list_define_cancer_en.append(unique_list[i])
        #----------------------------------------------------------------------------
            cancer_list_de_red =[]
            if len(list_cancer_en) > 0:
                if len(list_cancer_en) == 2:
                    cancer_list_de_red.append('Tell more than 2 diseases.')
                elif len(list_cancer_en)==1:
                    cancer_list_de_red.append(list_cancer_en[0])
            elif list_cancer_en==[]:
                cancer_list_de_red.append('Unable to identify / not sure if it is')
            if len(cancer_list_de_red)> 0 :
                column_cancer_nlp_rad.append(cancer_list_de_red[0])
            elif len(cancer_list_de_red)== 0 :
                column_cancer_nlp_rad.append('Unable to identify / not sure if it is')
        #-----------------------------------
        all_reddit_data = data
        all_reddit_data['defind_cancer_with_nlp'] = column_cancer_nlp_rad
        #-----------------------------------
        sentences_en = list(data['comments'])
        model_red = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        embeddings_red = model_red.encode(sentences_en)
        #Normalize the embeddings to unit length
        Normalize_embeddings_red = embeddings_red / np.linalg.norm(embeddings_red, axis=1, keepdims=True)
        clustering_model_red = KMeans(n_clusters=2)
        clustering_model_red.fit(Normalize_embeddings_red)
        cluster_assignment_en = clustering_model_red.labels_
        clusternd_sentences_en= {}
        for sentence_id_red, cluster_id_red in enumerate(cluster_assignment_en):
            if cluster_id_red not in clusternd_sentences_en:
                clusternd_sentences_en[cluster_id_red] = []
            clusternd_sentences_en[cluster_id_red].append(sentences_en[sentence_id_red])
        len_3=[]
        len_4=[]
        for i in range(len(clusternd_sentences_en)):
            x=len(clusternd_sentences_en[1][i])
            len_3.append(x)
            y=len(clusternd_sentences_en[0][i])
            len_4.append(y)
        if max(len_3) < max(len_4) :
            Pop_en=data[data['comments'].isin(clusternd_sentences_en[1])]
            Pop_en['cancer_clusternd'] = 'Not useful or not giving too much information'
            Pop_en['defind_cancer_with_clusternd'] = 'Not useful or not giving too much information'
            Pop_en_use=data[data['comments'].isin(clusternd_sentences_en[0])]
            useful = clusternd_sentences_en[0]
    # useful['cancer_clusternd'] = 'It may be useful or it may provide enough information.'
        else :
            Pop_en=data[data['comments'].isin(clusternd_sentences_en[0])]
            Pop_en_use=data[data['comments'].isin(clusternd_sentences_en[1])]
            Pop_en['cancer_clusternd'] = 'Not useful or not giving too much information'
            Pop_en['defind_cancer_with_clusternd'] = 'Not useful or not giving too much information'
            useful = clusternd_sentences_en[1]
        model_en_useful = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        useful_embeddings_en = model_en_useful.encode(useful)
        #Normalize the embeddings to unit length
        Normalize_useful_embeddings_en = useful_embeddings_en / np.linalg.norm(useful_embeddings_en, axis=1, keepdims=True)
        clustering_useful_model_en = KMeans(n_clusters=3)
        clustering_useful_model_en.fit(Normalize_useful_embeddings_en)
        cluster_assignment_useful_en = clustering_useful_model_en.labels_
        clusternd_useful_sentences_en= {}
        for cluster_ID_en in range(clustering_useful_model_en.n_clusters):
            clusternd_useful_sentences_en[cluster_ID_en] = []
        for sentence_ID_en, cluster_ID_en in enumerate(cluster_assignment_useful_en):
            clusternd_useful_sentences_en[cluster_ID_en].append(useful[sentence_ID_en])
        def define_Cencer_with_clusternd(use_clusternd_sentences,n_clusters):
            data = pd.DataFrame()
            for i in range(n_clusters):
                point = []
                define_C =[]
                test = all_reddit_data[all_reddit_data['comments'].isin(use_clusternd_sentences[i])]
                test_cer = list(test['defind_cancer_with_nlp'])
                for j in range(len(test_cer)):
                    if test_cer[j] in cancer_names_en:
                        point.append(test_cer[j])
                if len(set(point)) == 0 :
                    for x in range(len(test_cer)):
                        define_C.append('Unable to identify/not sure if it is')
                elif len(set(point)) == 1 :
                    for x in range(len(test_cer)):
                        define_C.append(point[0])
                elif len(set(point)) > 1:
                    for x in range(len(test_cer)):
                        define_C.append('There is a chance of having more than 2 types of cancer')
                test['defind_cancer_with_clusternd'] = define_C
                data = pd.concat([data,test])
            return data
        define_Cencer_b = define_Cencer_with_clusternd(clusternd_useful_sentences_en,3)
        define_Cencer_b['cancer_clusternd'] = 'It may be useful or it may provide enough information.'
        usedata=pd.concat([Pop_en,define_Cencer_b])
        new_colgenden_en=[]
        list_genden_en=[]
        #เเบ่งเพศ
        Genden_en = {'Male':['dad', "father","stepfather","grandfather","great-grandfather",
        "husband","boyfriend","fiancé","son","stepson","grandson","great-grandson","brother",
        "half-brother","stepbrother","uncle","great-uncle","nephew","great-nephew",
        "father-in-law","stepfather-in-law","grandfather-in-law","son-in-law","stepson-in-law",
        "grandson-in-law","brother-in-law","half-brother-in-law","stepbrother-in-law","uncle-in-law",
        "great-uncle-in-law","nephew-in-law","great-nephew-in-law","godfather","stepfather",
        "godson","foster father","foster son","stepson","stepbrother","half-brother","great-uncle",
        "great-nephew","first cousin","second cousin","third cousin","father-in-law",
        "stepfather-in-law","grandfather-in-law","son-in-law","stepson-in-law","grandson-in-law",
        "brother-in-law","half-brother-in-law","stepbrother-in-law","uncle-in-law","great-uncle-in-law",
        "nephew-in-law","great-nephew-in-law"'he','him','his','boy'],
        'Female':["mother",'mom',"stepmother","grandmother","great-grandmother","wife",
        "girlfriend","fiancée","daughter","stepdaughter","granddaughter","great-granddaughter",
        "sister","half-sister","stepsister","aunt","great-aunt","niece","great-niece",
        "mother-in-law","stepmother-in-law","grandmother-in-law","daughter-in-law",
        "stepdaughter-in-law","granddaughter-in-law","sister-in-law",
        "half-sister-in-law","stepsister-in-law","aunt-in-law","great-aunt-in-law",
        "niece-in-law","great-niece-in-law","cousin-in-law","godmother","stepmother",
        "goddaughter","foster mother","foster daughter","stepdaughter","stepsister",
        "half-sister","great-aunt","great-niece","mother-in-law","stepmother-in-law","grandmother-in-law",
        "daughter-in-law","stepdaughter-in-law","granddaughter-in-law","sister-in-law",
        "half-sister-in-law","stepsister-in-law","aunt-in-law","great-aunt-in-law",
        "niece-in-law","great-niece-in-law",'she','her','hers','mommy','girl']}
        for i in range(len(list_token_red)):
            for j in range(len(Genden_en['Female'])):
                for k in range(len(list_token_red[i])):
                    if (list_token_red[i][k] == Genden_en['Male'][j]):
                        list_genden_en.append('Male')
                    elif(list_token_red[i][k] == Genden_en['Female'][j]):
                        list_genden_en.append('Female')
            genden_list_en =[]
            genden_list_en = list(OrderedDict.fromkeys(list_genden_en)) # ลบคำซ้ำ
            #-------------------------------------------------------------------
            list_define_genden_en = []
            if len(genden_list_en) > 0 :
                if len(genden_list_en) == 2:
                    list_define_genden_en.append('Both genders are told.')
                elif len(genden_list_en)==1:
                    list_define_genden_en.append(genden_list_en[0])
            elif len(genden_list_en)==0:
                list_define_genden_en.append('Unable to identify/not sure if it is')
            genden_list_de_en =[]
            genden_list_de_en = list(OrderedDict.fromkeys(list_define_genden_en))
            new_colgenden_en.append(genden_list_de_en[0])
        def detect_person_en(comment):
            # คำที่ใช้ตรวจสอบว่ามีใครเป็นคนอยู่ในความคิดเห็น
            other = ['you','your','we','they','he','she','him','her','it']
            myself = ['my','myself']
            for keyword in  myself:
                if keyword in comment:
                    return "Tell about your own experiences"
            for keyword in  other:
                if keyword in comment:
                    return "Tell other people's experiences"
            # หากไม่พบคำที่บ่งบอกถึงคน
            return "Didn't tell the experience"
        def detect_gender_other_en(comment):
            # คำที่บ่งบอกถึงเพศชาย
            male_keywords = ['he','him','dad', "father","stepfather","grandfather","great-grandfather","husband",
            "boyfriend","fiancé","son","stepson","grandson","great-grandson","brother","half-brother","stepbrother","uncle","great-uncle","nephew",
            "great-nephew","father-in-law","stepfather-in-law","grandfather-in-law","son-in-law","stepson-in-law","grandson-in-law","brother-in-law",
            "half-brother-in-law","stepbrother-in-law","uncle-in-law","great-uncle-in-law","nephew-in-law","great-nephew-in-law","godfather","stepfather",
            "godson","foster father","foster son","stepson","stepbrother","half-brother","great-uncle","great-nephew","first cousin","second cousin",
            "third cousin","father-in-law","stepfather-in-law","grandfather-in-law","son-in-law","stepson-in-law","grandson-in-law","brother-in-law",
            "half-brother-in-law","stepbrother-in-law","uncle-in-law","great-uncle-in-law","nephew-in-law",
            "great-nephew-in-law",'boy']
            # คำที่บ่งบอกถึงเพศหญิง
            female_keywords = ["mother",'mom',"stepmother",'girl',
            "grandmother","great-grandmother","wife","girlfriend","fiancée","daughter","stepdaughter",
            "granddaughter","great-granddaughter","sister","half-sister","stepsister","aunt","great-aunt","niece",
            "great-niece","mother-in-law","stepmother-in-law","grandmother-in-law","daughter-in-law","stepdaughter-in-law",
            "granddaughter-in-law","sister-in-law","half-sister-in-law","stepsister-in-law","aunt-in-law","great-aunt-in-law",
            "niece-in-law","great-niece-in-law","cousin-in-law","godmother","stepmother","goddaughter","foster mother","foster daughter","stepdaughter","stepsister",
            "half-sister","great-aunt","great-niece","mother-in-law","stepmother-in-law","grandmother-in-law","daughter-in-law","stepdaughter-in-law",
            "granddaughter-in-law","sister-in-law","half-sister-in-law","stepsister-in-law","aunt-in-law","great-aunt-in-law","niece-in-law","great-niece-in-law",'mommy','she','her']
            # ตรวจสอบคำในความคิดเห็น
            for keyword in male_keywords:
                if keyword in comment :
                    return "Male"
            for keyword in female_keywords:
                if keyword in comment:
                    return "Female"
            return "Gender not specified"
        k3=[]
        k4=[]
        for i in data['comments']:
            k3.append(detect_person_en(str(i)))
            if detect_person_en(str(i)) == "Tell about your own experiences":
                k4.append("Gender not specified")
            elif detect_person_en(str(i)) == "Tell other people's experiences":
                k4.append(detect_gender_other_en(str(i)))
            elif detect_person_en(str(i)) == "Didn't tell the experience":
                k4.append(detect_gender_other_en(str(i)))
        symptoms_colcan_en = []
        for i in range(len(list_token_red)):
            list_symptoms_en= []
            for j in range(len(list_token_red[i])):
                for k in cancer_symptoms_en:
                    for l in range(len(cancer_symptoms_en[k])):
                        if list_token_red[i][j] == cancer_symptoms_en[k][l]:
                            list_symptoms_en.append(cancer_symptoms_en[k][0])
            unique_list_symptoms_en = list(OrderedDict.fromkeys(list_symptoms_en))
            if len(unique_list_symptoms_en) > 0:
                symptoms_colcan_en.append(unique_list_symptoms_en)
            else :
                symptoms_colcan_en.append(['No symptoms identified'])
        all_reddit_data = usedata
        all_reddit_data['defind_Genden_with_nlp'] = new_colgenden_en
        all_reddit_data['defind_Genden_with_python'] = k4
        all_reddit_data['defind_exp_with_python'] = k3
        all_reddit_data['symptoms_colcan_en'] = symptoms_colcan_en
        label_symptoms_en=all_reddit_data['symptoms_colcan_en'].str.join(sep='*').str.get_dummies(sep='*')
        all_reddit_data = all_reddit_data.join(label_symptoms_en)
        all_reddit_data.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
    # app1 = dash.Dash(requests_pathname_prefix="/app1/")
    df = pd.read_csv('data_pre.csv')
    sorue_sym_4 = pd.read_csv('soure_url.csv')
    soure = sorue_sym_4['url'][0]
    df = df.reset_index()
    if soure == 'www.facebook.com':
    # เพศ/ประสบการณ์/
        df['count_plot'] = 1
    #โรค
        df_can = df[['count_plot','โรค']].groupby(['โรค']).sum().reset_index()
        df_can = df_can[df_can['โรค']!= 'ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น']
    # อาการ
        last_10_columns = df.iloc[:, 13:-1]
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
    elif soure == 'www.reddit.com':
    # เพศ/ประสบการณ์/
        df['count_plot'] = 1
    #โรค
        df_can = df[['count_plot','defind_cancer_with_nlp']].groupby(['defind_cancer_with_nlp']).sum().reset_index()
        df_can = df_can #[df_can['defind_cancer_with_nlp']!= 'Unable to identify / not sure if it is']
    # อาการ
        last_10_columns = df.iloc[:, 10:-1]
        last_10_columns
        dfm = last_10_columns.melt()
        plot_df = (
            pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
        )
        plot_data=plot_df['มีการเล่า'].reset_index()
        plot_sym=plot_data # [plot_data['variable'] != 'ไม่มีการระบุอาการ']
        app1.layout = [
            html.Div(children='My First App with Data'),
            dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.bar(df_can, x='defind_cancer_with_nlp', y='count_plot')),
            dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_exp_with_python')),
            dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_Genden_with_nlp')),
            dcc.Graph(figure=px.histogram(plot_sym, x='variable', y='มีการเล่า', histfunc='avg')),
        ]
    return render_template('login2.html')

@server.route('/page3_2.py',methods=["POST","GET"])
def index_3():
    df = pd.read_csv('data_pre.csv')
    sorue_sym_4 = pd.read_csv('soure_url.csv')
    soure = sorue_sym_4['url'][0]
    df = df.reset_index()
    if soure == 'www.facebook.com':
    # เพศ/ประสบการณ์/
        df['count_plot'] = 1
    #โรค
        df_can = df[['count_plot','โรค']].groupby(['โรค']).sum().reset_index()
        df_can = df_can[df_can['โรค']!= 'ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น']
    # อาการ
        last_10_columns = df.iloc[:, 13:-1]
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
    elif soure == 'www.reddit.com':
    # เพศ/ประสบการณ์/
        df['count_plot'] = 1
    #โรค
        df_can = df[['count_plot','defind_cancer_with_nlp']].groupby(['defind_cancer_with_nlp']).sum().reset_index()
        df_can = df_can #[df_can['defind_cancer_with_nlp']!= 'Unable to identify / not sure if it is']
    # อาการ
        last_10_columns = df.iloc[:, 10:-1]
        last_10_columns
        dfm = last_10_columns.melt()
        plot_df = (
            pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
        )
        plot_data=plot_df['มีการเล่า'].reset_index()
        plot_sym=plot_data # [plot_data['variable'] != 'ไม่มีการระบุอาการ']
        app1.layout = [
            html.Div(children='My First App with Data'),
            dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(figure=px.bar(df_can, x='defind_cancer_with_nlp', y='count_plot')),
            dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_exp_with_python')),
            dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_Genden_with_nlp')),
            dcc.Graph(figure=px.histogram(plot_sym, x='variable', y='มีการเล่า', histfunc='avg')),
        ]
    return render_template('login2.html')

@server.route('/page2_2.py',methods=["POST","GET"])
def index_4():
    soure_b = pd.read_csv('soure_url.csv')
    soure = soure_b['url'][0]
    if soure == 'www.facebook.com':
        data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
        def sort_data(column_name):
            if column_name == 'like':
                data.sort_values('like', inplace=True, ascending=False)
            elif column_name == 'การตอบกลับ':
                data.sort_values('rechat', inplace=True, ascending=False)
            elif column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
        # number_of_rows = len(data)
        # number_of_columns = len(data.columns) 
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['name_cancarTH'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
    elif soure == 'www.reddit.com':
        data =  pd.read_csv("data_commentsred_docter.csv")
        def sort_data(column_name):
            if column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=False)
            else:
                pass
            return data
        sort_options = ['ความยาวของความคิดเห็น'] 
        data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
        name_can = data_cancer['cancer_names_en'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
    descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
    descriptive = descriptive.iloc[:, 1:]
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
    sorted_data = sort_data('like')
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    return render_template('output2.html', tables=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server},
)

if __name__ == '__main__':
    run_simple("localhost", 8050, application)


#========================================================================================================================
# @server.route('/test.py', methods=['POST','GET'])
# def test():
#     max_v = []
#     min_v = []
#     avg_v = []
#     _ = ['like','จำนวนการตอบกลับ','ความยาว']
#     data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
#     for i in range(len(data.columns)):
#         if i >= 2:
#             max_v.append(max(data[data.columns[i]].tolist()))
#             min_v.append(min(data[data.columns[i]].tolist()))
#             avg_v.append(np.mean(data[data.columns[i]].tolist()))
#     descriptive = pd.DataFrame()
#     descriptive[' '] = _
#     descriptive['max'] = max_v
#     descriptive['min'] = min_v
#     descriptive['avg'] = avg_v
#     tables = descriptive.to_html(classes='table table-striped', index=False)
#     return render_template('output.html', tables=[tables], titles=data.columns.values, number_of_rows=data.shape[0], number_of_columns=data.shape[1])
# app1 = dash.Dash(requests_pathname_prefix="/app1/")
# df = pd.read_csv('data_pre.csv')
# sorue_sym_4 = pd.read_csv('soure_url.csv')
# soure = sorue_sym_4['url'][0]
# df = df.reset_index()
# if soure == 'www.facebook.com':
#     # เพศ/ประสบการณ์/
#     df['count_plot'] = 1
#     #โรค
#     df_can = df[['count_plot','โรค']].groupby(['โรค']).sum().reset_index()
#     df_can = df_can[df_can['โรค']!= 'ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น']
#     # อาการ
#     last_10_columns = df.iloc[:, 12:-1]
#     last_10_columns
#     dfm = last_10_columns.melt()
#     plot_df = (
#         pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
#     )
#     plot_data=plot_df['มีการเล่า'].reset_index()
#     plot_sym=plot_data[plot_data['variable'] != 'ไม่มีการระบุอาการ']
#     app1.layout = [
#         html.Div(children='My First App with Data'),
#         dash_table.DataTable(data=df.to_dict('records'), page_size=10),
#         dcc.Graph(figure=px.bar(df_can, x='โรค', y='count_plot')),
#         dcc.Graph(figure=px.pie(df, values='count_plot', names='ใครเล่า')),
#         dcc.Graph(figure=px.pie(df, values='count_plot', names='เพศเเบ่งโดยใช้_python')),
#         dcc.Graph(figure=px.histogram(plot_sym, x='variable', y='มีการเล่า', histfunc='avg')),
#     ]
# elif soure == 'www.reddit.com':
#     # เพศ/ประสบการณ์/
#     df['count_plot'] = 1
#     #โรค
#     df_can = df[['count_plot','defind_cancer_with_nlp']].groupby(['defind_cancer_with_nlp']).sum().reset_index()
#     df_can = df_can[df_can['defind_cancer_with_nlp']!= 'ไม่สามารถระบุได้/ไม่มั่นใจว่าเป็น']
#     # อาการ
#     last_10_columns = df.iloc[:, 12:-1]
#     last_10_columns
#     dfm = last_10_columns.melt()
#     plot_df = (
#         pd.crosstab(dfm['variable'], dfm['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})
#     )
#     plot_data=plot_df['มีการเล่า'].reset_index()
#     plot_sym=plot_data[plot_data['variable'] != 'ไม่มีการระบุอาการ']
#     app1.layout = [
#         html.Div(children='My First App with Data'),
#         dash_table.DataTable(data=df.to_dict('records'), page_size=10),
#         dcc.Graph(figure=px.bar(df_can, x='defind_cancer_with_nlp', y='count_plot')),
#         dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_exp_with_python')),
#         dcc.Graph(figure=px.pie(df, values='count_plot', names='defind_Genden_with_nlp')),
#         dcc.Graph(figure=px.histogram(plot_sym, x='variable', y='มีการเล่า', histfunc='avg')),
#     ]