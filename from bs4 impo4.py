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
from lxml import etree 
import requests 
import re
#,'BeautifulSoup','selenium','bs4'
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
browser.get('https://www.facebook.com/story.php?story_fbid=738492865098283&id=100068127288896&rdid=KSfcPd478i4jBurb')
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
        time.sleep(7)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(11)
except:
    pass

SCROLL_PAUSE_TIME = 4

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
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
time.sleep(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#setup bs4 and data
# #ดึงข้อมูล
comments=[]
names=[]
re_chat_all=[]
like_kk = []
count=[]
xpath_like = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[4]/div/div/div[2]/div[3]/div[2]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/span/div/div[1]/span'
html =  BeautifulSoup(browser.page_source, "html.parser")
soup = BeautifulSoup(browser.page_source, 'lxml')
dom = etree.HTML(str(soup))
# ## comment
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
#เริ่มเก็บข้อมูล
for item in result:
    comments.append(item.text)
FBcomments = comments[2:]
for item in name :
    names.append(item.text)
data = pd.DataFrame()
#นับความยาว ความคิดเห็น
for item in FBcomments:
    count.append(len(item))

#เติมlikeที่ขาด
if len(FBcomments)>len(like_kk):
    differ = len(FBcomments)-len(like_kk)
    for i in range(differ):
        like_kk.append(0)
elif len(FBcomments)<len(like_kk):
    differ = len(like_kk)-len(FBcomments)
    for i in range(differ):
        FBcomments.append('comments_miss')
#เติมre_chatที่ขาด
if len(FBcomments)>len(re_chat_all):
    differ = len(FBcomments)-len(re_chat_all)
    for i in range(differ):
        re_chat_all.append(0)
elif len(FBcomments)<len(re_chat_all):
    differ = len(re_chat_all)-len(FBcomments)
    for i in range(differ):
        FBcomments.append('comments_miss')
#เติมre_chatที่ขาด
if len(FBcomments)>len(count):
    differ = len(FBcomments)-len(count)
    for i in range(differ):
        count.append(0)
elif len(FBcomments)<len(count):
    differ = len(count)-len(FBcomments)
    for i in range(differ):
        FBcomments.append('comments_miss')
#เติมชื่อขาดหรือลบชื่อเกินโดยอิ้งจากcomment
if len(FBcomments)>len(names):
    differ = len(FBcomments)-len(names)
    for i in range(differ):
        names.append(f'fillname_{i}')
elif len(FBcomments)<len(names):
    differ = len(names)-len(FBcomments)
    for i in range(differ):
        FBcomments.append('comments_miss')
# ทำตาราง
data['name'] = names
data['comments'] = FBcomments
data['rechat']= re_chat_all
data['like']=like_kk
data['count']=count
# data=data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
data = data[data['comments'] != 'comments_miss']
data.to_csv('data_commentsFB_docter.csv', index=False, encoding='utf-8-sig')

