from flask_cors import CORS  # comment this on deployment
from flask import request
import json
import os

# from api.client import NavitiaClient
# from utils import add_coordinates
from itinerary import Itinerary
from flask import Flask

app = Flask(__name__)
CORS(app)

# client = NavitiaClient()

print(os.getcwd())
JSON_PATH = os.path.join('data', 'stations_list.json')

itineraries_response = {'status': False}

@app.route('/prep_itineraries', methods=['POST'])
def prep_itineraries():
#     it = Itinerary(
#         request.json["departure"],
#         request.json["arrival"]
#     )
#     result = it.get_itineraries()
#     result = add_coordinates(result)

    file = open(os.path.join('data', 'test_samples', 'original.json'), mode='r', encoding='utf8')
    result = json.load(file)
    result = add_coordinates(result)

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

def add_coordinates(journeys: dict):
    '''
    Adds X Y coordinates for each station to a journey.
    '''
    for j_idx in journeys.keys():
        sections = journeys[j_idx]["sections"]
        for s_idx in sections.keys():
            section = sections[s_idx]
            if section["mode"] == "Métro":
                code = section["info"]["code"]
                all_stops_list = open(os.path.join("data", "stations", code + ".csv"), mode='r', encoding='utf8').read().split('\n')
                stations_metadata = json.loads(open(os.path.join("data", "stations_list.json"), mode='r', encoding='utf8').read())
                selected_stops = section["info"]["stops"]
                stations, angles = generate_xy(stations_metadata["stations"], all_stops_list, selected_stops, code)

                journeys[j_idx]["sections"][s_idx]["stations"] = stations
                journeys[j_idx]["sections"][s_idx]["angles"] = angles

    return journeys

def generate_xy(all_lines_list: list, all_stops_list: list, selected_stops: list, code):
    line_dict_stations = filter(lambda k: k["number"] == code and k["mode"] == "stations", all_lines_list)
    selected_station = next(line_dict_stations)
    x_coord_list = [k for k in selected_station["x"] if k != "_"]
    y_coord_list = [k for k in selected_station["y"] if k != "_"]

    chosen_x_stations = [x_coord_list[s] for s in range(len(all_stops_list)) if all_stops_list[s] in selected_stops]
    chosen_y_stations = [y_coord_list[s] for s in range(len(all_stops_list)) if all_stops_list[s] in selected_stops]

    line_dict_angles = filter(lambda k: k["number"] == code and k["mode"] == "angles", all_lines_list)
    selected_angles_dict = next(line_dict_angles)

    lowerbound = None
    upperbound = None
    for i in range(len(selected_angles_dict['x'])):
        if selected_angles_dict['x'][i] == int(chosen_x_stations[0]) and selected_angles_dict['y'][i] == int(chosen_y_stations[0]):
            lowerbound = i
        if selected_angles_dict['x'][i] == int(chosen_x_stations[-1]) and selected_angles_dict['y'][i] == int(chosen_y_stations[-1]):
            upperbound = i

    chosen_x_angles = selected_angles_dict['x'][min(lowerbound, upperbound):max(upperbound, lowerbound)]
    chosen_y_angles = selected_angles_dict['y'][min(lowerbound, upperbound):max(upperbound, lowerbound)]

    return {"x": chosen_x_stations, "y": chosen_y_stations}, {"x": chosen_x_angles, "y": chosen_y_angles}

if __name__ == '__main__':
    app.run()
