import pandas as pd
from api import client
from api.split_data import get_disruptions
import json
import os

from sqlclient import RDSClient
from disruption_generator import DisruptionGenerator

def request_disruptions():
    response = client.request_navitia("Metro")
    print(response["disruptions"])
    df_disruptions = get_disruptions(response["disruptions"])
    return df_disruptions

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

if __name__ == "__main__":
    # pd.set_option('display.max_columns', None)
    # disruptions = request_disruptions()
    # disruptions.to_csv(os.path.join('data', 'navitia', 'metros', 'disruptions.csv'), index=False, sep=";")
    # lines = zip(range(1, 15), [3, 3, 5, 5, 2, 2, 4, 5, 3, 4, 2, 4, 5, 3])
    # weighted_lines = [[x[0]]*x[1] for x in lines]
    # weighted_lines = [x for l in weighted_lines for x in l]
    # import random
    # print(weighted_lines)

    predict_disruptions = 'predict_disruptions'
    predict_duration = 'predict_duration'
    predict_priority = 'predict_priority'
    predict_cause = 'predict_cause'


    d = DisruptionGenerator()
    headers, disrupt = d.generate_disruptions()
    for x in disrupt:
        print(x)

    print("- - - IS DISRUPTED - - -")
    diskeys, is_disrupted = d.gen_xy_predict_disruption(disrupt)
    print(is_disrupted[1])
    # for isdr in is_disrupted:
    #     print(isdr)
    print(diskeys)
    #
    # print("- - - DURATION - - -")
    durkeys, durations = d.gen_xy_predict_duration(disrupt)
    # for dur in durations:
    #     print(dur)
    #
    # print("- - - PRIO - - -")
    prikeys, prios = d.gen_xy_predict_priority(disrupt)
    # for pri in prios:
    #     print(pri)
    #
    # print("- - - CAUSE - - -")
    caukeys, cause = d.gen_xy_predict_cause(disrupt)
    # for cau in cause:
    #     print(cau)


    from sqlclient import RDSClient
    rclient = RDSClient()

    rclient.create_db()
    rclient.create_table_generic(predict_disruptions, diskeys)
    rclient.create_table_generic(predict_duration, durkeys)
    rclient.create_table_generic(predict_priority, prikeys)
    rclient.create_table_generic(predict_cause, caukeys)
    print(rclient.tables)
    print()

    rclient.insert_dict(predict_disruptions, is_disrupted[1])

