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
app1 = dash.Dash(requests_pathname_prefix="/app1/")

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
    try:
        e_3 = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div[3]/div[2]/div/div[2]/span/span'
    except:
        pass
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
        try:
            e_3 = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div[3]/div[2]/div/div[2]/span/span'
            l_l_l = browser.find_element(By.XPATH,e_3)
            l_l_l.click()
            iframe = browser.find_element(By.CLASS_NAME, "x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x78zum5 xdt5ytf x1iyjqo2 x1al4vs7")
            ActionChains(browser)\
                .scroll_to_element(iframe)\
                .scroll_by_amount(0, 50)\
                .perform()
        except:
            pass
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
        result = html.find_all('div',{"class":"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u"})
        # ## name
        name = html.find_all(["span"],{"class":"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
        # ## re_chat
        for i in range(len(result)):
            x1=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/text()')
            y1=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/div/div[4]/text()')
            z2=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[2]/div/div/div[2]/div[2]/span/span/text()')
            z1=x1+y1+z2
            try:
                re_chat_all.append((re.findall(r'\b\d+\b',z1[0]))[0])
            except:
                re_chat_all.append(0)
        # like
        for i in range(len(result)):
            x2=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/span/div/div[1]/span/text()')
            xy2=dom.xpath(f'/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div[3]/div[{i+2}]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/span/div/div[1]/span/text()')
            try:
                try:
                    like_kk.append(x2[0])
                except:
                    like_kk.append(xy2[0])
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
    df = pd.read_csv('Data_scraper.csv')
    resp = make_response(df.to_csv())
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
 
        return render_template('Page 2 use_file_after.html')
    return render_template("Page 2 use_file.html")

@server.route('/after_pepar', methods = ['POST','GET'])   
def success():   
    try:   
        data_file_path = session.get('uploaded_data_file_path', None)
        # read csv
        url_chack = request.form['language']
        data_soure_a = {'url':[url_chack]}
        data_soure_b = pd.DataFrame(data_soure_a)
        data_soure_b.to_csv('soure_url.csv',index=False)
        data= pd.read_csv(data_file_path,encoding='utf-8-sig')
    except:
        data = pd.read_csv('Data_scraper.csv')
    tables = data.to_html(classes='table table-striped', index=False)
    return  render_template('output.html',tables=[tables])

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server},
)

if __name__ == '__main__':
    run_simple("localhost", 8050, application)
