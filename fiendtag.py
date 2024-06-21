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
  return render_template('index.html', skills=name_can,symptoms=symptoms_can)

@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
  if request.method == 'POST':
        # ข้อมูลที่ได้รับจากการกรอง
        skill = request.form['skill']
        symptom  = request.form['symptom'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        # ข้อมูลอาการเพิ่มเติม
        data_defu = pd.read_csv('name_cancer_and_symptoms (2).csv')
        data_defu_sym = data_defu[['Key_symptoms_TH','Values_symptoms_TH']].dropna()
        data_value_TH = pd.DataFrame()
        data_symptoms_TH = pd.DataFrame()
        data_value_TH['name_cancarTH_se']=name_cancer
        data_symptoms_TH['Key_symptoms_TH'] =name_symptom
        data_symptoms_TH_1 = data_symptoms_TH.merge(data_defu_sym, how='left',on='Key_symptoms_TH')
        print(data_symptoms_TH_1)
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
        all_data.to_csv('all_data_nameandsym.csv', index=False, encoding='utf-8-sig')
        msg = 'New record created successfully'  
        return jsonify(msg)

if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0', port=8001)