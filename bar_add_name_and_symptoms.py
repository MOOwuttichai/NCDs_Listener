from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load product data from CSV
data = pd.read_csv('name_cancer_and_symptoms (2).csv')

# Function to handle user input and search for products
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        search_term = request.args.get('q')
        if search_term:
            results = data[data['Product Name'].str.lower().contains(search_term.lower())]
            return jsonify({'results': results.to_json(orient='records')})
        else:
            return jsonify({'results': []})

    if request.method == 'POST':
        search_term = request.form.get('q')
        if search_term:
            results = data[data['Product Name'].str.lower().contains(search_term.lower())]
            return render_template('search_results.html', results=results)
        else:
            return render_template('search.html')

# Route to render the search page
@app.route('/')
def search_page():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
