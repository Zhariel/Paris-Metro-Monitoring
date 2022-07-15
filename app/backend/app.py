from flask_cors import CORS  # comment this on deployment
from flask import request
import json
import os

# from api.client import NavitiaClient
from app.backend.utils import add_coordinates
from api.itinerary import Itinerary
from flask import Flask

app = Flask(__name__)
CORS(app)

# client = NavitiaClient()

print(os.getcwd())
JSON_PATH = os.path.join('data', 'stations_list.json')

itineraries_response = {'status': False}

@app.route('/prep_itineraries', methods=['POST'])
def prep_itineraries():
    it = Itinerary(
        request.json["departure"],
        request.json["arrival"]
    )
    result = it.get_itineraries()
    result = add_coordinates(result)

    # file = open(os.path.join('data', 'test_samples', 'original.json'), mode='r', encoding='utf8')
    # result = json.load(file)
    # result = add_coordinates(result)

    global itineraries_response
    itineraries_response = {'status': True, 'itineraries': result}
    return "200"


@app.route('/itineraries', methods=['GET'])
def itineraries():
    global itineraries_response
    response = itineraries_response

    return response

@app.route('/stations', methods=['GET'])
def stations():
    file = open(JSON_PATH)
    json_object = (json.load(file))

    return json_object


if __name__ == '__main__':
    app.run()
