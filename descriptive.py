from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
 
 
@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    data = pd.read_csv('data\data_commentsFB_docter.csv')
    tables = data.to_html(classes='table table-striped', index=False)
    return render_template('templates/show_csv_data.html',tables=tables, titles=data.columns.values)
 
 
 
if __name__ == '__main__':
    app.run(debug=True)