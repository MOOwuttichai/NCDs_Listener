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
        url_is = url #'https://www.facebook.com/'+str(url_use)
        browser.get(url_is)
        wait = WebDriverWait(browser, 120) # once logged in, free to open up any target page
        time.sleep(7)


        count = 0
        switch = True
        old_numReviews = 0
        specifiedNumber = 999 # number of reviews to get
        # เปิดความคิดเห็นเพิ่มเติม
        try: 
            while switch:
                count += 1
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                l = browser.find_element(By.XPATH,k)
                l.click()
                a+=50
                k = x[:162]+str(a)+x[164:]
                time.sleep(5)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
        except:
            pass

        # เปิดเพิ่มเติม
        for i in range(3):
            r=int(aoa[-81:-80])
            for i in range(19999):
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
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        comments=[]
        names=[]
        html =  BeautifulSoup(browser.page_source, "html.parser")
        result = html.find_all('div',{"class":"xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"})
        name = html.find_all(["span"],{"class":"x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa x1s688f xzsf02u"})
        for item in result:
            comments.append(item.text)
        FBcomments = comments
        for item in name :
            names.append(item.text)
        data = pd.DataFrame()
        #เติมชื่อขาดหรือลบชื่อเกินโดยอิ้งจากcomment
        if len(FBcomments)>len(names):
            differ = len(FBcomments)-len(names)
            for i in range(differ):
                names.append(f'fillname_{i}')
        elif len(FBcomments)<len(names):
            differ = len(names)-len(FBcomments)
            for i in range(differ):
                FBcomments.append('comments_miss')
        data['name'] = names
        data['comments'] = FBcomments
        data=data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
        data = data[data['comments'] != 'comments_miss']
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
        data['name'] = names
        data['comments'] = comments
        data=data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
        data = data[data['comments'] != 'comments_miss']
    return  render_template('output.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)

if __name__ == '__main__':
  app.run()
