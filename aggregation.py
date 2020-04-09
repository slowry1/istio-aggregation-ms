from flask import Flask, jsonify, request, make_response
import requests
import json
from urllib.request import urlopen


app = Flask(__name__)


@app.route("/api/covid19_summary_data", methods=['GET'])
def get_ingest_covid19_summary_data():
    print('in here 1')
    response = requests.get("http://localhost:8000/summary")
    json_data = json.loads(response.text)
    print('in here 2')
    return json_data


@app.route("/api/covid19_countries_data", methods=['GET'])
def get_ingest_covid19_countries_data():
    print('in here 1')
    response = requests.get("http://localhost:8000/countries")
    json_data = json.loads(response.text)
    print('in here 2')
    return json_data


if __name__ == '__main__':
    app.run(debug=True)
