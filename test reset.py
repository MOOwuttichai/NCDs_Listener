import datetime
import pandas as pd
import dash
from dash import html,Dash
data_for_dash_facebook = pd.read_csv('data_pre_setting.csv', encoding='utf-8-sig')
data_for_dash_facebook.drop('sum_ch', axis=1, inplace=True)
data_for_dash_facebook.to_csv('data_pre_setting.csv', encoding='utf-8-sig',index=False)