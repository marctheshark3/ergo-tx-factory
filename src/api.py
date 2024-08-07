# api.py

from flask import Flask, jsonify, request
from database import PostgresDB
import pandas as pd

app = Flask(__name__)
db = PostgresDB()

@app.route('/sigs-core/<table_name>', methods=['GET'])
def get_table_data(table_name):
    conditions = request.args.to_dict()
    data = db.fetch_data(table_name, conditions)
    columns = db.get_column_names(table_name)
    df = pd.DataFrame(data, columns=columns)
    return df.to_json(orient='records')

if __name__ == '__main__':
    app.run(debug=True)