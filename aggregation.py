from flask import Flask, jsonify, request, make_response
import requests
import json


app = Flask(__name__)


@app.route("/api/covid19_data", methods=['GET'])
def get_ingest_covid19_data():
    print('in here 1')
    response = requests.get("https://api.covid19api.com/all")#"http://localhost:8000/")
    #json_data = json.loads(response.text)
    print('in here 2')
    # print(r)
    # print('in here 3')
    # return jsonify(r.text)
    return response.text


if __name__ == '__main__':
    app.run(debug=True)
