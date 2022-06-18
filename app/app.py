import flask
from flask import Flask, send_from_directory
# from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from flask import request
from flask import Flask
import json
import os

app = Flask(__name__)
CORS(app)

print(os.getcwd())
JSON_PATH = os.path.join('..', 'data', 'stations_list.json')


@app.route('/health')
def health():
    return "up"


@app.route('/stations')
def stations():
    file = open(JSON_PATH)
    json_object = (json.load(file))
    print(type(json_object))
    # print(json_object)

    return json_object


if __name__ == '__main__':
    app.run()
