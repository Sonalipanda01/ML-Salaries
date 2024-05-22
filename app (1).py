from flask import Flask, jsonify, send_from_directory
import pandas as pd
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Load data
data = pd.read_csv('salaries.csv')

# Aggregate data for main table
main_table = data.groupby('Year').agg(
    total_jobs=('job_title', 'count'),
    average_salary=('salary', 'mean')
).reset_index()

@app.route('/main_table', methods=['GET'])
def get_main_table():
    return jsonify(main_table.to_dict(orient='records'))

@app.route('/job_titles/<int:year>', methods=['GET'])
def get_job_titles(year):
    filtered_data = data[data['Year'] == year]
    job_titles = filtered_data['Job Title'].value_counts().reset_index()
    job_titles.columns = ['Job Title', 'Count']
    return jsonify(job_titles.to_dict(orient='records'))

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
