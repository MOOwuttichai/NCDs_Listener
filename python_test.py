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
from flask import Flask, request, render_template, session, redirect, url_for,jsonify
import numpy as np
import pandas as pd
import os

app = Flask(__name__,static_folder=os.path.join(os.getcwd(),'static'))

@app.route('/', methods=['GET'])
def index():
  return render_template('input.html')

@app.route('/process.py', methods=['POST'])
def process():
    url = request.form['url']
    url_chack = str(url).split('/')[2]
    data_soure_a = {'url':[url_chack]}
    data_soure_b=pd.DataFrame(data_soure_a)
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
    elif url_chack == 'www.reddit.com':
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

    return  render_template('output.html',  tables=[tables], titles=data.columns.values, 
                            sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])
#number_of_rows=number_of_rows, number_of_columns=number_of_columns

@app.route('/sort', methods=['POST','GET'])
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
    return render_template('output.html', tables=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_descript=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1],soure=soure)
#number_of_rows=number_of_rows, number_of_columns=number_of_columns,

@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
  if request.method == 'POST':
        # ข้อมูลที่ได้รับจากการกรอง
        skill = request.form['skill']
        symptom  = request.form['symptom'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        # ข้อมูลอาการเพิ่มเติม
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
        all_data.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
        msg = 'New record created successfully'  
        return jsonify(msg)     


@app.route('/test.py', methods=['POST','GET'])
def test():
    max_v = []
    min_v = []
    avg_v = []
    _ = ['like','จำนวนการตอบกลับ','ความยาว']
    data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
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
    tables = descriptive.to_html(classes='table table-striped', index=False)
    return render_template('output.html', tables=[tables], titles=data.columns.values, number_of_rows=data.shape[0], number_of_columns=data.shape[1])


if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0', port=8001)
