from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException 
import time
import pandas as pd
names=[]
comments=[]
data = pd.DataFrame()

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
html =  BeautifulSoup(driver.page_source, "html.parser")
result = html.find_all('div',{"class":"py-0 xs:mx-xs mx-2xs inline-block max-w-full"})
name = html.find_all(['a',"span"],{"class":["truncate font-bold text-neutral-content-strong text-12 hover:underline","truncate font-bold text-neutral-content-strong text-12 hover:no-underline text-neutral-content-weak"]})
for item in result:
    comments.append(item.text)
for item in name :
    names.append(item.text)
print(comments)
# print(name)
# data['name'] = names
# data['comments'] = comments
# data=data.applymap(lambda x: " ".join(x.split()) if isinstance(x, str) else x)
# print(data)
# print(comments)
# print(len(comments))
# print(len(names))
# data.to_csv('data_comments.csv')
