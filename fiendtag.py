from flask import Flask, request, render_template, session, redirect, url_for,jsonify
import pandas as pd
import numpy as np
from numpy import nan
app = Flask(__name__)

@app.route('/')
def index():
  data = pd.read_csv('name_cancer_and_symptoms (2).csv')
  name_can = data['name_cancarTH'].dropna().to_list()
  symptoms_can = data['Key_symptoms_TH'].dropna().to_list()
  return render_template('index_page3_2.html', skills=name_can,symptoms=symptoms_can)

@app.route('/page3.py',methods=["POST","GET"])
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
        data_defind.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
      elif sorue == 'www.reddit.com':
        data_sy_na = pd.read_csv('name_cancer_and_symptoms (2).csv')
        data_defind = data_sy_na[['cancer_names_en','Key_symptoms_EN','Valuessymptoms_EN']]
        data_defind.to_csv('all_data_nameandsym.csv')
    tables = data_defind.to_html(classes='table table-striped', index=False)
    return render_template('test.html',tables=[tables])

@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
  if request.method == 'POST':
        # ข้อมูลที่ได้รับจากการกรอง
        c_submit= request.form['custId']
        skill = request.form['skill']
        symptom  = request.form['symptom'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        # ข้อมูลอาการเพิ่มเติม
        data_defu = pd.read_csv('name_cancer_and_symptoms (2).csv')
        soure_sym = pd.read_csv('soure_url.csv')
        sorue = soure_sym['url'][0]
        if sorue == 'www.facebook.com':
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
          all_data['chack_submit'] = c_submit
          all_data.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
        elif sorue == 'www.reddit.com':
          data_defu_sym_EN = data_defu[['Key_symptoms_EN','Valuessymptoms_EN']].dropna()
          data_value_EN = pd.DataFrame()
          data_symptoms_EN = pd.DataFrame()
          data_value_EN['name_cancarEN_se']=name_cancer
          data_symptoms_EN['Key_symptoms_EN'] =name_symptom
          data_symptoms_EN_1 = data_symptoms_EN.merge(data_defu_sym_EN, how='left',on='Key_symptoms_EN')
          value_symptoms_EN= data_symptoms_EN_1[data_symptoms_EN_1['Valuessymptoms_EN'].isna()]
          list_of_sym_va_en = value_symptoms_EN['Key_symptoms_EN'].tolist()
          for i in list_of_sym_va_en:
            data_symptoms_EN_1.fillna(f"['{i}']",limit=1,inplace=True)
          # สร้างตาราง
          all_data = pd.DataFrame()
          list_100 = list(range(0,100))
          all_data['index'] = list_100
          all_data = all_data.merge(data_value_EN.reset_index(), how='outer')
          all_data = all_data.merge(data_symptoms_EN_1.reset_index(), how='outer')
          all_data['chack_submit'] = c_submit
          all_data.to_csv('all_data_nameandsym.csv')
        msg = 'New record created successfully'  
        return jsonify(msg)

if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0', port=8001)