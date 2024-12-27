from flask import Flask, render_template, request
import sqlite3
import os
import pandas as pd

DEBUG=False
DB_FILE=f"{os.path.abspath(os.path.dirname(__file__))}/../database.sqlite"

def debug(text):
    if DEBUG:
        print(text)


app = Flask(__name__)

# Load the data

@app.route('/')
def home():
    conn = sqlite3.connect(DB_FILE) 

    df = pd.read_sql_query('''SELECT DISTINCT Name from MASTER''', conn)
    # Pass unique person names to the frontend
    people = df['Name'].unique()

    debug(people)
    conn.close()

    return render_template('index.html', people=people)


@app.route('/get-data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_FILE) 

    # Get the selected person from the request
    person = request.args.get('person')
    # Filter data for the selected person
    filtered_data = pd.read_sql_query(f'''SELECT * from MASTER where Name = '{person}' ''', conn)

    conn.close()
    return filtered_data.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=DEBUG)
