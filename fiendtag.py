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
        skill = request.form['skill']
        symptom  = request.form['symptom'] 
        name_cancer=skill.split(', ')
        name_symptom = symptom.split(', ')
        print(name_cancer)
        print(name_symptom)
        msg = 'New record created successfully'  
        return jsonify(msg)

if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0', port=8001)