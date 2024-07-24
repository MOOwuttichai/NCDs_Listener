import subprocess
import time
import pyautogui
import datetime
import pandas as pd
import dash
from dash import html,Dash

# # data_for_dash_facebook = pd.read_csv('data_pre_setting.csv', encoding='utf-8-sig')
# # data_for_dash_facebook.drop('sum_ch', axis=1, inplace=True)
# # data_for_dash_facebook.to_csv('data_pre_setting.csv', encoding='utf-8-sig',index=False)
data_for_dash_facebook = pd.read_csv('data_for_dash_01.csv', encoding='utf-8-sig')
data_for_dash_facebook = data_for_dash_facebook.drop(['use_ful'], axis=1)
data_for_dash_facebook.to_csv('Atest_for_cheatgpt.csv',index=False,encoding='utf-8-sig')
# data_for_dash_raddit = pd.read_csv('data_test\data_pre_red2_up.csv', encoding='utf-8-sig')
# data_for_dash = pd.read_csv('data_pre.csv', encoding='utf-8-sig')
# if len(data_for_dash) == len(data_for_dash_raddit):
#     data_for_dash = data_for_dash_facebook
#     data_for_dash.to_csv('data_pre.csv', encoding='utf-8-sig',index=False)
# else :
#     data_for_dash = data_for_dash_raddit
#     data_for_dash.to_csv('data_pre.csv', encoding='utf-8-sig',index=False)

