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

server = Flask(__name__,static_folder=os.path.join(os.getcwd(),'static'))
app1 = dash.Dash(requests_pathname_prefix="/app1/",prevent_initial_callbacks=True)

@server.route('/', methods=['GET'])
# ส่วนของหน้าที่ 1 สำหรับ input url ใช้ประกอบกับ HTML
def index_A():
  return render_template('pagr_1_NEW.html')

@server.route('/url_sc', methods=['GET','POST'])
# ส่วนของหน้าที่ 1 สำหรับ input url ใช้ประกอบกับ HTML
def index_B():
  return render_template('Page1_pro1.html')

@server.route('/use_File', methods=['GET','POST'])
# ส่วนของหน้าที่ 1 สำหรับ input url ใช้ประกอบกับ HTML
def index_C():
  return render_template('Page 2 use_file.html')
# ส่วนของหน้าที่ 1 สำหรับการดึงข้อมูลมาเก็บเป็นตาราง เเละให้เเสดงผลหน้าที่ 2 โดยให้เเสดงตารางข้อมูล,ค่าสถิติเบื้องต้น,word cloud,เเละการใส่อาการ ใช้ร่วมกับ HTML ด้วย
# ปล. ตัวกรอกอาการเป็น tag ต่างๆใช้html(เขียนเอง),jqurry(เขียนเอง) เเละ css(สำเร็จรูป)
@server.route('/process.py', methods=['POST'])
def process():
    import pandas as pd
    # ส่วนของการเก็บข้อมูลจาก advance option
    url = request.form['url']
    x_1 = request.form['x']
    a_1 = request.form['a']
    aoa_1 =request.form['aoa']
    r_1 = request.form['r']
    flie_name = 'Data_scraper'
    # ส่วนของการเก็บข้อมูล ว่าเราดึงจากเว็ปไหน เช่น ดึงจากFacebook ก็จะเป็น www.Facebook.com
    url_chack = str(url).split('/')[2]
    data_soure_a = {'url':[url_chack]}
    data_soure_b = pd.DataFrame(data_soure_a)
    data_soure_b.to_csv('soure_url.csv',index=False)
    # ดึงข้อมูลจาก facebook
    if url_chack == 'www.facebook.com':
        option = Options()
        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        # โดยปกติเวลาเราเข้าหน้าเว็ปที่มีการขอข้อมูลจะมีการเด้ง "popup" ให้เรากดยอมรับ(allow)หรือปิดกัน(block)
        option.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )
        # โดยปกติเวลาเราเข้า facebook ผ่าน webdriver Chrome มันจะไม่มีการ login Facebook ให้เเละหากไม่login 
        # Facebook เองก็จะพยายามให้เรา login ส่งผลให้เราติดที่หน้าlogin
        # code ด้านล่างนี้ก็จะเป็นส่วนของการ auto_login ผ่านข้อมูล ชื่อเเละรหัสผ่านในไฟล์ facebook_credentials.txt
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
        x=x_1
        a=int(x[162:164])
        k=x

        aoa=aoa_1
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
                a+=int(a_1)
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
                r += int(r_1)
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
        data_like=pd.DataFrame(data={'like':like_count})
        data_count=pd.DataFrame(data={'count':count})
        # ทำตาราง
        data = data_comment
        data = data.join(data_name).fillna('NaN_name')
        data = data.join(data_rechat).fillna(0)
        data = data.join(data_like).fillna(0)
        data = data.join(data_count).fillna(0)
        data = data.iloc[:,[1,0,3,2,4]]
        number_of_rows = len(data)
        number_of_columns = len(data.columns)
        data.to_csv(f'{flie_name}.csv', index=False, encoding='utf-8-sig')
        browser.close() 
        
    # reddit
    elif url_chack == 'www.reddit.com':
        import pandas as pd
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
        data.to_csv(f'{flie_name}.csv', index=False, encoding='utf-8-sig')
        driver.close() 
    filename = f'{flie_name}.csv'
    return  render_template('Page 2 use_url.html',name = filename)

@server.route('/return-files/',methods=['POST','GET'])
def return_files_tut():
    df = pd.read_csv('Data_scraper.csv', encoding='utf-8-sig')
    resp = make_response(df.to_csv(index=False, encoding='utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=Data_scraper.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.secret_key = secrets.token_urlsafe(16)
@server.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
 
        # Extracting uploaded file name
        data_filename =  secure_filename(f.filename)
 
        f.save(os.path.join(server.config['UPLOAD_FOLDER'],
                            data_filename))

        session['uploaded_data_file_path'] =os.path.join(server.config['UPLOAD_FOLDER'],data_filename)
        url_chack = request.form['language']
        data_soure_a = {'url':[url_chack]}
        data_soure_b = pd.DataFrame(data_soure_a)
        data_soure_b.to_csv('soure_url.csv',index=False)
        return render_template('Page 2 use_file_after.html')
    return render_template("Page 2 use_file.html")

@server.route('/after_pepar', methods = ['POST','GET'])   
def success():   
    import pandas as pd
    try:   
        data_file_path = session.get('uploaded_data_file_path', None)
        data= pd.read_csv(data_file_path,encoding='utf-8-sig')
    except:
        data = pd.read_csv('Data_scraper.csv')
    count_user = len(set(data['name']))
    count_comment = len(set(data['comments']))
    number_of_rows = len(data)
    number_of_columns = len(data.columns)
    sorue_sym_2 = pd.read_csv('soure_url.csv')
    sorue = sorue_sym_2['url'][0]
    if sorue == 'www.facebook.com':
        data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
        data_defind = data_sy_na[['name_cancarTH','Key_symptoms_TH','Values_symptoms_TH']]
        data_defind = data_defind.rename(columns={'name_cancarTH': 'name_cancarTH_se'})
        data_defind.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
    elif sorue == 'www.reddit.com':
        data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
        data_defind = data_sy_na[['cancer_names_en','Key_symptoms_EN','Valuessymptoms_EN']]
        data_defind=data_defind.rename(columns={'cancer_names_en': 'cancer_names_en_se'})
        data_defind.to_csv('all_data_nameandsym.csv')
    sorue_sym_3 = pd.read_csv('soure_url.csv')
    sorue = sorue_sym_3['url'][0]
    if sorue == 'www.facebook.com':
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
        for i in range(len(comment)):#len(comment)
            text= comment['คำพูดโรค'][i]
            custom_tokenizer = Tokenizer(words)
            Token = custom_tokenizer.word_tokenize(normalize(str(text)))
            Token.append('end')
            list_token.append(Token)
        comment['token'] = list_token
        comment.to_csv('data_tokenizer.csv',encoding='utf-8-sig')
        time.sleep(8)
        #หาโรค
        #--------------------------------------------------------
        new_colcan = []
        for i in range(len(list_token)):#len(comment)
            list_cancer = []
            for k in range(len(list_token[i])):
                if (list_token[i][k] == "มะเร็ง")|(list_token[i][k] == "โรคมะเร็ง")|(list_token[i][k] == "โรค"):
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
        #หาว่ามีประโยชน์หรือไม่มีประโยชน์
        use_ful_data =[]
        for i in range(len(list_token)):
            if len(list_token[i]) >= 50:
                use_ful_data.append('อาจมีประโยชน์')
            else :
                use_ful_data.append('ไม่มีประโยชน์')
        Data_pre_and_clane = comment
        Data_pre_and_clane['โรค'] = new_colcan
        Data_pre_and_clane['ความมีประโยชน์'] = use_ful_data
        Data_pre_and_clane['ใครเล่า'] = k1
        Data_pre_and_clane['เพศเเบ่งโดยใช้_nlp'] = new_colgenden
        Data_pre_and_clane['เพศเเบ่งโดยใช้_python'] = k2
        Data_pre_and_clane['อาการ']=symptoms_colcan
        label_symptoms=Data_pre_and_clane['อาการ'].str.join(sep='*').str.get_dummies(sep='*')
        Data_pre_and_clane=Data_pre_and_clane.join(label_symptoms)
        Data_pre_and_clane.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
        data_show = Data_pre_and_clane.iloc[:,:5]
    elif sorue == 'www.reddit.com':
        import pandas as pd 
        # ระบุโรค
        name_cancar_and_symptoms_pd = pd.read_csv('all_data_nameandsym.csv')
        name_cancar_list  = name_cancar_and_symptoms_pd['cancer_names_en_se'].tolist()
        cancer_names_en = [item for item in name_cancar_list if not(pd.isnull(item)) == True]
        # ระบุอาการ
        symptoms_pd = name_cancar_and_symptoms_pd[['Key_symptoms_EN','Valuessymptoms_EN']].dropna()
        data_k_list = symptoms_pd['Key_symptoms_EN'].tolist()
        data_V_list = symptoms_pd['Valuessymptoms_EN'].tolist()
        # ระบุโรคเเละอาการในรูป lower
        cancer_symptoms_en = {}
        for list_item in range(len(data_V_list)):
            split_t = ast.literal_eval(data_V_list[list_item])
            split_t = [n.strip() for n in split_t]
            cancer_symptoms_en[data_k_list[list_item]]=split_t
        data_raddit=data.groupby('name').sum().reset_index()
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
        data_com = data_raddit['comments'].to_list()
        list_token_red = []
        for item_comment_red in range(len(data_com)):
            data_r_token = token(data_com[item_comment_red].translate(str.maketrans('', '', string.punctuation)))
            data_r_token = remove_(data_r_token)
            data_r_token = lemma(data_r_token)
            list_token_red.append(data_r_token)
        data_raddit['token'] = list_token_red
        data_raddit.to_csv('data_tokenizer.csv',encoding='utf-8-sig')
        column_cancer_nlp_rad=[]
        for list_token_i in range(len(list_token_red)):#len(comment)
            list_cancer_en = []
            for list_token_k in range(len(list_token_red[list_token_i])):
                if (list_token_red[list_token_i][list_token_k] == 'cancer'):
                    list_cancer_en.append(list_token_red[list_token_i][list_token_k-1]+' '+list_token_red[list_token_i][list_token_k])
            unique_list_en = list(OrderedDict.fromkeys(list_cancer_en))

        #----------------------------------------------------------------------------
            list_define_cancer_en = []
            for i in range(len(unique_list_en)):
                for j in range(len(cancer_names_en)):
                    if unique_list_en[i]==cancer_names_en[j]:
                        list_define_cancer_en.append(unique_list_en[i])
        #----------------------------------------------------------------------------
            cancer_list_de_red =[]
            if len(list_define_cancer_en) > 0:
                if len(list_define_cancer_en) == 2:
                    cancer_list_de_red.append('Tell more than 2 diseases.')
                elif len(list_define_cancer_en)==1:
                    cancer_list_de_red.append(list_define_cancer_en[0])
            elif list_define_cancer_en==[]:
                cancer_list_de_red.append('Unable to identify / not sure if it is')
            if len(cancer_list_de_red)> 0 :
                column_cancer_nlp_rad.append(cancer_list_de_red[0])
            elif len(cancer_list_de_red)== 0 :
                column_cancer_nlp_rad.append('Unable to identify / not sure if it is')
        #-----------------------------------
        all_reddit_data = data_raddit
        all_reddit_data['defind_cancer_with_nlp'] = column_cancer_nlp_rad
        #-----------------------------------
        data_value_red =[]
        for i in range(len(list_token_red)):
            if len(list_token_red[i]) >= 50 :
                data_value_red.append('maybe_useful')
            else:
                data_value_red.append('Not useful or not giving too much information')
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
        for i in data_raddit['comments']:
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
        all_reddit_data['defind_Genden_with_nlp'] = new_colgenden_en
        all_reddit_data['defind_Genden_with_python'] = k4
        all_reddit_data['defind_exp_with_python'] = k3
        all_reddit_data['use_ful'] = data_value_red
        all_reddit_data['symptoms_colcan_en'] = symptoms_colcan_en
        label_symptoms_en=all_reddit_data['symptoms_colcan_en'].str.join(sep='*').str.get_dummies(sep='*')
        all_reddit_data = all_reddit_data.join(label_symptoms_en)
        all_reddit_data.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
        data_show = all_reddit_data.iloc[:,:3]
    sorue_sym_4 = pd.read_csv('soure_url.csv')
    sorue_chack = sorue_sym_4['url'][0]
    if sorue_chack == 'www.facebook.com': 
        _ = ['จำนวนคนตอบกลับ','จำนวนคนกด like','จำนวนความยาวตัวอักษร']
        data = Data_pre_and_clane
        def sort_data(column_name,how_sort):
            if column_name == 'จำนวนคนกด like':
                data_show.sort_values('like', inplace=True, ascending=how_sort)
            elif column_name == 'จำนวนคนตอบกลับ':
                data_show.sort_values('rechat', inplace=True, ascending=how_sort)
            elif column_name == 'จำนวนความยาวตัวอักษร':
                data_show.sort_values('count', inplace=True, ascending=how_sort)
            else:
                pass
            return data_show
        sort_options = ['จำนวนคนกด like', 'จำนวนคนตอบกลับ', 'จำนวนความยาวตัวอักษร']
        mylist_name_can = data['โรค'].to_list()
        name_can  = list(dict.fromkeys(mylist_name_can))
        sym_list = data.columns
        symptoms_can = sym_list[13:]
        data_name_sym_have = pd.DataFrame()
        data_value_TH = pd.DataFrame(data={'name_cancarTH':name_can})
        data_symptoms_TH = pd.DataFrame(data={'Key_symptoms_TH':symptoms_can})
        list_100 = list(range(0,100))
        data_name_sym_have['index'] = list_100
        data_name_sym_have = data_name_sym_have.merge(data_value_TH.reset_index(), how='outer')
        data_name_sym_have = data_name_sym_have.merge(data_symptoms_TH.reset_index(), how='outer')
        data_name_sym_have.to_csv('data_name_sym_have.csv',encoding='utf-8-sig')
        #------word cloud---------#
        from pythainlp.tokenize import word_tokenize as to_th_k # เป็นตัวตัดคำของภาษาไทย
        from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย
        text_th= ''
        for row in data['คำพูดโรค']: # ให้ python อ่านข้อมูลรีวิวจากทุก row ใน columns 'content'
            text_th = text_th + row.lower() + ' ' # เก็บข้อมูลรีวิวของเราทั้งหมดเป็น String ในตัวแปร text

        wt_th = to_th_k(text_th, engine='newmm') # ตัดคำที่ได้จากตัวแปร text

        path_th = 'THSarabunNew-20240628T045147Z-001\THSarabunNew\THSarabunNew.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
        wordcloud_th = WordCloud(font_path = path_th, # font ที่เราต้องการใช้ในการแสดงผล เราเลือกใช้ THSarabunNew
                            stopwords = thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                            relative_scaling = 0.3,
                            min_font_size = 1,
                            background_color = "white",
                            width=620,
                            height=300,
                            max_words = 500, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                            colormap = 'plasma',
                            scale = 3,
                            font_step = 4,
                            collocations = False,
                            regexp = r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                            margin=2).generate(' '.join(wt_th)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

        wordcloud_th.to_file("wordcloud.png")
        max_v = []
        min_v = []
        avg_v = []
        for i in range(len(data_show.columns)):
            if i >= 2 :
                max_v.append(max(data_show[data_show.columns[i]].tolist()))
                min_v.append(min(data_show[data_show.columns[i]].tolist()))
                avg_v.append(np.mean(data_show[data_show.columns[i]].tolist()))
        descriptive = pd.DataFrame()
        descriptive[' '] = _
        descriptive['max'] = max_v
        descriptive['min'] = min_v
        descriptive['avg'] = avg_v
        descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
        sorted_data = sort_data('จำนวนคนกด like',False)
    elif sorue_chack == 'www.reddit.com':
        import pandas as pd
        from nltk.tokenize import word_tokenize as to_en
        from nltk.stem import WordNetLemmatizer
        data = all_reddit_data
        _ = ['จำนวนความยาวตัวอักษร']
        def sort_data(column_name,how_sort):
            if column_name == 'ความยาวของความคิดเห็น':
                data_show.sort_values('count', inplace=True, ascending=how_sort)
            else:
                pass
            return data_show
        sort_options = ['ความยาวของความคิดเห็น']
        mylist_name_can = data['defind_cancer_with_nlp'].to_list()
        name_can  = list(dict.fromkeys(mylist_name_can))
        symptoms_can = data.columns[10:]
        data_name_sym_have = pd.DataFrame()
        data_value_TH = pd.DataFrame(data={'cancer_names_en':name_can})
        data_symptoms_TH = pd.DataFrame(data={'Key_symptoms_EN':symptoms_can})
        list_100 = list(range(0,100))
        data_name_sym_have['index'] = list_100
        data_name_sym_have = data_name_sym_have.merge(data_value_TH.reset_index(), how='outer')
        data_name_sym_have = data_name_sym_have.merge(data_symptoms_TH.reset_index(), how='outer')
        data_name_sym_have.to_csv('data_name_sym_have.csv',encoding='utf-8-sig')
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
            width=620,
            height=300,
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
        for i in range(len(data_show.columns)):
            if i == 2:
                max_v.append(max(data_show[data_show.columns[i]].tolist()))
                min_v.append(min(data_show[data_show.columns[i]].tolist()))
                avg_v.append(np.mean(data_show[data_show.columns[i]].tolist()))
        descriptive = pd.DataFrame()
        descriptive[' '] = _
        descriptive['max'] = max_v
        descriptive['min'] = min_v
        descriptive['avg'] = avg_v
        descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
        sorted_data = sort_data('ความยาวของความคิดเห็น',False)
    descriptive =pd.read_csv('data_desc.csv')
    descriptive = descriptive.iloc[:, 1:]
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # เรียงลำดับข้อมูลตามค่าเริ่มต้น (like)
    sorted_data.to_csv('sorted_data.csv',encoding='utf-8-sig')
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    return  render_template('output2.html',tables=[tables],sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d] ,count_user = count_user,count_comment=count_comment,number_of_rows=number_of_rows
                           ,number_of_columns=number_of_columns)     
    



@server.route('/sort', methods=['POST','GET'])
def sort():
    soure_b = pd.read_csv('soure_url.csv')
    soure = soure_b['url'][0]
    data = pd.read_csv("sorted_data.csv", encoding='utf-8-sig')
    data = data.iloc[:,1:]
    number_of_rows = len(data)
    number_of_columns = len(data.columns)
    count_user = len(set(data.iloc[:,0]))
    count_comment = len(set(data.iloc[:,1]))
    if soure == 'www.facebook.com':
        def sort_data(column_name,how_sort):
            if column_name == 'like':
                data.sort_values('like', inplace=True, ascending=how_sort)
            elif column_name == 'การตอบกลับ':
                data.sort_values('rechat', inplace=True, ascending=how_sort)
            elif column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=how_sort)
            else:
                pass
            return data
        sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
        data_cancer= pd.read_csv('data_name_sym_have.csv')
        name_can = data_cancer['name_cancarTH'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
    elif soure == 'www.reddit.com':
        def sort_data(column_name,how_sort):
            if column_name == 'ความยาวของความคิดเห็น':
                data.sort_values('count', inplace=True, ascending=how_sort)
            else:
                pass
            return data
        sort_options = ['ความยาวของความคิดเห็น']
        data_cancer= pd.read_csv('data_name_sym_have.csv')
        name_can = data_cancer['cancer_names_en'].dropna().to_list()
        symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
    descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
    descriptive = descriptive.iloc[:, 1:]
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # รับค่าคอลัมน์ที่เลือกจาก dropdownlist
    column_name = request.form['sort_column']
    how_sort_clk = request.form['HOW']
    if how_sort_clk == 'มากไปน้อย' :
        how_sort = False
    elif how_sort_clk == 'น้อยไปมาก':
        how_sort = True
    # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
    sorted_data = sort_data(column_name,how_sort)
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('output2.html', tables=[tables], sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d],number_of_rows=number_of_rows,number_of_columns=number_of_columns,count_user = count_user,count_comment=count_comment)

@server.route('/wordcloud.png')
def wordcloud():
    return send_from_directory('.', 'wordcloud.png')
#number_of_rows=number_of_rows, number_of_columns=number_of_columns,

@server.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    #========================================== ส่วนตัวรับข้อมูลเพิ่ม/ลด โรคเเละอาการ ======================================
    if request.method == 'POST':
        # ข้อมูลที่ได้รับจากการกรอง
        import pandas as pd
        skill = request.form['skill']
        symptom  = request.form['symptom']
        sum_ch = request.form['sum_ch'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        soure_b = pd.read_csv('soure_url.csv')
        soure = soure_b['url'][0]
        if name_cancer ==[''] or name_cancer == [] or name_cancer is None :
            if soure == 'www.facebook.com':
                data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
                data_defind = data_sy_na[['name_cancarTH']]
                name_cancer = data_defind['name_cancarTH'].to_list()
            elif soure == 'www.reddit.com':
                data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
                data_defind = data_sy_na[['cancer_names_en']]
                cancer_names_en = data_defind['cancer_names_en'].to_list()
        if name_symptom ==[''] or name_symptom == [] or name_symptom is None :
            if soure == 'www.facebook.com':
                data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
                data_defind = data_sy_na[['Key_symptoms_TH']]
                name_symptom = data_defind['Key_symptoms_TH'].to_list()
            elif soure == 'www.reddit.com':
                data_sy_na = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
                data_defind = data_sy_na[['Key_symptoms_EN']]
                data_k_list = data_defind['Key_symptoms_EN'].to_list()
        # ข้อมูลอาการเพิ่มเติม
        # c_submit= request.form['custId']
        if soure == 'www.facebook.com':
            data_defu = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
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
            data_defu = pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
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
        all_data.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
        sorue = soure
        #===================================================================================================
        # update ตาราง 
        if sorue == 'www.facebook.com':
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
        #====================================================================================================
            #เเปลงหัวตาราง
            data = pd.read_csv('data_tokenizer.csv', encoding='utf-8-sig')
            comment=data.groupby('ชื่อ').sum().reset_index()
            comment = comment.drop(['Unnamed: 0'], axis=1)
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
            #หาว่ามีประโยชน์หรือไม่มีประโยชน์
            use_ful_data =[]
            for i in range(len(list_token)):
                if len(list_token[i]) >= 50:
                    use_ful_data.append('อาจมีประโยชน์')
                else :
                    use_ful_data.append('ไม่มีประโยชน์')
            Data_pre_and_clane = comment
            Data_pre_and_clane['โรค'] = new_colcan
            Data_pre_and_clane['ความมีประโยชน์'] = use_ful_data
            Data_pre_and_clane['ใครเล่า'] = k1
            Data_pre_and_clane['เพศเเบ่งโดยใช้_nlp'] = new_colgenden
            Data_pre_and_clane['เพศเเบ่งโดยใช้_python'] = k2
            Data_pre_and_clane['อาการ']=symptoms_colcan
            label_symptoms=Data_pre_and_clane['อาการ'].str.join(sep='*').str.get_dummies(sep='*')
            Data_pre_and_clane=Data_pre_and_clane.join(label_symptoms)
            Data_pre_and_clane.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
        elif sorue == 'www.reddit.com':
            import pandas as pd
            data = pd.read_csv('data_tokenizer.csv', encoding='utf-8-sig')
            count_user = len(set(data['name']))
            count_comment = len(set(data['comments']))
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
            data_raddit=data.groupby('name').sum().reset_index()
            data_raddit = data_raddit.drop(['Unnamed: 0'], axis=1)
            list_token_red = []
            for i in range(len(data_raddit['token'])):
                list_token_red.append(ast.literal_eval(data_raddit['token'][i]))
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
            all_reddit_data = data_raddit
            all_reddit_data['defind_cancer_with_nlp'] = column_cancer_nlp_rad
        #-----------------------------------
            data_value_red =[]
            for i in range(len(list_token_red)):
                if len(list_token_red[i]) >= 50 :
                    data_value_red.append('maybe_useful')
                else:
                    data_value_red.append('Not useful or not giving too much information')
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
            for i in data_raddit['comments']:
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
            all_reddit_data['defind_Genden_with_nlp'] = new_colgenden_en
            all_reddit_data['defind_Genden_with_python'] = k4
            all_reddit_data['defind_exp_with_python'] = k3
            all_reddit_data['use_ful'] = data_value_red
            all_reddit_data['symptoms_colcan_en'] = symptoms_colcan_en
            label_symptoms_en=all_reddit_data['symptoms_colcan_en'].str.join(sep='*').str.get_dummies(sep='*')
            all_reddit_data = all_reddit_data.join(label_symptoms_en)
            all_reddit_data.to_csv('data_pre.csv', index=False, encoding='utf-8-sig')
#======================================================================================================================
        if soure == 'www.facebook.com':
            all_data=pd.read_csv('all_data_nameandsym.csv')
            data_use=pd.read_csv('data_pre.csv')
            name_cancarTH_filter = all_data['name_cancarTH_se'].dropna().to_list()
            name_symptomsTH_filter = all_data['Key_symptoms_TH'].dropna().to_list()
            data_column_sym = data_use.columns[12:]
            for i in data_column_sym:
                if i not in name_symptomsTH_filter:
                    data_use.drop(i, axis=1, inplace=True)
            rows_to_drop = data_use[~data_use['โรค'].isin(name_cancarTH_filter)].index
            data_use.drop(rows_to_drop, axis=0, inplace=True)
        elif soure == 'www.reddit.com':
            #filter reddit
            all_data=pd.read_csv('all_data_nameandsym.csv')
            data_use=pd.read_csv('data_pre.csv')
            name_symptoms_filter_en = all_data['Key_symptoms_EN'].dropna().to_list()
            name_cancar_filter_en= all_data['cancer_names_en_se'].dropna().to_list()
            data_column_sym = data_use.columns[10:]
            for i in data_column_sym:
                if i not in name_symptoms_filter_en:
                    data_use.drop(i, axis=1, inplace=True)
            rows_to_drop = data_use[~data_use['defind_cancer_with_nlp'].isin(name_cancar_filter_en)].index
            data_use.drop(rows_to_drop, axis=0, inplace=True)
        data_use['sum_ch'] = sum_ch
        data_use.to_csv('data_pre_setting.csv', index=False, encoding='utf-8-sig')
#===========================================================================================================================
        sorue_sym_4 = pd.read_csv('soure_url.csv')
        sorue_chack = sorue_sym_4['url'][0]
        if sorue_chack == 'www.facebook.com': 
            _ = ['จำนวนคนตอบกลับ','จำนวนคนกด like','จำนวนความยาวตัวอักษร']
            data =  data_use
            data_show = data_use.iloc[:,:5]
            def sort_data(column_name,how_sort):
                if column_name == 'จำนวนคนกด like':
                    data_show.sort_values('like', inplace=True, ascending=how_sort)
                elif column_name == 'จำนวนคนตอบกลับ':
                    data_show.sort_values('rechat', inplace=True, ascending=how_sort)
                elif column_name == 'จำนวนความยาวตัวอักษร':
                    data_show.sort_values('count', inplace=True, ascending=how_sort)
                else:
                    pass
                return data_show
            sort_options = ['จำนวนคนกด like', 'จำนวนคนตอบกลับ', 'จำนวนความยาวตัวอักษร']
            mylist_name_can = data['โรค'].to_list()
            name_can  = list(dict.fromkeys(mylist_name_can))
            sym_list = data.columns
            symptoms_can = sym_list[12:]
            data_name_sym_have = pd.DataFrame()
            data_value_TH = pd.DataFrame(data={'name_cancarTH':name_can})
            data_symptoms_TH = pd.DataFrame(data={'Key_symptoms_TH':symptoms_can})
            list_100 = list(range(0,100))
            data_name_sym_have['index'] = list_100
            data_name_sym_have = data_name_sym_have.merge(data_value_TH.reset_index(), how='outer')
            data_name_sym_have = data_name_sym_have.merge(data_symptoms_TH.reset_index(), how='outer')
            data_name_sym_have.to_csv('data_name_sym_have.csv',encoding='utf-8-sig')
            #------word cloud---------#
            from pythainlp.tokenize import word_tokenize as to_th_k # เป็นตัวตัดคำของภาษาไทย
            from pythainlp.corpus import thai_stopwords # เป็นคลัง Stop Words ของภาษาไทย
            text_th= ''
            for row in data['คำพูดโรค']: # ให้ python อ่านข้อมูลรีวิวจากทุก row ใน columns 'content'
                text_th = text_th + row.lower() + ' ' # เก็บข้อมูลรีวิวของเราทั้งหมดเป็น String ในตัวแปร text

            wt_th = to_th_k(text_th, engine='newmm') # ตัดคำที่ได้จากตัวแปร text

            path_th = 'THSarabunNew-20240628T045147Z-001\THSarabunNew\THSarabunNew.ttf' # ตั้ง path ไปหา font ที่เราต้องการใช้แสดงผล
            wordcloud_th = WordCloud(font_path = path_th, # font ที่เราต้องการใช้ในการแสดงผล เราเลือกใช้ THSarabunNew
                                stopwords = thai_stopwords(), # stop words ที่ใช้ซึ่งจะโดนตัดออกและไม่แสดงบน words cloud
                                relative_scaling = 0.3,
                                min_font_size = 1,
                                background_color = "white",
                                width=620,
                                height=300,
                                max_words = 500, # จำนวนคำที่เราต้องการจะแสดงใน Word Cloud
                                colormap = 'plasma',
                                scale = 3,
                                font_step = 4,
                                collocations = False,
                                regexp = r"[ก-๙a-zA-Z']+", # Regular expression to split the input text into token
                                margin=2).generate(' '.join(wt_th)) # input คำที่เราตัดเข้าไปจากตัวแปร wt ในรูปแบบ string

            wordcloud_th.to_file("wordcloud.png")
            max_v = []
            min_v = []
            avg_v = []
            for i in range(len(data_show.columns)):
                if i >= 2 :
                    max_v.append(max(data_show[data_show.columns[i]].tolist()))
                    min_v.append(min(data_show[data_show.columns[i]].tolist()))
                    avg_v.append(np.mean(data_show[data_show.columns[i]].tolist()))
            descriptive = pd.DataFrame()
            descriptive[' '] = _
            descriptive['max'] = max_v
            descriptive['min'] = min_v
            descriptive['avg'] = avg_v
            descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
            sorted_data = sort_data('จำนวนคนกด like',False)
        elif sorue_chack == 'www.reddit.com':
            import pandas as pd
            from nltk.tokenize import word_tokenize as to_en
            from nltk.stem import WordNetLemmatizer
            data = all_reddit_data
            data_show = data_use.iloc[:,:3]
            _ = ['จำนวนความยาวตัวอักษร']
            def sort_data(column_name,how_sort):
                if column_name == 'ความยาวของความคิดเห็น':
                    data_show.sort_values('count', inplace=True, ascending=how_sort)
                else:
                    pass
                return data_show
            sort_options = ['ความยาวของความคิดเห็น']
            mylist_name_can = data['defind_cancer_with_nlp'].to_list()
            name_can  = list(dict.fromkeys(mylist_name_can))
            symptoms_can = data.columns[10:]
            data_name_sym_have = pd.DataFrame()
            data_value_TH = pd.DataFrame(data={'cancer_names_en':name_can})
            data_symptoms_TH = pd.DataFrame(data={'Key_symptoms_EN':symptoms_can})
            list_100 = list(range(0,100))
            data_name_sym_have['index'] = list_100
            data_name_sym_have = data_name_sym_have.merge(data_value_TH.reset_index(), how='outer')
            data_name_sym_have = data_name_sym_have.merge(data_symptoms_TH.reset_index(), how='outer')
            data_name_sym_have.to_csv('data_name_sym_have.csv',encoding='utf-8-sig')
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
                width=620,
                height=300,
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
            for i in range(len(data_show.columns)):
                if i == 2:
                    max_v.append(max(data_show[data_show.columns[i]].tolist()))
                    min_v.append(min(data_show[data_show.columns[i]].tolist()))
                    avg_v.append(np.mean(data_show[data_show.columns[i]].tolist()))
            descriptive = pd.DataFrame()
            descriptive[' '] = _
            descriptive['max'] = max_v
            descriptive['min'] = min_v
            descriptive['avg'] = avg_v
            descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
            sorted_data = sort_data('ความยาวของความคิดเห็น',False)
        descriptive =pd.read_csv('data_desc.csv')
        descriptive = descriptive.iloc[:, 1:]
        tables_d = descriptive.to_html(classes='table table-striped', index=False)
        # เรียงลำดับข้อมูลตามค่าเริ่มต้น (like)
        sorted_data.to_csv('sorted_data.csv',encoding='utf-8-sig')
        tables = sorted_data.to_html(classes='table table-striped', index=False)
        count_user = len(set(sorted_data.iloc[:,0]))
        count_comment = len(set(sorted_data.iloc[:,1]))
        number_of_rows = len(data)
        number_of_columns = len(data.columns)
            # for found in name_cancarTH_filter:
    return render_template('output2.html', tables=[tables], sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                    ,tables_descript=[tables_d],count_user=count_user,count_comment=count_comment,number_of_rows=number_of_rows,number_of_columns=number_of_columns)


@server.route('/page3.py',methods=["POST","GET"])
def index_2():
    sorue_sym_4 = pd.read_csv('soure_url.csv')
    soure = sorue_sym_4['url'][0]
    import dash_bootstrap_components as dbc
    if soure == 'www.facebook.com':
        try:
            data_for_dash_facebook = pd.read_csv('data_pre_setting.csv', encoding='utf-8-sig')
            data_for_dash_facebook.drop('sum_ch', axis=1, inplace=True)
        except:
            data_for_dash_facebook = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
        data_for_dash_facebook['count_plot'] = 1
        sym_o_th = data_for_dash_facebook.iloc[:, 13:-1]
        sym_o1_th = sym_o_th.melt()
        sym_o2_th = (pd.crosstab(sym_o1_th['variable'], sym_o1_th['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()

        app1.layout = html.Div([
            html.Div([
                dash_table.DataTable(id='datatable')
            ]),
        html.Div(
            [
            dbc.ModalHeader(dbc.Button("Print", id="grid-browser-print-btn")),
            dbc.ModalBody(
                # customize your printed report here
                [
                # exp
                html.Div([
                    html.P("แผนภูมิประสบการณ์กับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-exp-graph"),
                    html.P(id = 'text_sum_exp')],style={'width': '40%',  'display': 'inline-block'}),
                html.Div([
                    html.P("ประสบการณ์:"),
                    dcc.Checklist(id='pie-charts-exp-names',
                        options=data_for_dash_facebook['ใครเล่า'].unique(),
                        value=data_for_dash_facebook['ใครเล่า'].unique()),
                    ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                # Gender
                html.Div([
                    html.P("แผนภูมิเพศผู้ป่วยกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-Gender-graph"),
                    html.P(id = 'text_sum_Gender')],style={'width': '40%',  'display': 'inline-block'}),
                html.Div([
                    html.P("เพศ:"),
                    dcc.Checklist(id='pie-charts-Gender-names',
                        options=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique(),
                        value=data_for_dash_facebook['เพศเเบ่งโดยใช้_python'].unique()),
                        ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                    html.Br(style={"line-height": "5"}),
                # carcer
                html.Div([
                    html.P("โรค:"),
                    dcc.Dropdown(id='pie-charts-cancer-names',
                        options=data_for_dash_facebook['โรค'].unique(),
                        value=data_for_dash_facebook['โรค'].unique(),multi=True),
                    ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                html.Div([
                    html.P("แผนภูมิโรคกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="his-charts-carcer-graph"),
                    html.P(id = 'text_sum_cancer',style={'whiteSpace': 'pre-line'})],style={'width': '50%', 'display': 'inline-block'}),
                # useful
                html.Div([
                    html.P("แผนภูมิความมีประโยชน์กับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-useful-graph"),
                    html.P(id ="text_sum_useful")],style={'width': '40%',  'display': 'inline-block'}),
                html.Div([
                    html.P("ความมีประโยชน์:"),
                    dcc.Checklist(id="pie-charts-useful-names",
                        options=data_for_dash_facebook['ความมีประโยชน์'].unique(),
                        value=data_for_dash_facebook['ความมีประโยชน์'].unique()),
                    ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                    html.Br(style={"line-height": "5"}),
                # sym
                html.Div([
                    html.P("อาการ:"),
                    dcc.Dropdown(id='pie-charts-sym-names',
                        options=sym_o2_th['variable'].unique(),
                        multi=True)],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                html.Div([
                    html.P("แผนภูมิอาการกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="his-charts-sym-graph"),
                    html.P(id ="text_sum_sym",style={'whiteSpace': 'pre-line'})],style={'width': '50%','display': 'inline-block'}),
                # like
                html.Div([
                    html.P("แผนภูมิจำนวนยอดไลน์กับจำนวนความคิดเห็น"),
                    dcc.Graph(id="line-charts-like-graph"),
                    html.P(id ="text_sum_like",style={'whiteSpace': 'pre-line'})],style={'width': '55%','display': 'inline-block'}),
                html.Div([
                    html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
                    dcc.Slider(0, max(data_for_dash_facebook['count'].tolist()), max(data_for_dash_facebook['count'].tolist())/5,
                        value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
                        id='slider-count_word-names'),
                    ],style={'width': '20%', 'display': 'inline-block',"height": "100px","float":"left"}),
                # reply count
                html.Div([
                    html.P("แผนภูมิจำนวนการตอบกลับกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="line-charts-rechat-graph"),
                    html.P(id ="text_sum_reply",style={'whiteSpace': 'pre-line'})],style={'width': '55%','display': 'inline-block'}),
                html.Div([
                    html.P("จำนวนการตอบกลับ(ขั้นต่ำ):"),
                    dcc.Slider(0, max(data_for_dash_facebook['rechat'].tolist()), max(data_for_dash_facebook['rechat'].tolist())/5,
                        value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
                        id='slider-count_rechat-names'),
                    ],style={'width': '20%', 'display': 'inline-block',"height": "300px","float":"left"}),
                # word count
                html.Div([
                    html.P("แผนภูมิจำนวนตัวอักษรกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="line-charts-count_word-graph"),
                    html.P(id ="text_sum_word",style={'whiteSpace': 'pre-line'})],style={'width': '55%','display': 'inline-block'}),
                html.Div([
                    html.P("จำนวน like(ขั้นต่ำ):"),
                    dcc.Slider(0, max(data_for_dash_facebook['like'].tolist()), max(data_for_dash_facebook['like'].tolist())/5,
                        value=0,tooltip={"placement": "bottom", "always_visible": True},vertical=True,
                        id='slider-count_like-names'),
                    ],style={'width': '20%', 'display': 'inline-block',"height": "300px","float":"left"}),
                ],
                id="grid-print-area",
                ),
                html.Div(id="dummy"),
                ])
                ])
        @app1.callback(
            Output("pie-charts-exp-graph", "figure"),
            Output("pie-charts-Gender-graph", "figure"),
            Output("his-charts-carcer-graph", "figure"), 
            Output("pie-charts-useful-graph", "figure"),
            Output("his-charts-sym-graph", "figure"),
            Output("line-charts-like-graph", "figure"),
            Output("line-charts-rechat-graph", "figure"),
            Output("line-charts-count_word-graph", "figure"),
            Output("text_sum_exp", 'children'),
            Output("text_sum_Gender", 'children'),
            Output("text_sum_cancer", 'children'),
            Output("text_sum_useful", 'children'), 
            Output("text_sum_sym", 'children'),
            Output("text_sum_like", 'children'),
            Output("text_sum_reply", 'children'),
            Output("text_sum_word", 'children'),
            Output('datatable', 'data'), 
            Input("pie-charts-exp-names", "value"),
            Input("pie-charts-Gender-names", "value"),
            Input("pie-charts-cancer-names", "value"),
            Input("pie-charts-useful-names", "value"),
            Input("pie-charts-sym-names", "value"),
            Input("slider-count_like-names", "value"),
            Input("slider-count_rechat-names", "value"),
            Input("slider-count_word-names", "value"),
            prevent_initial_call=True,
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
            nms = nms[nms['ความมีประโยชน์'].isin(useful)]
            nms = nms[nms['like']>=count_like]
            nms = nms[nms['rechat']>=count_rechat]
            nms = nms[nms['count']>=count_word]
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
            fig_1 = px.pie(nms, values='count_plot', names=nms['ใครเล่า'],color_discrete_sequence=px.colors.sequential.Emrld)
            fig_2 = px.pie(nms, values='count_plot', names=nms['เพศเเบ่งโดยใช้_python'],color='เพศเเบ่งโดยใช้_python',color_discrete_map={'เพศชาย':'darkblue','เพศหญิง':"magenta",'ไม่ระบุเพศ':'gray'})
            fig_3 = px.histogram(nms, x=nms['โรค'], y='count_plot',barmode='group',text_auto=True)
            fig_4 = px.pie(nms, values='count_plot', names=nms['ความมีประโยชน์'],color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True)
            fig_6 = px.line(nms,x='ชื่อ', y='like')
            fig_7 = px.line(nms,x='ชื่อ', y='rechat')
            fig_8 = px.line(nms,x='ชื่อ', y='count')
            #สรุปกราฟประสบการณ์
            sum_all_exp = nms['ใครเล่า']
            sum_non_exp = nms[nms['ใครเล่า']=='ไม่ได้เล่าประสบการณ์']
            sum_other_exp = nms[nms['ใครเล่า']=='เล่าประสบการณ์คนอื่น']
            sum_self_exp = nms[nms['ใครเล่า']=='เล่าประสบการณ์ตัวเอง']
            value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
            value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
            value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
            text_1 = f'''ผลจากกราฟ ประสบการณ์กับความคิดเห็น พบว่าความคิดเห็นที่ไม่ได้เล่าประสบการณ์เกี่ยวกับโรคมีจำนวน {len(sum_non_exp)}ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
            { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก{len(sum_self_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
            if len(sum_other_exp) > len(sum_self_exp) else 
            f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
            #สรุปกราฟเพศ 
            sum_all_gen = nms['เพศเเบ่งโดยใช้_python']
            sum_female_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='เพศหญิง']
            sum_male_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='เพศชาย']
            sum_non_gen = nms[nms['เพศเเบ่งโดยใช้_python']=='ไม่ระบุเพศ']
            value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
            value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
            value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
            text_2 = f'''ผลจากกราฟ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
            { f"เพศชายจำนวน {len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_male_p_gen,2)} ในขณะที่อีก{len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
            if len(sum_male_gen) > len(sum_female_gen) else 
            f"เพศหญิงจำนวน {len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_female_p_gen,2)} ในขณะที่อีก{len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
            # สรุปกราฟโรค
            nms_can = nms[['โรค','count_plot']]
            nms_gro_cancer = nms_can.groupby('โรค').sum().reset_index().sort_values(by='count_plot',ascending=False)
            text_3 ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
            for fill in range(len(nms_gro_cancer)):
                p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
                text_3 = text_3 + f'\n- {nms_gro_cancer["โรค"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}'
            # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
            sum_all_useful = nms['ความมีประโยชน์']
            sum_have_useful = nms[nms['ความมีประโยชน์']=='อาจมีประโยชน์']
            sum_not_useful = nms[nms['ความมีประโยชน์']=='ไม่มีประโยชน์']
            value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
            value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
            text_4= f'''ผลจากกราฟ ความมีประโยชน์กับความคิดเห็น พบว่าส่วนมากเป็นความคิดเห็นที่
            {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_have_useful_p,2)} ในขณะที่อีก{len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
            if len(sum_have_useful) > len(sum_not_useful) else 
            f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_not_useful_p,2)} ในขณะที่อีก{len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
            text_5 ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
            for filler in range(len(plot_sym)):
                plot_sym_next = plot_sym.reset_index()
                text_5 = text_5 + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
            avg_11=nms['like'].mean()
            avg_22=nms['rechat'].mean()
            avg_33=nms['count'].mean()
            text_6 = f'''จากกราฟจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['like'].max()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ {nms['like'].min()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ {round(avg_11,2)}\n'''
            text_7= f'''จากกราฟจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['rechat'].max()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['rechat'].min()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_22,2)}\n'''
            text_8= f'''จากกราฟจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['count'].max()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['count'].min()}\n
                        ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_33,2)}\n'''
            data_for_export = dash_table.DataTable(nms.to_dict('records'), [{"name": i, "id": i} for i in nms.columns],export_format="csv")
            return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,fig_7,fig_8,text_1,text_2,text_3,text_4,text_5,text_6,text_7,text_8,data_for_export]
        app1.clientside_callback(
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
    elif soure == 'www.reddit.com':
        import dash_bootstrap_components as dbc
        try:
            data_for_dash_raddit= pd.read_csv('data_pre_setting.csv', encoding='utf-8-sig')
            data_for_dash_raddit.drop('sum_ch', axis=1, inplace=True)
        except:
            data_for_dash_raddit = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
        data_for_dash_raddit['count_plot'] = 1
        sym_o = data_for_dash_raddit.iloc[:, 10:-1]
        sym_o1 = sym_o.melt()
        sym_o2 = (pd.crosstab(sym_o1['variable'], sym_o1['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'})).reset_index()
        app1.layout = html.Div([
                html.Div([
                dbc.ModalHeader(dbc.Button("Print", id="grid-browser-print-btn")),
                dbc.ModalBody(
                # customize your printed report here
                [
                # exp
                html.Div([
                    html.P("แผนภูมิประสบการณ์กับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-exp-graph"),
                    html.P(id = 'text_sum_exp')],style={'width': '40%',  'display': 'inline-block'}),
                html.Div([
                        html.P("ประสบการณ์"),
                        # exp
                        dcc.Checklist(id='pie-charts-exp-names',
                            options=data_for_dash_raddit['defind_exp_with_python'].unique(),
                            value=data_for_dash_raddit['defind_exp_with_python'].unique()),
                        ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                # Gender
                html.Div([
                    html.P("แผนภูมิเพศผู้ป่วยกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-Gender-graph"),
                    html.P(id = 'text_sum_Gender')],style={'width': '40%',  'display': 'inline-block'}),
                html.Div([
                        html.P("เพศ"),
                        dcc.Checklist(id='pie-charts-Gender-names',
                            options=data_for_dash_raddit['defind_Genden_with_python'].unique(),
                            value=data_for_dash_raddit['defind_Genden_with_python'].unique()),
                        ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                        html.Br(style={"line-height": "5"}),
                # carcer
                html.Div([
                        html.P("โรค:"),
                        dcc.Dropdown(id='pie-charts-cancer-names',
                            options=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),
                            value=data_for_dash_raddit['defind_cancer_with_nlp'].unique(),multi=True),
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
                        dcc.Checklist(id="pie-charts-useful-names",
                            options=data_for_dash_raddit['use_ful'].unique(),
                            value=data_for_dash_raddit['use_ful'].unique()),
                        ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                        html.Br(style={"line-height": "5"}),
                # sym
                html.Div([
                        html.P("อาการ:"),
                        dcc.Dropdown(id='pie-charts-sym-names',
                            options=sym_o2['variable'].unique(),
                            multi=True),
                        ],style={'width': '29%', 'display': 'inline-block',"float":"left"}),
                html.Div([
                    html.P("แผนภูมิอาการกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-sym-graph"),
                    html.P(id ="text_sum_sym",style={'whiteSpace': 'pre-line'})],style={'width': '29%','display': 'inline-block'}),
                # word count
                html.Div([
                    html.P("จำนวนคำในประโยค(ขั้นต่ำ):"),
                    dcc.Slider(0, 1000, 1000/5,
                    value=100,tooltip={"placement": "bottom", "always_visible": True},
                    id='slider-count_word-names'),
                    ],style={'width': '49%', 'display': 'inline-block',"float":"left"}),
                html.Div([
                    html.P("แผนภูมิจำนวนตัวอักษรกับจำนวนความคิดเห็น"),
                    dcc.Graph(id="pie-charts-count_word-graph"),
                    html.P(id ="text_sum_word",style={'whiteSpace': 'pre-line'})],style={'width': '70%','display': 'inline-block'}),
                    ],
                    id="grid-print-area",
                ),
                    html.Div(id="dummy"),
                    ],style={'width': '70%','display': 'inline-block',"float":"right"}
                )
                ])
        @app1.callback(
            Output("pie-charts-exp-graph", "figure"),
            Output("pie-charts-Gender-graph", "figure"),
            Output("pie-charts-carcer-graph", "figure"), 
            Output("pie-charts-useful-graph", "figure"),
            Output("pie-charts-sym-graph", "figure"),
            Output("pie-charts-count_word-graph", "figure"),
            Output("text_sum_exp", 'children'),
            Output("text_sum_Gender", 'children'),
            Output("text_sum_cancer", 'children'), 
            Output("text_sum_useful", 'children'),
            Output("text_sum_sym", 'children'), 
            Output("text_sum_word", 'children'),
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
            nms = nms[nms['defind_Genden_with_python'].isin(Gender)]
            nms = nms[nms['defind_cancer_with_nlp'].isin(carcer)]
            nms = nms[nms['use_ful'].isin(useful)]
            sym_c = nms.iloc[:, 10:-1]
            sym_ca = sym_c.melt()
            sym_can = (pd.crosstab(sym_ca['variable'], sym_ca['value']).rename(columns={0: 'ไม่มีการเล่า', 1: 'มีการเล่า'}))
            plot_data=sym_can['มีการเล่า'].reset_index()
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
            nms = nms[nms['count']>=count_word]
            fig_1 = px.pie(nms, values='count_plot', names=nms['defind_exp_with_python'],color_discrete_sequence=px.colors.sequential.Emrld)
            fig_2 = px.pie(nms, values='count_plot', names=nms['defind_Genden_with_python'],color='defind_Genden_with_python',color_discrete_map={'Male':'darkblue','Female':"magenta",'Gender not specified':'gray'})
            fig_3 = px.histogram(nms, x=nms['defind_cancer_with_nlp'], y='count_plot',barmode='group',text_auto=True)
            fig_4 = px.pie(nms, values='count_plot', names=nms['use_ful'],color_discrete_sequence=px.colors.sequential.Aggrnyl)
            fig_5 = px.histogram(plot_sym, x='variable', y='มีการเล่า',barmode='group',text_auto=True)
            fig_6 = px.line(nms,x='name', y='count')
            avg_33=nms['count'].mean()
            #สรุปกราฟประสบการณ์
            sum_all_exp = nms['defind_exp_with_python']
            sum_non_exp = nms[nms['defind_exp_with_python']=="Didn't tell the experience"]
            sum_other_exp = nms[nms['defind_exp_with_python']=="Tell other people's experiences"]
            sum_self_exp = nms[nms['defind_exp_with_python']=='Tell about your own experiences']
            value_non_p = (len(sum_non_exp)/len(sum_all_exp))*100
            value_other_p = (len(sum_other_exp)/len(sum_all_exp))*100
            value_self_p = (len(sum_self_exp)/len(sum_all_exp))*100
            text_1_en = f'''ผลจากกราฟ ประสบการณ์กับความคิดเห็น พบว่าความคิดเห็นที่ไม่ได้เล่าประสบการณ์เกี่ยวกับโรคมีจำนวน {len(sum_non_exp)}ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p, 2)} โดยความคิดเห็นที่เป็นการเล่าประสบการณ์เกี่ยวกับโรคสำหรับหัวข้อนี้ส่วนมากเป็น 
            { f"การเล่าประสบการณ์คนอื่นจำนวน {len(sum_other_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} ในขณะที่อีก{len(sum_self_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} เป็นการเล่าจากประสบการณ์ตนเอง" 
            if len(sum_other_exp) > len(sum_self_exp) else 
            f"การเล่าประสบการณ์ตัวเองจำนวน {len(sum_self_exp)} ความคิดเห็นคิดเป็นร้อยละ {round(value_self_p,2)} ในขณะที่อีก {len(sum_other_exp)}ความคิดเห็นคิดเป็นร้อยละ {round(value_other_p,2)} เป็นการเล่าจากประสบการณ์คนอื่น"}'''
            #สรุปกราฟเพศ 
            sum_all_gen = nms['defind_Genden_with_python']
            sum_female_gen = nms[nms['defind_Genden_with_python']=='Female']
            sum_male_gen = nms[nms['defind_Genden_with_python']=='Male']
            sum_non_gen = nms[nms['defind_Genden_with_python']=='Gender not specified']
            value_female_p_gen = (len(sum_female_gen)/len(sum_all_gen))*100
            value_male_p_gen = (len(sum_male_gen)/len(sum_all_gen))*100
            value_non_p_gen = (len(sum_non_gen)/len(sum_all_gen))*100
            text_2_en = f'''ผลจากกราฟ เพศกับความคิดเห็น พบว่า ความคิดเห็นที่ไม่สามารถระบุเพศได้มีจำนวน {len(sum_non_gen)} ความคิดเห็น คิดเป็นร้อยละ {round(value_non_p_gen, 2)} โดยความคิดเห็นที่มีการระบุเพศ สำหรับหัวข้อนี้ส่วนมากเป็น 
            { f"เพศชายจำนวน {len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_male_p_gen,2)} ในขณะที่อีก{len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_female_p_gen,2)} เป็นเพศหญิง" 
            if len(sum_male_gen) > len(sum_female_gen) else 
            f"เพศหญิงจำนวน {len(sum_female_gen)}ความคิดเห็น คิดเป็นร้อยละ{round(value_female_p_gen,2)} ในขณะที่อีก{len(sum_male_gen)}ความคิดเห็น คิดเป็นร้อยละ {round(value_male_p_gen,2)} เป็นเพศชาย"}'''
            # สรุปกราฟโรค
            nms_can = nms[['defind_cancer_with_nlp','count_plot']]
            nms_gro_cancer = nms_can.groupby('defind_cancer_with_nlp').sum().reset_index().sort_values(by='count_plot',ascending=False)
            text_3_en ='โรคทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
            for fill in range(len(nms_gro_cancer)):
                p_can = (nms_gro_cancer["count_plot"][fill]/nms_gro_cancer["count_plot"].sum())*100
                text_3_en = text_3_en + f'\n- {nms_gro_cancer["defind_cancer_with_nlp"][fill]} มีจำนวน {nms_gro_cancer["count_plot"][fill]} ความคิดเห็น คิดเป็นร้อยละ {round(p_can,2)}'
            # สรุปกราฟมีประโยชน์หรือไม่มีประโยชน์
            sum_all_useful = nms['use_ful']
            sum_have_useful = nms[nms['use_ful']=='maybe_useful']
            sum_not_useful = nms[nms['use_ful']=='Not useful or not giving too much information']
            value_have_useful_p = (len(sum_have_useful)/len(sum_all_useful))*100
            value_not_useful_p = (len(sum_not_useful)/len(sum_all_useful))*100
            text_4_en= f'''ผลจากกราฟ ความมีประโยชน์กับความคิดเห็น พบว่าส่วนมากเป็นความคิดเห็นที่
            {f"อาจมีประโยชน์จำนวน {len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_have_useful_p,2)} ในขณะที่อีก{len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_not_useful_p,2)} ความคิดเห็นที่ไม่มีประโยชน์" 
            if len(sum_have_useful) > len(sum_not_useful) else 
            f"ไม่มีประโยชน์จำนวน {len(sum_not_useful)}ความคิดเห็น คิดเป็นร้อยละ{round(value_not_useful_p,2)} ในขณะที่อีก{len(sum_have_useful)}ความคิดเห็น คิดเป็นร้อยละ {round(value_have_useful_p,2)} ความคิดเห็นที่อาจมีประโยชน์"}'''
            #อาการ
            text_5_en ='อาการทั้งหมดที่พบในหัวข้อนี้ได้เเก่ \n'
            for filler in range(len(plot_sym)):
                plot_sym_next = plot_sym.reset_index()
                text_5_en = text_5_en + f'- {plot_sym_next["variable"][filler]} มีจำนวน {plot_sym_next["มีการเล่า"][filler]} ความคิดเห็น \n'
            # count word
            text_6_en= f'''จากกราฟจะพบว่า ยอดไลค์ในหัวข้อนี้มีค่ามากที่สุดคือ {nms['count'].max()}\n
                ยอดไลค์ในหัวข้อนี้มีค่าน้อยที่สุดคือ{nms['count'].min()}\n
                ยอดไลค์ในหัวข้อนี้มีค่าเฉลี่ยที่สุดคือ{round(avg_33,2)}\n'''
            return [fig_1,fig_2,fig_3,fig_4,fig_5,fig_6,text_1_en,text_2_en,text_3_en,text_4_en,text_5_en,text_6_en]
        app1.clientside_callback(
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
    return render_template('login2.html')

# @server.route('/page3_2.py',methods=["POST","GET"])
# def index_3():
#     return render_template('login2.html')

# @server.route('/page2_2.py',methods=["POST","GET"])
# def index_4():
#     soure_b = pd.read_csv('soure_url.csv')
#     soure = soure_b['url'][0]
#     if soure == 'www.facebook.com':
#         data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
#         def sort_data(column_name):
#             if column_name == 'like':
#                 data.sort_values('like', inplace=True, ascending=False)
#             elif column_name == 'การตอบกลับ':
#                 data.sort_values('rechat', inplace=True, ascending=False)
#             elif column_name == 'ความยาวของความคิดเห็น':
#                 data.sort_values('count', inplace=True, ascending=False)
#             else:
#                 pass
#             return data
#         sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
#         # number_of_rows = len(data)
#         # number_of_columns = len(data.columns) 
#         data_cancer= pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
#         name_can = data_cancer['name_cancarTH'].dropna().to_list()
#         symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
#     elif soure == 'www.reddit.com':
#         data =  pd.read_csv("data_commentsred_docter.csv")
#         def sort_data(column_name):
#             if column_name == 'ความยาวของความคิดเห็น':
#                 data.sort_values('count', inplace=True, ascending=False)
#             else:
#                 pass
#             return data
#         sort_options = ['ความยาวของความคิดเห็น'] 
#         data_cancer= pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
#         name_can = data_cancer['cancer_names_en'].dropna().to_list()
#         symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
#     descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
#     descriptive = descriptive.iloc[:, 1:]
#     tables_d = descriptive.to_html(classes='table table-striped', index=False)
#     # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
#     sorted_data = sort_data('like')
#     tables = sorted_data.to_html(classes='table table-striped', index=False)
#     return render_template('output2.html', tables=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
#                            ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])

# @server.route('/page2_3.py',methods=["POST","GET"])
# def index_7():
#     soure_b = pd.read_csv('soure_url.csv')
#     soure = soure_b['url'][0]
#     if soure == 'www.facebook.com':
#         data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
#         def sort_data(column_name):
#             if column_name == 'like':
#                 data.sort_values('like', inplace=True, ascending=False)
#             elif column_name == 'การตอบกลับ':
#                 data.sort_values('rechat', inplace=True, ascending=False)
#             elif column_name == 'ความยาวของความคิดเห็น':
#                 data.sort_values('count', inplace=True, ascending=False)
#             else:
#                 pass
#             return data
#         sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
#         data_cancer= pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
#         name_can = data_cancer['name_cancarTH'].dropna().to_list()
#         symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
#     elif soure == 'www.reddit.com':
#         data =  pd.read_csv("data_commentsred_docter.csv")
#         def sort_data(column_name):
#             if column_name == 'ความยาวของความคิดเห็น':
#                 data.sort_values('count', inplace=True, ascending=False)
#             else:
#                 pass
#             return data
#         sort_options = ['ความยาวของความคิดเห็น'] 
#         data_cancer= pd.read_csv('name_cancer_and_symptoms_lowercase.csv')
#         name_can = data_cancer['cancer_names_en'].dropna().to_list()
#         symptoms_can = data_cancer['Key_symptoms_EN'].dropna().to_list()
#     descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
#     descriptive = descriptive.iloc[:, 1:]
#     tables_d = descriptive.to_html(classes='table table-striped', index=False)
#     # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
#     sorted_data = sort_data('like')
#     tables = sorted_data.to_html(classes='table table-striped', index=False)
#     return render_template('output3.html', tables=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
#                            ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])

# @server.route('/page1_2', methods=['POST','GET'])
# def index5():
#   return render_template('input3.html')

# @server.route('/page1_3', methods=['POST','GET'])
# def index6():
#   return render_template('input4.html')

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server},
)

if __name__ == '__main__':
    run_simple("localhost", 8050, application)
