import pandas as pd
from flask import Flask, render_template, request
import numpy as np
from numpy import nan
app = Flask(__name__)

# โหลดข้อมูล CSV
data_1 = pd.read_csv('data_commentsFB_docter_test1.csv')

# ฟังก์ชันสำหรับเรียงลำดับข้อมูล
def sort_data(column_name):
    if column_name == 'like':
        data_1.sort_values('like', inplace=True, ascending=False)
    elif column_name == 'การตอบกลับ':
        data_1.sort_values('rechat', inplace=True, ascending=False)
    elif column_name == 'ความยาวของความคิดเห็น':
        data_1.sort_values('count', inplace=True, ascending=False)
    else:
        pass
    return data_1

# เส้นทางสำหรับหน้าหลัก
@app.route('/')
def index():
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
    descriptive.to_csv('data_desc.csv',encoding='utf-8-sig')
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    
    # เตรียมตัวเลือกสำหรับ dropdownlist
    sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']

    # เรียงลำดับข้อมูลตามค่าเริ่มต้น (like)
    sorted_data = sort_data('like')
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    data_cancer = pd.read_csv('name_cancer_and_symptoms (2).csv')
    name_can = data_cancer['name_cancarTH'].dropna().to_list()
    symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('index_soft.html', data=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_d=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])
# เส้นทางสำหรับการเรียงลำดับข้อมูล
@app.route('/sort', methods=['POST'])
def sort():
    data = pd.read_csv("data_commentsFB_docter.csv", encoding='utf-8-sig')
    descriptive=pd.read_csv('data_desc.csv',encoding='utf-8-sig')
    tables_d = descriptive.to_html(classes='table table-striped', index=False)
    # เตรียมตัวเลือกสำหรับ dropdownlist
    sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
    # รับค่าคอลัมน์ที่เลือกจาก dropdownlist
    column_name = request.form['sort_column']
    # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
    sorted_data = sort_data(column_name)
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    data_cancer= pd.read_csv('name_cancer_and_symptoms (2).csv')
    name_can = data_cancer['name_cancarTH'].dropna().to_list()
    symptoms_can = data_cancer['Key_symptoms_TH'].dropna().to_list() 
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('index_soft.html', data=[tables],titles=data.columns.values, sort_options=sort_options,skills=name_can,symptoms=symptoms_can
                           ,tables_d=[tables_d], number_of_rows=data.shape[0], number_of_columns=data.shape[1])

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
    app.run(debug=True)
