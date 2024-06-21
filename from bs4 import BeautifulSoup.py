from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import time
import pandas as pd
import json
import time
import re
import datetime
from lxml import etree 
import requests 
import re

names=[]
comments=[]
up_comment=[]


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
url = 'https://www.reddit.com/r/memes/comments/1c6yxj9/most_useless_feature/'
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

#up data
x='/html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[1]/shreddit-comment-action-row//div/div/div[1]/span/span/faceplate-number'
y='/html/body/shreddit-app/div/div[1]/div/main/div/faceplate-batch/shreddit-comment-tree/shreddit-comment[1]/shreddit-comment/shreddit-comment-action-row//div/div/div[1]/span/span/faceplate-number'
kok=y
POP = x
roki=2
y_1=int(x[103:104])
ror = []
for i in range(100):
  ror.append(POP)
  roki=2
  kok = y[:103]+str(y_1)+y[104:122]+y[-71:]
  for j in range(20):
    ror.append(kok)
    retio = '[' + str(roki) + ']'
    kok = y[:103]+str(y_1)+y[104:122]+retio+ y[-71:]
    roki+=1
  y_1+=1
  POP = x[:103]+str(y_1)+x[-72:]

html =  BeautifulSoup(driver.page_source, "html.parser")
soup_red = BeautifulSoup(driver.page_source, 'lxml')
dom_red = etree.HTML(str(soup_red))
result = html.find_all(['div','div'],{"class":["py-0 xs:mx-xs mx-2xs inline-block max-w-full","md text-14"]})
name = html.find_all(['a',"span",'a'],{"class":["truncate font-bold text-neutral-content-strong text-12 hover:underline","truncate font-bold text-neutral-content-strong text-12 hover:no-underline text-neutral-content-weak","author-name whitespace-nowrap text-neutral-content visited:text-neutral-content-weak  a no-visited no-underline hover:no-underline"]})

for item in result:
    comments.append(item.text)
for item in name :
    names.append(item.text)

data_comment=pd.DataFrame(data={'comments':comments})
data_name=pd.DataFrame(data={'name':names})
data_up=pd.DataFrame(data={'up':up_comment})
data = data_comment
data = data.join(data_name)
data = data.join(data_up)
data = data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
data = data.iloc[:,[1,0,2]]
data.to_csv('data_comments_test1.csv')
