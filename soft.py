import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# โหลดข้อมูล CSV
data = pd.read_csv('data_commentsFB_docter_test1.csv')

# ฟังก์ชันสำหรับเรียงลำดับข้อมูล
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

# เส้นทางสำหรับหน้าหลัก
@app.route('/')
def index():
    # เตรียมตัวเลือกสำหรับ dropdownlist
    sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']

    # เรียงลำดับข้อมูลตามค่าเริ่มต้น (like)
    sorted_data = sort_data('like')
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('index_soft.html', data=[tables],titles=data.columns.values, sort_options=sort_options)

# เส้นทางสำหรับการเรียงลำดับข้อมูล
@app.route('/sort', methods=['POST'])
def sort():
    # เตรียมตัวเลือกสำหรับ dropdownlist
    sort_options = ['like', 'การตอบกลับ', 'ความยาวของความคิดเห็น']
    # รับค่าคอลัมน์ที่เลือกจาก dropdownlist
    column_name = request.form['sort_column']
    # เรียงลำดับข้อมูลตามคอลัมน์ที่เลือก
    sorted_data = sort_data(column_name)
    tables = sorted_data.to_html(classes='table table-striped', index=False)
    # ส่งข้อมูลไปยังเทมเพลต HTML
    return render_template('index_soft.html', data=[tables],titles=data.columns.values, sort_options=sort_options)

if __name__ == '__main__':
    app.run(debug=True)
